from random import randint, choice, choices

from scriptred import ActBase




def undomove(n):
        """
        Returns the move that will undo n, helper for move()
        """
        if n == 1:
                return 3
        if n==3:
                return 1
        if n == 2:
                return 4
        if n == 4:
                return 2   
        else:
                return randint(1, 4)

def move(robot, motion=-1): 
        """
        Function to handle moving. Does 2 things:
        1) Smart Random, don't undo the previous move in random
        2) Store the value of previous move in ActBase.last_move
        """

        id = robot.GetInitialSignal()[0:3]
        
        last_m_undo = undomove(ActBase.last_move[id])
        # print(f"For robot {id}, {motion=}")
        if motion == -1:
                list_of_moves = [0, 1, 2, 3, 4]
                list_of_moves.remove(last_m_undo)
                if (robot.investigate_up() == 'wall'):
                        list_of_moves.remove('1') if '1' in list_of_moves else None
                if (robot.investigate_down() == 'wall'):
                        list_of_moves.remove('3') if '3' in list_of_moves else None
                if (robot.investigate_left() == 'wall'):
                        list_of_moves.remove('4') if '4' in list_of_moves else None
                if (robot.investigate_right() == 'wall'):
                        list_of_moves.remove('2') if '2' in list_of_moves else None
                        
                n = choice(list_of_moves)
        else:
                n = motion
        
        ActBase.last_move[id] = n
        return n

        
def move_to(robot, sx, sy):
        """
        Move robot to a particular position sx, sy
        """
        x, y = robot.GetPosition()
        print(f"{x=}, {y=}, {sx=}, {sy=}")
        if x < sx:
                
                return move(robot, 2)
        if x > sx:
                return move(robot, 4)
        if y < sy :
                
                return move(robot, 3)
        if y > sy:
                
                return move(robot, 1)

def spread(robot):
        if(ActBase.timeframe <= 200):
                x, y = robot.GetPosition()
                z, w = ActBase.posofbase
                x, y = x-z, y-w
                if abs(x) > abs(y) and y < 0:
                        return move(robot, 1)
                if abs(x) > abs(y) and y >= 0:
                        return move(robot, 3)
                if abs(x) < abs(y) and x < 0:
                        return move(robot, 4)
                if abs(x) < abs(y) and x >= 0:
                        return move(robot, 2)
                else:
                        return move(robot)
        return move(robot)      

def hilbertmove(robot, quadrant=1):
        x, y = robot.GetPosition()
        z, w = ActBase.posofbase
        # print(z, w)
        if quadrant == 1:
                relative_x, relative_y = x-z, w-y
                listofmoves = [0, 1, 2, 3, 4]
        if quadrant == 3:
                relative_x, relative_y = z-x, y-w
                listofmoves = [0, 3, 4, 1, 2]
        if quadrant == 2:
                relative_x, relative_y = z-x, w-y
                listofmoves = [0, 1, 4, 3, 2]
        if quadrant == 0:
                relative_x, relative_y = x-z, y-w
                listofmoves = [0, 3, 2, 1, 4]
                
        if (relative_x >0 and relative_y>0):
                if (relative_x%2 != 0 and relative_x >= relative_y):
                        return move(robot, listofmoves[3])
                elif (relative_x %2 == 0 and relative_x > relative_y):
                        return move(robot, listofmoves[1])
                elif (relative_y %2 == 0 and relative_x <= relative_y):
                        return move(robot, listofmoves[4])
                elif (relative_y %2 !=0 and relative_x < relative_y):
                        return move(robot, listofmoves[2])
        elif (relative_x == 0 and relative_y%2==0 and relative_y !=0):
                return move(robot, listofmoves[1])
        elif (relative_x == 0 and relative_y%2 !=0):
                return move(robot,listofmoves[2])
        elif (relative_y == 0 and relative_x != 0 and relative_x %2 == 0):
                return move(robot, listofmoves[1])
        elif (relative_y ==0 and relative_x %2 != 0):
                return move(robot, listofmoves[2])
        elif (relative_x == 0 and relative_y == 0):
                return move(robot, listofmoves[1])
        else:
                return move(robot, listofmoves[0])                            


def act_random_robot(robot):
        """
        From the sample script on Notion
        """
        up = robot.investigate_up()
        down = robot.investigate_down()
        left = robot.investigate_left()
        right = robot.investigate_right()
        x,y = robot.GetPosition()
        elixir = robot.GetElixir()
        virus = 500
        # print(elixir)
        robot.setSignal('')
        if up == "enemy" and robot.GetVirus() > 1000:
                robot.DeployVirus(virus)
        elif up == "enemy-base":
                if x < 10:
                        msg_x = '0' + str(x)
                else: 
                        msg_x = str(x)
                if y-1 < 10:
                        msg_y = '0' + str(y-1)
                else:
                        msg_y = str(y-1)
                msg = "base" + msg_x + msg_y
                robot.setSignal(msg)
                if robot.GetVirus() > 500:
                        robot.DeployVirus(500)
        if down == "enemy" and robot.GetVirus() > 1000:
                robot.DeployVirus(virus)
        elif down == "enemy-base":
                
                if x < 10:
                        msg_x = '0' + str(x)
                else: 
                        msg_x = str(x)
                if y+1 < 10:
                        msg_y = '0' + str(y+1)
                else:
                        msg_y = str(y+1)
                msg = "base" + msg_x + msg_y
                robot.setSignal(msg)
                if robot.GetVirus() > 500:
                        robot.DeployVirus(500)
        
        if left == "enemy" and robot.GetVirus() > 1000:
                robot.DeployVirus(virus)
        elif left == "enemy-base":
                if x - 1 < 10:
                        msg_x = '0' + str(x-1)
                else: 
                        msg_x = str(x-1)
                if y < 10:
                        msg_y = '0' + str(y)
                else:
                        msg_y = str(y)
                msg = "base" + msg_x + msg_y
                robot.setSignal(msg)
                if robot.GetVirus() > 500:
                        robot.DeployVirus(500)
                
        if right == "enemy" and robot.GetVirus() > 1000:
                robot.DeployVirus(virus)
        elif right == "enemy-base":
                x,y = robot.GetPosition()
                if x+1 < 10:
                        msg_x = '0' + str(x+1)
                else: 
                        msg_x = str(x+1)
                if y < 10:
                        msg_y = '0' + str(y)
                else:
                        msg_y = str(y)
                msg = "base" + msg_x + msg_y
                robot.setSignal(msg)
                if robot.GetVirus() > 500:
                        robot.DeployVirus(500)
        

        
        
        if len(robot.GetCurrentBaseSignal()) > 0:
                s = robot.GetCurrentBaseSignal()[4:]
                sx = int(s[0:2])
                sy = int(s[2:4])
                dist = abs(sx-x) + abs(sy-y)
                if dist==1:
                        robot.DeployVirus(robot.GetVirus()*0.75)
                        return 0
                if x < sx:
                        return 2
                if x > sx:
                        return 4
                if y < sy :
                        return 3
                if y > sy:
                        return 1
        else:
                return move(robot)    

def give_instruction_wall(n):
    """
    Gives instructions to each of the wall's robots for first few timeframes
    """
    if (n == 1):
        return [2,2,0,0]
    if (n ==2):
        return [2,2,1,0]
    if (n == 3):
        return [2,2,1,1]
    if (n == 4):
        return [1,1,2,0]
    if (n == 5):
        return [1,1,0,0]
    if (n == 6):
        return [1,1,4,0]
    if (n == 7):
        return [1,1,4,4]
    if (n == 8):
        return [4,4,1,0]
    if (n == 9):
        return [4,4,0,0]
    if (n == 10):
        return [4,4,3,0]
    if (n == 11):
        return [4,4,3,3]
    if (n == 12):
        return [3,3,4,0]
    if (n == 13):
        return [3,3,0,0]
    if (n == 14):
        return [3,3,2,0]
    if (n == 15):
        return [3,3,2,2]
    if (n == 16):
        return [2,2,3,0]
    return []

def give_instruction_es(n):
    if (n == 1):
        return [2,]*6
    if (n == 2):
        return [4,]*6
    if (n == 3):
        return [1,1,2,2,1,1]
    if (n == 4):
        return [1,1,4,4,1,1]
    if (n == 5):
        return [3,3,4,4,3,3]
    if (n == 6):
        return [3,3,2,2,3,3]


def ActRobot(robot):
    role=robot.GetInitialSignal()[0]
    timeframe = ActBase.timeframe
    up = robot.investigate_up()
    down = robot.investigate_down()
    left = robot.investigate_left()
    right = robot.investigate_right()
    x,y = robot.GetPosition()
    robot.setSignal('')
    basex, basey = ActBase.posofbase
    cx,cy=ActBase.cx,ActBase.cy
    
    wall_virus = 800
    if up == "enemy" and robot.GetVirus() > 1000:
        robot.DeployVirus(wall_virus)
    elif up == "enemy-base":
        if x < 10:
            msg_x = '0' + str(x)
        else: 
            msg_x = str(x)
        if y-1 < 10:
            msg_y = '0' + str(y-1)
        else:
            msg_y = str(y-1)
        msg = "base" + msg_x + msg_y
        robot.setSignal(msg)
        if robot.GetVirus() > 500:
            robot.DeployVirus(wall_virus)
    if down == "enemy" and robot.GetVirus() > 1000:
            robot.DeployVirus(wall_virus)
    elif down == "enemy-base":
            
            if x < 10:
                    msg_x = '0' + str(x)
            else: 
                    msg_x = str(x)
            if y+1 < 10:
                    msg_y = '0' + str(y+1)
            else:
                    msg_y = str(y+1)
            msg = "base" + msg_x + msg_y
            robot.setSignal(msg)
            if robot.GetVirus() > 500:
                    robot.DeployVirus(wall_virus)
    
    if left == "enemy" and robot.GetVirus() > 1000:
            robot.DeployVirus(wall_virus)
    elif left == "enemy-base":
            if x - 1 < 10:
                    msg_x = '0' + str(x-1)
            else: 
                    msg_x = str(x-1)
            if y < 10:
                    msg_y = '0' + str(y)
            else:
                    msg_y = str(y)
            msg = "base" + msg_x + msg_y
            robot.setSignal(msg)
            if robot.GetVirus() > 500:
                    robot.DeployVirus(wall_virus)
            
    if right == "enemy" and robot.GetVirus() > 1000:
            robot.DeployVirus(wall_virus)
    elif right == "enemy-base":
            x,y = robot.GetPosition()
            if x+1 < 10:
                    msg_x = '0' + str(x+1)
            else: 
                    msg_x = str(x+1)
            if y < 10:
                    msg_y = '0' + str(y)
            else:
                    msg_y = str(y)
            msg = "base" + msg_x + msg_y
            robot.setSignal(msg)
            if robot.GetVirus() > 500:
                    robot.DeployVirus(wall_virus)

    if(role == 'W'):
        n = int(robot.GetInitialSignal()[1:3]) 
        instructions = give_instruction_wall(n)
        if (timeframe <= len(instructions)-1) :
            return move(robot, instructions[timeframe])
        elif(timeframe <= 120):
                return hilbertmove(robot,n%4)
        elif(timeframe <= 145): 
            return move_to(robot, basex, basey)
        elif(timeframe - 145 <= len(instructions)):
             return move(robot, instructions[timeframe - 146])
        else:
                return move(robot, 0)            

    if(role == 'C' and int(robot.GetInitialSignal()[2]) in range(3)):
        # print('c')
        x,y = robot.GetPosition()
        z,w = ActBase.posofbase
        # print(y)
        if (abs(x-z) + abs(y-w) < 25 and x > 19 and x < 39 and y > 19 and y < 39):    
                return spread(robot)
        return move(robot)            
        
    if(role == 'C' and int(robot.GetInitialSignal()[2]) in range(3, 6)):
        x,y = robot.GetPosition()
        z,w = ActBase.posofbase
        if (abs(x-z) + abs(y-w) < 25 and x > 19 and x < 39 and y > 0 and y < 19):
                return spread(robot)
        return move(robot)
        
#     if timeframe==0:
#             robot.setSignal(robot.GetInitialSignal())
    if(role == 'E'):
        id = robot.GetInitialSignal()[0:3]
        n = ActBase.Emotion[id]
        instructions = give_instruction_es(n)
        
        if x<=5:
            ActBase.Emotion[id] = 3 
        elif y<=5 :
            ActBase.Emotion[id] = 6
        elif y>=cy-5 :
            ActBase.Emotion[id] = 4
        elif x>=cx-5 :
            ActBase.Emotion[id] = 5
        return move(robot, choices([instructions[timeframe%6], 1, 2, 3, 4], weights=[9,0.25, 0.25, 0.25, 0.25])[0])


    return move(robot)
            

def ActBase(base):
    '''
    Add your code here
    
    '''
    ActBase.timeframe+=1
#     print(ActBase.timeframe)
    #Dimensions of Canvas
    if ActBase.timeframe==0:
        ActBase.cx,ActBase.cy=base.GetDimensionX(),base.GetDimensionY()
        ActBase.posofbase = base.GetPosition()

    # Wall

    if (ActBase.timeframe == 0): 
        for i in range(1, 10):
            base.create_robot(f'W0{i}')    
            ActBase.last_move[f'W0{i}'] = randint(0,4)   
        for i in range(10, 17):
            base.create_robot(f'W{i}')
            ActBase.last_move[f'W{i}'] = randint(0,4) 
#     # Collect Resource
    if (ActBase.timeframe == 0):
        for i in range(3):
                base.create_robot(f'C0{i}')
                ActBase.last_move[f'C0{i}'] = randint(0,4) 
        for i in range(3, 6):
                base.create_robot(f'C0{i}')            
                ActBase.last_move[f'C0{i}'] = randint(0,4) 

#     Enemy Scout
    if (ActBase.timeframe == 0): 
        for i in range(1, 7):
            base.create_robot(f'E0{i}')    
            ActBase.last_move[f'E0{i}'] = randint(0,4)  
            ActBase.Emotion[f'E0{i}'] = i

    # print(base.GetPosition())

    L = base.GetListOfSignals()
    for l in L:
        if len(l) > 0:
                base.SetYourSignal(l)
                return
    return

ActBase.timeframe=-1
ActBase.last_move = {}
ActBase.posofbase = (29, 19)
ActBase.Emotion = {}