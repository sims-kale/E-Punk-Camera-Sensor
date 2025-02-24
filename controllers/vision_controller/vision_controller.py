"""visual_navigation_solution controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()

MAX_SPEED = 6.28

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

# Sensors

camera = robot.getDevice("camera")
camera.enable(timestep)
camera.recognitionEnable(timestep)

camera_width = camera.getWidth()

# Actuators

leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)


# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()
    
    objects = camera.getRecognitionObjects()

    # Process sensor data here.

    if len(objects) == 0:
        print("No object found. Searching...")
        leftSpeed = 0.2 * MAX_SPEED
        rightSpeed = -0.2 * MAX_SPEED
    else:
        print("Found the object")
        object = objects[0]
        position_on_image = object.getPositionOnImage()
        relative_position = object.getPosition()
        
        # If the object is not in the middle of the screen...
        if position_on_image[0] != camera_width / 2:
            # ... turn either left or right to center it
            if position_on_image[0] < camera_width / 2:
                print("Object is on the left, rotating left")
                leftSpeed = -0.2 * MAX_SPEED
                rightSpeed = 0.2 * MAX_SPEED
            elif position_on_image[0] > camera_width / 2:
                print("Object is on the right, rotating right")
                leftSpeed = 0.2 * MAX_SPEED
                rightSpeed = -0.2 * MAX_SPEED
        else:
             # Object is central. If it's distant, approach it
            if relative_position[0] > 0.1:
                print("Object is frontal, advancing")
                leftSpeed = 0.5 * MAX_SPEED
                rightSpeed = 0.5 * MAX_SPEED
            else:
                print("Destination reached")
                leftSpeed = 0
                rightSpeed = 0

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)

# Enter here exit cleanup code.
