import itertools
from tabulate import tabulate
import pandas as pd
#states = [1, 2, 3, 4]
#reward_arr = [10, -1, 0, 1]
#terminal_state = [1, 4]
states = [1, 2, 3, 4, 5, 6]
reward_arr = [10, 0, 0, 0, 9, -5]
terminal_state = [1, 6]

actions = ['L', 'R']
transition_probability = [0.8, 0.2]
discount_factor = 0.9

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

def transition_fn(state, action):
    if state in terminal_state:
        return ((state,action, 1), (state,action, 1))
    if action == 'L':
        return ((state-1,action, 0.8), (state, action,0.2))
    if action == 'R':
        return ((state+1, action, 0.8), (state, action, 0.2))


def build_q_table():
    sm_q_table = {}
    for state in states:
        sm_q_table[state] = {}
        for action in actions:
            sm_q_table[state][action] = 0
    return sm_q_table

def compute_greedy_policy(state, q_table):
    return  list(q_table[state].keys())[list(q_table[state].values()).index(max(q_table[state].values()))]

def compute_v_value(state, q_table):
    return max(q_table[state].values()) 

def compute_q_table(q_table,time_index):
        new_q_table = build_q_table()
        for state_action_pair in get_key_map([states, actions]):
        #print(state_action_pair)
                new_q_table[state_action_pair[0]][state_action_pair[1]] = compute_q_value(state_action_pair[0], state_action_pair[1], q_table,time_index)
        return new_q_table

def compute_q_value(state, action, q_table,time_index):
    if state in terminal_state:
        return reward_arr[states.index(state)]
    else:
        transition_tuple = transition_fn(state, action)
        accumilator = 0
        for transition in transition_tuple:
            #print(transition)
            accumilator += transition[2] * (reward_arr[states.index(state)] + discount_factor*compute_v_value(transition[0], q_table))
        
        return accumilator


def get_key_map(arr):
    finalmap = []
    for i in itertools.product(*arr):
        finalmap.append(i)
    return finalmap


q_table_timestep = {}
computed_v_values = []
dataframe_collection = {}


for i in range(0, 6):
    if i == 0:
        q_table_timestep[i] = build_q_table()
        continue
    else:
        q_table_timestep[i] = q_table_timestep[i-1]
    
    q_table_timestep[i] = compute_q_table(q_table_timestep[i],i)
    
    dataframe_collection[i]=pd.DataFrame(q_table_timestep[i])
    #print("V Function At Timestep ",i)
    for state in states:
            va = [i,state,compute_v_value(state,q_table_timestep[i]),compute_greedy_policy(state,q_table_timestep[i])]
            computed_v_values.append(va)


for key in dataframe_collection.keys():
    print("\n" +"="*40)
    print(key)
    print("-"*40)
    print(tabulate(dataframe_collection[key],headers='keys', tablefmt='fancy_grid'))
    dataframe_collection[key].to_csv('q-table-'+str(key)+'.csv')

df = pd.DataFrame(computed_v_values,columns=['Iteration_Number','State','Computed_Q_Value','Greedy_Next_State_Policy'])
print('\n')
print(tabulate(df,headers='keys', tablefmt='fancy_grid'))
df.to_csv('v-values.csv')
    #print(q_table_timestep)    
    #
#q_table = build_q_table()
