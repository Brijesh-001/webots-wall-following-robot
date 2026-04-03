from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Motors
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# Distance sensors (ps0–ps7)
ps = []
for i in range(8):
    sensor = robot.getDevice(f'ps{i}')
    sensor.enable(timestep)
    ps.append(sensor)

# Speed
MAX_SPEED = 6.28

while robot.step(timestep) != -1:

    # Read sensors
    ps_values = [sensor.getValue() for sensor in ps]

    # Wall detection
    right_wall = ps_values[5] > 80
    front_wall = ps_values[0] > 80 or ps_values[1] > 80 or ps_values[2] > 80

    # Default speeds
    left_speed = 0.5 * MAX_SPEED
    right_speed = 0.5 * MAX_SPEED

    # 🔴 If wall in front → turn left
    if front_wall:
        left_speed = -0.5 * MAX_SPEED
        right_speed = 0.5 * MAX_SPEED

    # 🟡 If wall on right → go straight
    elif right_wall:
        left_speed = 0.5 * MAX_SPEED
        right_speed = 0.5 * MAX_SPEED

    # 🟢 If no wall → turn right to find wall
    else:
        left_speed = 0.5 * MAX_SPEED
        right_speed = 0.2 * MAX_SPEED

    # Apply speeds
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)