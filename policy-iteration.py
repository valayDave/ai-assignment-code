import json
import itertools
import pandas as pd
from tabulate import tabulate
import copy

states = [1, 2, 3]
reward_arr = [-1,-2,-1]
terminal_state = [2]

actions = ['A', 'B']
transition_probability = [0.8, 0.2]
discount_factor = 0.9

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

def transition_fn(state, action):
    if state in terminal_state:
        return ((state,action, 1), (state,action, 1))
    if action == 'A':
        if state == 1:
            return ((2,action, 0.8), (1, action,0.2))
        if state == 3:
            return ((1,action, 0.9), (3, action,0.1))
            
    if action == 'B':
        if state == 1:
            return ((3,action, 0.9), (1, action,0.1))
        if state == 3:
            return ((2,action, 0.8), (3, action,0.2))
        #return ((state+1, action, 0.8), (state, action, 0.2))


def build_q_table():
    sm_q_table = {}
    for state in states:
        sm_q_table[state] = {}
        for action in actions:
            sm_q_table[state][action] = 0
    return sm_q_table


def compute_v_value(state, q_table):
    return max(q_table[state].values())

def compute_q_table(q_table,state_action_pairs):
        new_q_table = build_q_table()
        for state_action_pair in state_action_pairs:
        #print(state_action_pair)
                new_q_table[state_action_pair[0]][state_action_pair[1]] = compute_q_value(state_action_pair[0], state_action_pair[1], q_table)
        return new_q_table

def compute_q_value(state, action, q_table):
    if state in terminal_state:
        return reward_arr[states.index(state)]
        
    else:
        transition_tuple = transition_fn(state, action)
        accumilator = 0
        for transition in transition_tuple:
            #print(transition)
            accumilator += transition[2] * (reward_arr[states.index(state)] + discount_factor*compute_v_value(transition[0], q_table))
            print(str(transition[2])+' * ('+str(reward_arr[states.index(state)])+' + '+ str(discount_factor)+' * '+str(compute_v_value(transition[0], q_table))+' )')
        print('Current Transition Tuple',transition_tuple,'For states',state,action,accumilator)
        return accumilator

def compute_greedy_policy(state, q_table):
    return  list(q_table[state].keys())[list(q_table[state].values()).index(max(q_table[state].values()))]

def get_key_map(arr):
    finalmap = []
    for i in itertools.product(*arr):
        finalmap.append(i)
    return finalmap

#TODO : Compute Policy Iteration
policy_v = {}
current_policy = [(1,'B'),(3,'B'),(2,'B')]
printing_df_arr = []
time_step = 0
for i in range(0, 15):
    time_step = i
    if i == 0:
        policy_v[i] = build_q_table()
        continue
    else:
        policy_v[i] = build_q_table()
    
    prev_v_values = copy.deepcopy(policy_v[i-1])
    new_policy = []
    deltas = []
    print("Current Policy :",current_policy)
    for state,curr_action in current_policy: # TODO : Compute V Values.
        transition_tuples = transition_fn(state,curr_action)
        add_v_val = 0
        for next_state,action,prob in transition_tuples:
            if state not in terminal_state:
                add_v_val += prob*(reward_arr[states.index(state)] + discount_factor* prev_v_values[next_state][curr_action])
            else:
                add_v_val = reward_arr[states.index(state)]
        policy_v[i][state][curr_action] = add_v_val

        if state not in terminal_state:
            delta = prev_v_values[next_state][curr_action] - policy_v[i][state][curr_action]
            deltas.append(delta)
            print('State',state,'Action',curr_action,"Previous V",prev_v_values[next_state][curr_action],"Value After Policy Evaluation : ",policy_v[i][state][curr_action])
        
    #TODO: Conduct Policy Update : VALIDATE WEATHER THIS SHOULD COME HERE OR WHERE SHOULD THIS CHECK BE DONE> 
    for state,curr_action in current_policy:
        if state in terminal_state:
            new_policy.append((state,curr_action))
            continue
        all_state_action_pairs = get_key_map([[state],actions])
        new_action = None,
        s_a_values = {}
        for curr_state,action in all_state_action_pairs:
            transition_tuples = transition_fn(state,action)
            # print(curr_state,action)
            add_v_val = 0
            for next_state,action,probability in transition_tuples:
                    add_v_val += probability*(reward_arr[states.index(state)] + discount_factor* policy_v[i][state][curr_action])
            s_a_values[action] = add_v_val
        
        # list(s_a_values.keys()).index(list(s_a_values.values()).index(max()))
        # new_action = list(s_a_values.keys())[]
        print(s_a_values)
        new_action_key_index = list(s_a_values.values()).index(max(list(s_a_values.values())))
        new_action = list(s_a_values.keys())[new_action_key_index]
        new_policy.append((state,new_action))
        print("State",state,"Current Policy Value :",curr_action,"POLICY UPDATE :",new_action)

    print("New Policy : ",new_policy)
    #current_policy = new_policy
    print("=="*15+"Iteration "+str(i)+"=="*15)
    
    if [delta for delta in deltas if abs(delta) > 0.01].__len__() == 0:
        print("Deltas",deltas)
        break
print(json.dumps(policy_v, indent=4, sort_keys=True))

# q_table_timestep = {}
# computed_v_values = []
# dataframe_collection = {}

# for i in range(0, 5):
#     if i == 0:
#         q_table_timestep[i] = build_q_table()
#         continue
#     else:
#         q_table_timestep[i] = q_table_timestep[i-1]
    
#     q_table_timestep[i] = compute_q_table(q_table_timestep[i],get_key_map([states, actions]))
    
#     # print("V Function At Timestep ",i)
#     # for state in states:
#     #         print(state,round(compute_v_value(state,q_table_timestep[i])))


#     dataframe_collection[i]=pd.DataFrame(q_table_timestep[i])
#     #print("V Function At Timestep ",i)
#     for state in states:
#         if state not in terminal_state:
#             va = [i,state,compute_v_value(state,q_table_timestep[i]),compute_greedy_policy(state,q_table_timestep[i])]
#             computed_v_values.append(va)


# for key in dataframe_collection.keys():
#     print("\n" +"="*40)
#     print(key)
#     print("-"*40)
#     print(tabulate(dataframe_collection[key],headers='keys', tablefmt='fancy_grid'))
#     #dataframe_collection[key].to_csv('q-table-'+str(key)+'.csv')

# df = pd.DataFrame(computed_v_values,columns=['Iteration_Number','State','Computed_Q_Value','Greedy_Next_State_Policy'])
# print('\n')
# print(tabulate(df,headers='keys', tablefmt='fancy_grid'))
#     #print(q_table_timestep)    
#     #
# #q_table = build_q_table()
