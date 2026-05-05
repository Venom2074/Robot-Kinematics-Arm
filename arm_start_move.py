import time

SCL = 3
SDA = 2

import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c, address=0x41)
pca.frequency = 50

armJoint = [servo.Servo(pca.channels[i], min_pulse=400, max_pulse=2400) for i in range(6)]

armJoint[1].angle = 120
time.sleep(0.5)
for i in range(6):
    armJoint[i].angle = 0
time.sleep(0.5)

# hold at a valid pulse-width position so servos stay firm
HOLD = 5
for i in range(6):
    armJoint[i].angle = HOLD
time.sleep(0.3)

current_angles = [float(HOLD)] * 6

print("\nAt start position. You can now adjust joint angles.")
print("Commands:  <joint>           (e.g. '0'     prints angle of joint 0)")
print("           <joint> <angle>   (e.g. '0 90'  sets joint 0 to 90°)")
print("           <joint> +<delta>  (e.g. '2 +5'  adds 5° to joint 2)")
print("           <joint> -<delta>  (e.g. '2 -5'  subtracts 5° from joint 2)")
print("Press Ctrl+C to exit and print final angles.\n")

try:
    while True:
        try:
            raw = input(">> ").strip()
            if not raw:
                continue
            parts = raw.split()

            joint = int(parts[0])
            if joint < 0 or joint > 5:
                print("Joint must be 0-5.")
                continue

            if len(parts) == 1:
                print(f"  Joint {joint} = {current_angles[joint]:.1f}°")
                continue

            val_str = parts[1]
            if val_str.startswith('+') or val_str.startswith('-'):
                new_angle = current_angles[joint] + float(val_str)
            else:
                new_angle = float(val_str)

            new_angle = max(1, min(180, new_angle))
            armJoint[joint].angle = new_angle
            current_angles[joint] = new_angle
            print(f"  Joint {joint} -> {new_angle:.1f}°")

        except ValueError:
            print("Invalid input. Example: '0' to read, '2 +5' or '0 90' to set")

except KeyboardInterrupt:
    print("\n\nFinal joint angles:")
    for i, angle in enumerate(current_angles):
        print(f"  armJoint[{i}].angle = {angle:.1f}")
    pca.deinit()
