from pymycobot import MyCobot280
import time

#Joint Id      range
#    1 	    -168 ~ 168
#    2 	    -135 ~ 135
#    3 	    -150 ~ 150
#    4 	    -145 ~ 145
#    5 	    -155 ~ 160
#    6 	    -180 ~ 180

mc = MyCobot280("/dev/ttyUSB0", 1000000)

if mc.is_power_on() == 0:
    mc.power_on()
    time.sleep(2)

mc.send_angles([0, 90, 0, -90, -90, 0], 40)
print('se mueve')
while mc.is_moving():
    pass
#for i in range(1, 7):
#    mc.set_servo_calibration(i)
#    time.sleep(1)

while mc.is_moving():
    pass
print('se acabo')
q = [0, 0, 0, 0, 0, 0]
while True:
    print("6 grados")
    q[0], q[1], q[2], q[3], q[4], q[5] = map(float, input("Ingresar coordenada: ").split())
    mc.send_angles(q, 30)
    print("moviendo")
    while mc.is_moving():
        pass