"""visual_navigation_solution controller."""
from controller import Robot

# Initialize robot and constants
robot = Robot()
MAX_SPEED = 6.28
timestep = int(robot.getBasicTimeStep())

# Red detection thresholds (R, G, B)
RED_THRESHOLD = [0.8, 0.5, 0.5]  # Red >= 0.8, Green/Blue <= 0.5

# Camera setup
camera = robot.getDevice("camera")
camera.enable(timestep)
camera.recognitionEnable(timestep)
camera_width = camera.getWidth()

# Motor setup
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# Centering threshold
CENTER_THRESHOLD = 10  # Pixels


def is_red(color):
    """Check if color is primarily red (high R, low G/B)."""
    return (
        color[0] >= RED_THRESHOLD[0] and  # Strong red component
        color[1] <= RED_THRESHOLD[1] and  # Low green
        color[2] <= RED_THRESHOLD[2]      # Low blue
    )


while robot.step(timestep) != -1:
    red_object = None
    objects = camera.getRecognitionObjects()
    
    print(f"Total detected objects: {len(objects)}")  # Debugging
    
    # Find the reddest object (prioritizing R > G/B)
    for obj in objects:
        obj_color = obj.colors
        print(f"Detected Color - R: {obj_color[0]:.2f}, G: {obj_color[1]:.2f}, B: {obj_color[2]:.2f}")
        
        if is_red(obj_color):
            red_object = obj
            break  # First red object found
    
    # Initialize search behavior
    left_speed = 0.4 * MAX_SPEED    # Rotate clockwise
    right_speed = -0.4 * MAX_SPEED
    
    if red_object:
        print("RED OBJECT DETECTED! Navigating...")
        position_on_image = red_object.getPositionOnImage()[0]
        relative_position = red_object.getPosition()[2]
        print(f"Object position in image: {position_on_image}")
        print(f"Distance from robot: {relative_position:.2f}")
        
        # Center object horizontally with a tolerance
        if abs(position_on_image - camera_width / 2) > CENTER_THRESHOLD:
            if position_on_image < camera_width / 2:
                print("Object is on the left, rotating left")
                left_speed = -0.2 * MAX_SPEED
                right_speed = 0.2 * MAX_SPEED
            else:
                print("Object is on the right, rotating right")
                left_speed = 0.2 * MAX_SPEED
                right_speed = -0.2 * MAX_SPEED
        else:
            # Object is centered. If it's distant, approach it
            if relative_position > 0.01:
                print("Object is frontal, advancing")
                left_speed = 0.5 * MAX_SPEED
                right_speed = 0.5 * MAX_SPEED
            else:
                print("Destination reached")
                left_speed = 0
                right_speed = 0
    else:
        print("No red object found. Searching...")
    
    # Update motors
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
