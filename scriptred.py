from random import randint

# t = 0

def ActRobot(robot):
        up = robot.investigate_up()
        down = robot.investigate_down()
        left = robot.investigate_left()
        right = robot.investigate_right()
        x,y = robot.GetPosition()
        elixir = robot.GetElixir()
        # print(elixir)
        robot.setSignal('')
        if up == "enemy" and robot.GetVirus() > 1000:
                robot.DeployVirus(100)
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
                robot.DeployVirus(100)
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
                robot.DeployVirus(100)
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
                robot.DeployVirus(100)
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
                return randint(1,4)
        

def ActBase(base):
    '''
    Add your code here
    
    '''
#     t += 1
    up = base.investigate_up()
    down = base.investigate_down()
    left = base.investigate_left()
    right = base.investigate_right()
    nw=base.investigate_nw()
    ne=base.investigate_ne()
    sw=base.investigate_sw()
    se=base.investigate_se()
    while base.GetElixir() > 500:
        base.create_robot('')
        # print(base.GetElixir())
#     if  'enemy' in [up,down,left,right,nw,ne,sw,se]:
#             base.DeployVirus(1000)
    L = base.GetListOfSignals()
    for l in L:
        if len(l) > 0:
                base.SetYourSignal(l)
                return


    