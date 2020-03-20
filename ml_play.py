"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False
    ball_x_keep = 100
    ball_y_keep = 400

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
        else:
            # 取得兩組球的x, y值
            ball_x, ball_y = scene_info.ball
            plat_x, plat_y = scene_info.platform
            m = (ball_y - ball_y_keep)/(ball_x - ball_x_keep)
            # 相減得到向量
            if ball_y - ball_y_keep > 0: # 球往下
                if ball_x - ball_x_keep > 0: # 球往右

                    if ball_x - (ball_y - 400)/m > 200: # 會碰到右邊
                        boundR = ball_y - m*(ball_x - 200)
                        m2 = -m
                        plat_x_next = 200 - (boundR - 400)/m2
                        if plat_x + 25 - plat_x_next > 15:
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                        elif plat_x + 25 - plat_x_next < -15:
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                        else:
                            comm.send_instruction(scene_info.frame, PlatformAction.NONE)

                    else: #不會碰到右邊
                        plat_x_next = ball_x - (ball_y - 400)/m
                        if plat_x + 25 - plat_x_next > 15:
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                        elif plat_x + 25 - plat_x_next < -15:
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                        else:
                            comm.send_instruction(scene_info.frame, PlatformAction.NONE)

                elif ball_x - ball_x_keep < 0: # 球往左

                    if ball_x - (ball_y - 400)/m < 0: # 會碰到左邊
                        boundL = ball_y - m*(ball_x)
                        m2 = -m
                        plat_x_next =  - (boundL - 400)/m2
                        if plat_x + 25 - plat_x_next > 15:
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                        elif plat_x + 25 - plat_x_next < -15:
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                        else:
                            comm.send_instruction(scene_info.frame, PlatformAction.NONE)

                    else: #不會碰到左邊
                        plat_x_next =  ball_x - (ball_y - 400)/m
                        if plat_x + 25 - plat_x_next > 15:
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                        elif plat_x + 25 - plat_x_next < -15:
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                        else:
                            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                
                else: # 垂直往下
                    if plat_x + 25 - ball_x > 15:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif plat_x + 25 - ball_x < -15:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    else:
                        comm.send_instruction(scene_info.frame, PlatformAction.NONE)

            ball_x_keep = ball_x
            ball_y_keep = ball_y
            
