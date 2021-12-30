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
        
        # print(n)
        ActBase.last_move[id] = n
        return n

        
def move_to(robot, sx, sy):
        """
        Move robot to a particular position sx, sy
        """
        x, y = robot.GetPosition()
        # print(f"{x=}, {y=}, {sx=}, {sy=}")

        if x < sx:
                return move(robot, 2)
        if x > sx:
                return move(robot, 4)
        if y < sy :
                
                return move(robot, 3)
        if y > sy:
                
                return move(robot, 1)

def protect_home(robot):
        
        return move_to(robot, ActBase.posofbase[0], ActBase.posofbase[1])

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
        
        if (relative_x > 0 and relative_y > 0):
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
                print(f"{relative_x=}, {relative_y=}")
                print(robot.GetInitialSignal())
                print(f"{x=} {y=}")
                print(f"{z=} {w=}")
                return move(robot, listofmoves[0])    # TODO: Change later                        

def give_instruction_wall(robot):
    """
    Gives instructions to each of the wall's robots to build wall
    """
    n = int(robot.GetInitialSignal()[1:3]) 
    if (n == 1):
        return [1,1,1,0]
    if (n == 2):
        return [4,4,4,0]
    if (n == 3):
        return [3,3,3,0]
    if (n == 4):
        return [2,2,2,0]
    if (n == 5):
        return [1,1,2,2]
    if (n == 6):
        return [4,4,1,1]
    if (n == 7):
        return [3,3,4,4]
    if (n == 8):
        return [2,2,3,3]
#     if (n == 9):
#         return [4,4,0,0]
#     if (n == 10):
#         return [4,4,3,0]
#     if (n == 11):
#         return [4,4,3,3]
#     if (n == 12):
#         return [3,3,4,0]
#     if (n == 13):
#         return [3,3,0,0]
#     if (n == 14):
#         return [3,3,2,0]
#     if (n == 15):
#         return [3,3,2,2]
#     if (n == 16):
#         return [2,2,3,0]
    return []

def give_instruction_sidewall(n):
    if (n == 1):
        return [2,]*2
    if (n == 2):
        return [4,]*2
    if (n == 3):
        return [1,2]
    if (n == 4):
        return [1,4]
    if (n == 5):
        return [3,4]
    if (n == 6):
        return [3,2]

def give_instruction_es(n):
    if (n == 1):
        return [2,]*2
    if (n == 2):
        return [4,]*2
    if (n == 3):
        return [1,2]
    if (n == 4):
        return [1,4]
    if (n == 5):
        return [3,4]
    if (n == 6):
        return [3,2]
    if (n == 7):
        return [3,]*2
    if (n == 8):
        return [1,]*2



def reach_enemy_base(robot):
        base_sig = robot.GetCurrentBaseSignal()
        x, y = robot.GetPosition()
        # print(robot.GetVirus())
        if robot.GetVirus() < 100:
                move(robot)
        if len(base_sig)>4:
                if base_sig[0:4] == 'base':
                        s = base_sig[4:]

                        sx = int(s[0:2])
                        sy = int(s[2:4])
                        # print(f"{sx=} {sy=}")
                        dist = abs(sx-x) + abs(sy-y)
                        if dist == 1:
                                robot.DeployVirus(robot.GetVirus()*0.75)
                        #         return move(robot, 0)
                        return move_to(robot, sx, sy)


def ActRobot(robot):
    role=robot.GetInitialSignal()[0]
#     print(role)
    timeframe = ActBase.timeframe
    up = robot.investigate_up()
    down = robot.investigate_down()
    left = robot.investigate_left()
    right = robot.investigate_right()
    nw=robot.investigate_nw()
    ne=robot.investigate_ne()
    sw=robot.investigate_sw()
    se=robot.investigate_se()
    x,y = robot.GetPosition()
    robot.setSignal('')
    basex, basey = ActBase.posofbase
    cx,cy=ActBase.cx,ActBase.cy
    bcord=ActBase.bcord
    base_sig = robot.GetCurrentBaseSignal() 
    enemy_found = False
    base_attacked = False
    if len(base_sig)>4:
            if base_sig[0:4] == 'base':
                    enemy_found = True
            if len(base_sig) == 9 and base_sig[8] == 'H':
                    base_attacked = True
                #     print("Base Attacked")
    if (role=='C'):
        if base_attacked:
                return protect_home(robot)        
    if role == 'W':
        virus = 800
    else:
        virus = 500
    virus = min(virus, robot.GetVirus())
    if timeframe>200:
        if robot.GetVirus() < 100:
                return move(robot)
        
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
            robot.DeployVirus(virus)
            
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
                    robot.DeployVirus(virus)
    
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
                    robot.DeployVirus(virus)
            
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
                    robot.DeployVirus(virus)

    if nw == "enemy" and robot.GetVirus() > 1000:
        robot.DeployVirus(virus)
    elif nw == "enemy-base":
        if x-1 < 10:
            msg_x = '0' + str(x-1)
        else: 
            msg_x = str(x-1)
        if y-1 < 10:
            msg_y = '0' + str(y-1)
        else:
            msg_y = str(y-1)
        msg = "base" + msg_x + msg_y
        robot.setSignal(msg)
        if robot.GetVirus() > 500:
            robot.DeployVirus(virus)

    if ne == "enemy" and robot.GetVirus() > 1000:
        robot.DeployVirus(virus)
    elif ne == "enemy-base":
        if x+1 < 10:
            msg_x = '0' + str(x+1)
        else: 
            msg_x = str(x+1)
        if y-1 < 10:
            msg_y = '0' + str(y-1)
        else:
            msg_y = str(y-1)
        msg = "base" + msg_x + msg_y
        robot.setSignal(msg)
        if robot.GetVirus() > 500:
            robot.DeployVirus(virus)

    if se == "enemy" and robot.GetVirus() > 1000:
        robot.DeployVirus(virus)
    elif se == "enemy-base":
        if x+1 < 10:
            msg_x = '0' + str(x+1)
        else: 
            msg_x = str(x+1)
        if y+1 < 10:
            msg_y = '0' + str(y+1)
        else:
            msg_y = str(y+1)
        msg = "base" + msg_x + msg_y
        robot.setSignal(msg)
        if robot.GetVirus() > 500:
            robot.DeployVirus(virus)

    if sw == "enemy" and robot.GetVirus() > 1000:
        robot.DeployVirus(virus)
    elif sw == "enemy-base":
        if x-1 < 10:
            msg_x = '0' + str(x-1)
        else: 
            msg_x = str(x-1)
        if y+1 < 10:
            msg_y = '0' + str(y+1)
        else:
            msg_y = str(y+1)
        msg = "base" + msg_x + msg_y
        robot.setSignal(msg)
        if robot.GetVirus() > 500:
            robot.DeployVirus(virus)

    if(role == 'W'):
        if enemy_found and not base_attacked:
            return reach_enemy_base(robot)
        
        n = int(robot.GetInitialSignal()[1:3]) 
        
        instructions = give_instruction_wall(robot)
        if (timeframe <= len(instructions)-1) :
            return move(robot, instructions[timeframe])
        elif(timeframe <= 120):
                return hilbertmove(robot,n%4)
        elif(timeframe <= 145): 
            return move_to(robot, basex, basey)
        elif(timeframe - 145 <= len(instructions)):
             return move(robot, instructions[timeframe - 146])
        elif(timeframe == 146 + len(instructions)):
                return move(robot, 4)
        else:
             list_of_moves=[1,2,2,3,3,4,4,1]
             return move(robot, list_of_moves[(timeframe-146 - len(instructions) - 1)%8])  

      

    if(role == 'C' and int(robot.GetInitialSignal()[2]) in range(3)):

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
        if enemy_found:
            return reach_enemy_base(robot)
        id = robot.GetInitialSignal()[0:3]
        n = ActBase.Emotion[id]
        instructions = give_instruction_es(n)
        if bcord[0]>cx/2:
                if x<=5:
                        ActBase.Emotion[id] = 3 
                elif y<=5 :
                        ActBase.Emotion[id] = 6
                elif y>=cy-5 :
                        ActBase.Emotion[id] = 4
                elif x>=cx-5 :
                        ActBase.Emotion[id] = 5
        
        else:
                if x<=5:
                        ActBase.Emotion[id] = 3 
                elif y<=5 :
                        ActBase.Emotion[id] = 6
                elif y>=cy-5 :
                        ActBase.Emotion[id] = 4
                elif x>=cx-5 :
                        ActBase.Emotion[id] = 5
        # TODO: Fine tune
        return move(robot, choices([instructions[timeframe%2], 1, 2, 3, 4], weights=[5,0.25, 0.25, 0.25, 0.25])[0]) 

    return move(robot)
            

def ActBase(base):
    '''
    Add your code here

    '''
    ActBase.timeframe+=1

    up = base.investigate_up()
    down = base.investigate_down()
    left = base.investigate_left()
    right = base.investigate_right()
    nw=base.investigate_nw()
    ne=base.investigate_ne()
    sw=base.investigate_sw()
    se=base.investigate_se()

    # which robots are made
    wall = True
    enemy_scout = True
    resource = True
    sidewall = False

    # Kill enemies if they are near
    if  'enemy' in [up,down,left,right,nw,ne,sw,se]:
            l = base.GetYourSignal() 
            if l == '':
                base.SetYourSignal("XXXXXXXXH")
            elif len(l) == 8:
                if l[0:4] == 'base':
                        base.SetYourSignal(l+'H')
            # TODO: Edit if you make a new signal
            base.DeployVirus(min(1000, base.GetVirus()))

    #print(ActBase.timeframe)

    #Dimensions of Canvas
    if ActBase.timeframe==0:
        ActBase.cx,ActBase.cy=base.GetDimensionX(),base.GetDimensionY()
        ActBase.posofbase = base.GetPosition()
        ActBase.bcord=base.GetPosition()

    # Wall
    if (ActBase.timeframe == 0) and wall: 
        
        for i in range(1, 9):
            base.create_robot(f'W0{i}')    
            ActBase.last_move[f'W0{i}'] = randint(0,4)   
        # for i in range(10, 17):
        #     base.create_robot(f'W{i}')
        #     ActBase.last_move[f'W{i}'] = randint(0,4) 


#     Collect Resource
    if (ActBase.timeframe == 0) and resource:
        for i in range(3):
                base.create_robot(f'C0{i}')
                ActBase.last_move[f'C0{i}'] = randint(0,4) 
        for i in range(3, 6):
                base.create_robot(f'C0{i}')            
                ActBase.last_move[f'C0{i}'] = randint(0,4) 

#     Enemy Scout
    if (ActBase.timeframe == 0) and enemy_scout: 
        for i in range(1, 9):
            base.create_robot(f'E0{i}')    
            ActBase.last_move[f'E0{i}'] = randint(0,4)  
            ActBase.Emotion[f'E0{i}'] = i

#     Sidewall
    if (ActBase.timeframe == 0) and sidewall: 
        for i in range(1, 7):
            base.create_robot(f'S0{i}')    
            ActBase.last_move[f'S0{i}'] = randint(0,4)  


    # check if a robot found enemy base
    L = base.GetListOfSignals()
    for l in L:
        if len(l) > 4:
                if(l[0:4] == 'base'):
                        bs = base.GetYourSignal()
                        if len(bs) == 0:
                                base.SetYourSignal(l)
                        elif len(bs) == 9 and bs[8] == 'H':
                                base.SetYourSignal(l+'H')
                return
    return

ActBase.timeframe=-1
ActBase.last_move = {}
ActBase.posofbase = (29, 19) # Is reset above
ActBase.Emotion = {}
