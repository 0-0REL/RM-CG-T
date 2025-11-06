%% modelo de robot
clc,clear
L(1) = Link([0     135     0     pi/2], 'standard');
L(2) = Link([0     0       110   0],    'standard');
L(3) = Link([0     0       95    0],    'standard');
L(4) = Link([0     70      0     -pi/2], 'standard');
L(5) = Link([0     85      0     pi/2], 'standard');
L(6) = Link([0     45      0     0],    'standard');

% Crear el robot
robot = SerialLink(L, 'name', 'MiRobot');
%% Calculo
close
% xd = [0  0  1  0.0450;
%       1  0  0  -0.07; 
%       0  1  0  0.425];
xd = [0  0  1  0.1;
      1  0  0  -0.07; 
      0  1  0  0.2];
q_k = [0; 90; 0; -90; 90; 0]*(pi/180);
epsi=1e-3; %tolerancia en la solucion "Error"
limAng = [-pi/2 pi/2;   %Limites de movimiento
          -pi   0;
          -pi/2 pi/2;
          -pi/2 pi/2;
          -11*pi/18 7*pi/18;
          -pi/2 pi/2];
ok = false;
for idx = 1:1000  %Comienza calculo
    % for i = 1:6 %Establece los limites de movimiento
    %     if q_k(i) > limAng(i,2) || q_k(i) < limAng(i,1)
    %             q_k(i) = sum(limAng(1,:))/2;
    %     end
    % end
    f_q = TH_06(q_k); %Cinematica Directa
    error = xd(:)-f_q(:);
    if norm(error) < epsi
        %disp('Funciono')
        ok = true;
        break
    end
    Jinv = pinv(jacobiano_jacobot(q_k));
    q_k = q_k+Jinv*error;
    % for i = 1:6 %Encierra los angulos en [-180, 180]
    %     while true
    %         if q_k(i) > 2*pi
    %             q_k(i) = mod(q_k(i),2*pi);
    %             if q_k(i) > pi
    %                 q_k(i) = q_k(i)-2*pi;
    %             end
    %         elseif q_k(i) < -2*pi
    %             q_k(i) = mod(q_k(i),-2*pi);
    %             if q_k(i) < -pi
    %                 q_k(i) = q_k(i)+2*pi;
    %             end
    %         else
    %             break
    %         end
    %     end
    %  end
end %Termina calculo
%% Visualizar
if ok
    robot.teach(q_k');
else
    disp('No se encontró solución dentro de los límites establecidos.');
end
