SIZE = [1080, 720]
NAME = "Empty Pygame Project"
FPS = 0  # 0 - unlimited
COLORS = {
    "background": (223, 223, 203),
    "text": (0, 0, 0),
    "scale": (0, 0, 0),
}

# Camera
CAMERA_START_X = 0
CAMERA_START_Y = 0
CAMERA_START_DISTANCE = 10
CAMERA_MOVE_SPEED = 1
CAMERA_ZOOM_SPEED = 1

# Player
PLAYER_START_X = 0
PLAYER_START_Y = 0
PLAYER_MOVE_SPEED = 4  # Meters per second
PLAYER_SIZE = 2  # Width and height (in meters)
PLAYER_INTERPOLATION_SPEED = 15  # How fast the drawn position catches up to the server position

# Map scale (UI)
SCALE_MIN_PIXELS = 50
SCALE_MAX_PIXELS = 200
SCALE_FIRST_DIGITAL = (1, 2, 5)
SCALE_OFFSET = (60, 10)
SCALE_STICK_WIDTH = 5
SCALE_LINE_WIDTH = 2
SCALE_LABEL_OFFSET = (30, 0)

# HUD
HUD_FONT_SIZE = 20
HUD_SCALE_OFFSET = (140, 15)
HUD_FPS_MARGIN = (70, 21)

# Networking
NET_HOST = "127.0.0.1"
NET_PORT = 5000
NET_BUFFER_SIZE = 4096

