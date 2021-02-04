import pandas as pd
import numpy as np
import env
import time

np.random.seed(2)

ALPHA = 0.1 # 学习效率 
LAMBDA = 0.9 # 衰减值
PROBABILITY = 0.1 # 随机概率
MAX_EPISODES = 10000 # 训练次数

def build_q_table():
        q_table = pd.DataFrame(
                np.zeros((3**9,9))
        )
        return q_table

def choose_action(state,q_table,environment):
        state_actions = q_table.iloc[state,:]
        for i in range(9):
                if environment.at[i // 3,i % 3] != 0: # 去掉不可选的动作
                        state_actions.pop(i)

        if len(state_actions[state_actions==0]) > 0:
                action = int(np.random.choice(state_actions[state_actions==0].index)) # 每个没操作过动作都尝试一下
        elif(np.random.uniform()<PROBABILITY): 
                action = int(np.random.choice(state_actions.index)) # 随机选择action里面的动作
        else:  
                action = state_actions.idxmax() # 返回最大价值动作的索引

        return action

def rl(q_table):

        for episode in range(MAX_EPISODES):
                
                print("episode",episode)
                environment = pd.DataFrame(np.zeros((3,3)))
                result = "continue"

                # 玩家1操作
                state1 = env.get_state(environment)
                action1 = choose_action(state1,q_table,environment)
                env.get_result(environment,1,action1)

                while True:
                        # 玩家2操作
                        state2 = env.get_state(environment) 
                        action2 = choose_action(state2,q_table,environment)
                        result = env.get_result(environment,2,action2)
                        state1_ = env.get_state(environment) # 玩家2完成动作后，就是玩家1的转移后的状态
                        if result == 'win':
                                R1,R2 = -1,1
                                q_table.loc[state1,action1] += ALPHA * (R1 + LAMBDA*q_table.iloc[state1_,:].max() - q_table.loc[state1,action1])
                                q_table.loc[state2,action2] += ALPHA * (R2 - q_table.loc[state2,action2])
                                break
                        elif result == 'continue':
                                R1 = 0
                                q_table.loc[state1,action1] += ALPHA * (R1 + LAMBDA*q_table.iloc[state1_,:].max() - q_table.loc[state1,action1])
                        else:
                                R1,R2 = 0.1,0.1
                                q_table.loc[state1,action1] += ALPHA * (R1 + LAMBDA*q_table.iloc[state1_,:].max() - q_table.loc[state1,action1])
                                q_table.loc[state2,action2] += ALPHA * (R2 - q_table.loc[state2,action2])
                                break

                        # 玩家1操作
                        state1 = env.get_state(environment)
                        action1 = choose_action(state1,q_table,environment)
                        result = env.get_result(environment,1,action1)
                        state2_ = env.get_state(environment)
                        if result == 'win': 
                                R1,R2 = 1,-1
                                q_table.loc[state2,action2] += ALPHA * (R2 + LAMBDA*q_table.iloc[state2_,:].max() - q_table.loc[state2,action2])
                                q_table.loc[state1,action1] += ALPHA * (R1 - q_table.loc[state1,action1])
                                break
                        elif result == 'continue':
                                R2 = 0
                                q_table.loc[state2,action2] += ALPHA * (R2 + LAMBDA*q_table.iloc[state2_,:].max() - q_table.loc[state2,action2])
                        else:
                                R1,R2 = 0.1,0.1
                                q_table.loc[state2,action2] += ALPHA * (R2 + LAMBDA*q_table.iloc[state2_,:].max() - q_table.loc[state2,action2])
                                q_table.loc[state1,action1] += ALPHA * (R1 - q_table.loc[state1,action1])
                                break
        return q_table

if __name__ == "__main__":
        try:
                q_table = pd.read_csv("q_table.csv")
                q_table.columns = [0,1,2,3,4,5,6,7,8] # 因为读取出来的列为字符，所以重新设置
        except:
                q_table = build_q_table()
                q_table.to_csv("q_table.csv",header=True, index=False)
        
        q_table = rl(q_table)
        q_table.to_csv("q_table.csv",header=True, index=False)
