% Robot MyCobot
%
% Depende de las siguientes funciones
% T_06.m
% jac_mycobot.m
clear
syms theta d a alpha
T_z = [cos(theta) -sin(theta) 0 0;
    sin(theta) cos(theta) 0 0;
    0 0 1 d;
    0 0 0 1];
T_x = [1 0 0 a;
    0 cos(alpha) -sin(alpha) 0;
    0 sin(alpha) cos(alpha) 0;
    0 0 0 1];
T = T_z * T_x;

syms q_1 q_2 q_3 q_4 q_5 q_6
q = [q_1 q_2 q_3 q_4 q_5 q_6];
T01 = subs(T,[a,alpha,d,theta],[0,pi/2,134.75,q_1]);
T12 = subs(T,[a,alpha,d,theta],[110,0,0,q_2]);
T23 = subs(T,[a,alpha,d,theta],[96,0,0,q_3]);
T34 = subs(T,[a,alpha,d,theta],[0,-pi/2,63.4,q_4]);
T45 = subs(T,[a,alpha,d,theta],[0,-pi/2,75.05,q_5]);
T56 = subs(T,[a,alpha,d,theta],[0,0,45.6,q_6]);

T06 = T01 * T12 * T23 * T34 * T45 * T56;
subs(T06,q,deg2rad([0.0, 90.0 0.0, -90, -90, 0]))
%% Jacobiano
doce = T06(1:3,:);
f_q = doce(:);
j = jacobian(f_q,q);
%% Exportar funciones
matlabFunction(T06(1:3,:), 'File', 'T_06', 'Vars', q);
matlabFunction(j, 'File', 'jac_mycobot', 'Vars', q);
%% Cinematica inversa
clear, clc
xd = [0  0  1  45.6;
      -1  0  0  -63.4; 
      0  -1  0  415];
q_k = deg2rad([0; 90; 0; -90; -90; 0]);
epsi=1e-3; %tolerancia en la solucion "Error"
limAng = deg2rad([-168 168;   %Limites de movimiento
                  -135 135;
                  -150 150;
                  -145 145;
                  -155 160;
                  -180 180]);
for idx = 1:1000  %Comienza calculo
    for i = 1:6 %Establece los limites de movimiento
        if q_k(i) > limAng(i,2) || q_k(i) < limAng(i,1)
                q_k(i) = sum(limAng(1,:))/2;
        end
    end
    f_q = T_06(q_k(1),q_k(2),q_k(3),q_k(4),q_k(5),q_k(6));
    error = xd(:)-f_q(:);
    if norm(error) < epsi
        %disp('Funciono')
        ok = true;
        break
    end
    Jinv = pinv(jac_mycobot(q_k(1),q_k(2),q_k(3),q_k(4),q_k(5),q_k(6)));
    q_k = q_k+Jinv*error;
    for i = 1:6 %Encierra los angulos en [-180, 180]
        while true
            if q_k(i) > 2*pi
                q_k(i) = mod(q_k(i),2*pi);
                if q_k(i) > pi
                    q_k(i) = q_k(i)-2*pi;
                end
            elseif q_k(i) < -2*pi
                q_k(i) = mod(q_k(i),-2*pi);
                if q_k(i) < -pi
                    q_k(i) = q_k(i)+2*pi;
                end
            else
                break
            end
        end
     end
end
disp(rad2deg(q_k'))
disp(T_06(q_k(1),q_k(2),q_k(3),q_k(4),q_k(5),q_k(6)))