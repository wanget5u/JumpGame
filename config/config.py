# [RESOULTION / WINDOW RELATED]
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
ASPECT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT
FULLSCREEN = False

# [UI ELEMENTS]
BACKGROUND_COLOR = ( 43,45,48 )
BACKGROUND_PAUSE_COLOR = ( 33, 35, 38, 128)
BUTTON_COLOR = ( 67,69,74 )
TEXT_COLOR = ( 255,255,255 )
SLIDER_COLOR = ( 200,200,200 )
FONT_SIZE = 48
LEVEL_LOAD_BUTTON_WIDTH = 240
LEVEL_LOAD_BUTTON_HEIGHT = 120
PADDING = 40
LEVELS_PER_PAGE = 6
ATTEMPT_LABEL_X_OFFSET = 400

END_WALL_OUTER_COLOR = ( 64,64,64 )
END_WALL_INNER_COLOR = ( 24,24,24 )
END_WALL_OUTER_WIDTH = 5

FLOOR_OUTER_COLOR = ( 64,64,64 )
FLOOR_INNER_COLOR = ( 24,24,24 )
FLOOR_OUTER_HEIGHT = 5

# [PLAYER VARIABLES]
PLAYER_INNER_COLOR = ( 255,255,255 )
PLAYER_OUTER_COLOR = ( 145,145,145 )
PLAYER_OUTER_SIZE = 60
PLAYER_INNER_SIZE = PLAYER_OUTER_SIZE - 15

# [GAME VARIABLES]
PLAYER_SPEED = 500
PLAYER_START_X = 120
LEVEL_BEGIN_X = 120
MIN_LEVEL_LENGTH = 1020
END_WALL_X = 480

FLOOR_Y = 720

RENDER_MARGIN = 100

# [GAME OBJECTS COLORS]
BLOCK_OUTER_COLOR = ( 64,64,64 )
BLOCK_INNER_COLOR = ( 44,44,44 )
BLOCK_OUTER_SIZE = PLAYER_OUTER_SIZE
BLOCK_INNER_SIZE = BLOCK_OUTER_SIZE - 5

SPIKE_OUTER_COLOR = ( 64,64,64 )
SPIKE_INNER_COLOR = ( 44,44,44 )

SPIKE_OUTER_WIDTH = BLOCK_OUTER_SIZE
SPIKE_OUTER_HEIGHT = BLOCK_OUTER_SIZE
SPIKE_INNER_WIDTH = SPIKE_OUTER_WIDTH - 5
SPIKE_INNER_HEIGHT = SPIKE_OUTER_HEIGHT - 5

ORB_OUTER_COLOR = ( 255,255,255 )
ORB_INNER_COLOR = ( 230,205,0 )
ORB_OUTER_DIAMETER = BLOCK_OUTER_SIZE - 8
ORB_INNER_DIAMETER = BLOCK_OUTER_SIZE - 28

PAD_OUTER_COLOR = ORB_OUTER_COLOR
PAD_INNER_COLOR = ORB_INNER_COLOR
PAD_OUTER_WIDTH = BLOCK_OUTER_SIZE - 4
PAD_OUTER_HEIGHT = BLOCK_OUTER_SIZE // 5
PAD_INNER_WIDTH = PAD_OUTER_WIDTH - 4
PAD_INNER_HEIGHT = PAD_OUTER_HEIGHT - 4

# [EDITOR VAR]
GRID_SIZE = PLAYER_OUTER_SIZE
TOOLBAR_HEIGHT = SCREEN_HEIGHT - FLOOR_Y
TOOLBAR_COLOR = ( 80,80,80 )
GRID_COLOR = ( 130,130,130,50 )
GRID_START_LINE_COLOR = ( 200,200,200 )
HIGHLIGHT_COLOR = ( 255,255,255 )
MAX_SLIDER_X = 2520
SLIDER_MARGIN = 180