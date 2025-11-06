% Parámetros DH en el orden [theta d a alpha]
% Nota: Peter Corke usa ese orden: theta, d, a, alpha
clc, clear
L(1) = Link([0     135     0     pi/2], 'standard');
L(2) = Link([0     0       110    0],    'standard');
L(3) = Link([0     0       95     0],    'standard');
L(4) = Link([0     70      0      -pi/2], 'standard');
L(5) = Link([0    85      0     pi/2], 'standard');
L(6) = Link([0     45      0      0],    'standard');

% Crear el robot
robot = SerialLink(L, 'name', 'MiRobot');

% Visualización
q = deg2rad([0 90 0 -90 90 0]);  % en radianes
robot.teach(q);
