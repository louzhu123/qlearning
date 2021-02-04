import pandas as pd
import numpy as np
import time
import os

np.random.seed(2)

class people:
        def __init__(self,order):
                self.order = order

        def get_action(self,environment):
                while True:
                        try:
                                action = eval(input('请输入1-9（第一行 1-3，第二行 4-6，第三行7-9）, 按0退出游戏\n'))
                        except:
                                continue
                        if action == 0 :
                                os._exit(0)

                        action -= 1
                        if environment.at[action // 3,action % 3] == 0:
                                return action
                        else:
                                print("位置",action+1,"不可选")
                
class robot:
        def __init__(self,order):
                q_table = pd.read_csv("q_table.csv")
                q_table.columns = [0,1,2,3,4,5,6,7,8] # 因为读取出来的列为字符，所以重新设置
                self.order = order 
                self.q_table = q_table

        def get_action(self,environment):
                state = get_state(environment)
                state_actions = self.q_table.iloc[state,:]
                for i in range(9):
                        if environment.at[i // 3,i % 3] != 0:
                                state_actions.pop(i)
                action = state_actions.idxmax() # 返回最大价值动作的索引
                return action

def round(environment,player):
        result = get_result(environment,player.order,player.get_action(environment))
        os.system('cls')

        visual = pd.DataFrame([['','',''],['','',''],['','','']])
        for i in range(3):
                for j in range(3):
                        value = environment.iloc[i,j]
                        if value == 0:
                                visual.iloc[i,j] = ' '
                        elif value == 1:
                                visual.iloc[i,j] = '√'
                        else:
                                visual.iloc[i,j] = 'x'
        print(visual)
        time.sleep(1)
        return result

def play(player1,player2):
        environment = pd.DataFrame(np.zeros((3,3)))   
        print(pd.DataFrame([['','',''],['','',''],['','','']]))

        round(environment,player1)
        while True:
                result = round(environment,player2)
                if result != "continue":
                        break
                result = round(environment,player1)
                if result != "continue":
                        break
        print("游戏结束")
        return result

def robot_robot():
        play(robot(1),robot(2))

def people_robot():
        if np.random.uniform() > 0.5:
                play(people(1),robot(2))
        else:
                play(robot(1),people(2))
        play(people(1),robot(2))

def get_state(environment): # 返回十进制状态
        state = 0
        i = 8
        for row in range(3):
                for col in range(3):
                        state += environment.iloc[row,col] * (3 ** i)
                        i -= 1
        return int(state)

def get_result(environment,player,action):
        # 改变环境
        i = 0
        for row in range(3):
                for col in range(3):
                        if i == action:
                                environment.iloc[row,col] = player
                        i += 1
        # 判断结果

        # player胜利
        for row in range(3):         # 横三个
                first = environment.iloc[row,0]
                if first != 0 and environment.iloc[row,1] == first and environment.iloc[row,2] == first:
                        return "win"
        for col in range(3):         # 纵三个
                first = environment.iloc[0,col]
                if first != 0 and environment.iloc[1,col] == first and environment.iloc[2,col] == first:
                        return "win"   
        first = environment.iloc[0,0] # 斜三个
        if first != 0 and environment.iloc[1,1] == first and environment.iloc[2,2] == first:
                return "win"
        first = environment.iloc[0,2]
        if first != 0 and environment.iloc[1,1] == first and environment.iloc[2,0] == first:
                return "win"

        # 游戏继续
        for row in range(3):
                for col in range(3):
                        if environment.iloc[row,col] == 0:
                                return "continue"

        # 平局
        return "draw"

if __name__ == "__main__":

    while True:
        people_robot()
        #robot_robot()  # 因为机器只会按照价最大值的动作去执行，所以会一直重复