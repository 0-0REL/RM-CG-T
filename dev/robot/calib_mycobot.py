# Calibración del robot, alinear y después jola
from pymycobot import MyCobot280
import time

# The above needs to be written at the beginning of the code, meaning to import the project package

# MyCobot class initialization requires two parameters: serial port and baud rate

# The first is the serial port string, such as:
# linux: "/dev/ttyUSB0"
# windows: "COM6"
# The second is the baud rate:
# M5 version is: 1000000
# The following is as follows:
# mycobot-M5:
# linux:
# mc = MyCobot("/dev/ttyUSB0", 1000000)
# windows:
# mc = MyCobot("COM6", 1000000)
# mycobot-raspi:
# mc = MyCobot(PI_PORT, PI_BAUD)
#
# Initialize a MyCobot object
# The following is the object code for the windows version
mc = MyCobot280("/dev/ttyUSB0", 1000000)
# Power off the robot and relax the joints
time.sleep(2)
print("Relajando los servos...")
mc.release_all_servos()
# After relaxing the joints, bend the robot to align the zero position scale of the robot
time.sleep(5)
print("Calibrando los servos...")
# Calibrate the robot joints one by one
for i in range(1, 7):
    mc.set_servo_calibration(i)
    time.sleep(1)
# Power on the robot to lock the robot
mc.power_on()
time.sleep(2)
print("Enviando a la posición cero...")
mc.send_angles([0, -90.0, 0.0, 90.0, 90.0, 0.0], 10)
while mc.is_moving():
    pass
# Calibrate the robot joints one by one
print("Calibrando los servos...")
for i in range(1, 7):
    mc.set_servo_calibration(i)
    time.sleep(1)
# Power on the robot to lock the robot
mc.power_on()
time.sleep(2)
# Print all joint angles
print(mc.get_angles())
time.sleep(1)