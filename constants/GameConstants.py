import enum
class GameConstants(enum.Enum):
    LANES=3
    
    INITIAL_ENERGY=100
    MAX_ENERGY=100
    
    PROJ_INITIAL_VEL=5
    PROJ_ACELERATION=1.2
    
    ENEMY_VEL=0.3
    VILLAIN_ACTIONS=["enemy", "move", "stop", "good"]
    VILLAIN_INTIAL_ACTION="stop"
    
    VILLAIN_MOVE=[-1, 1]
    ENEMY_MOVE=[-1, 0, 1]
    OBJ_THREAD_TIME=0.002