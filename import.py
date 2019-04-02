import numpy
import itertools

s = numpy.random.uniform(0,1,10)

table_paths = [
    'Question5_Tables/Table1/Valay_Dave_Dave.txt',
    'Question5_Tables/Table2/Valay_Dave_Dave.txt',
    'Question5_Tables/Table3/Valay_Dave_Dave.txt',
    'Question5_Tables/Table4/Valay_Dave_Dave.txt',
    'Question5_Tables/Table5/Valay_Dave_Dave.txt'
]

A_keys = ['a1','a2']
table6 = [0.6,0.4] # A
B_keys = ['b1','b2','b3','b4']
table7 = [0.1,0.6,0.2,0.1] # B
C_keys = ['c1','c2']
table8 = [0.3,0.7]#C
table1 = [line.rstrip('\n').split(',') for line in open(table_paths[0])] # D | A,B,C
D_keys = ['d1','d2']
table2 = [line.rstrip('\n').split(',') for line in open(table_paths[1])] # E | A,B,C
E_keys = ['e1','e2']
table5 = [line.rstrip('\n').split(',') for line in open(table_paths[4])] # F | D,E
F_keys = ['f1','f2','f3','f4']
table3 = [line.rstrip('\n').split(',') for line in open(table_paths[2])] # G | D,E
G_keys = ['g1','g2','g3']
table4 = [line.rstrip('\n').split(',') for line in open(table_paths[3])] # H | D,E
H_keys = ['h1','h2','h3']

final_tables = [] #Contains the parsed Values here for D,E,F,G,H


# Python program to illustrate the intersection 
# of two lists in most simple way 
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 


def get_key_map(arr):
    finalmap = []
    for i in itertools.product(*arr):
        finalmap.append(i)
    return finalmap

D_map = get_key_map([A_keys,B_keys,C_keys])
E_map = get_key_map([A_keys,B_keys,C_keys])
F_map = get_key_map([D_keys,E_keys])
G_map = get_key_map([D_keys,E_keys])
H_map = get_key_map([D_keys,E_keys])

# match_index()
tables = [table1,table2,table5,table3,table4]
for table in tables:
    accumilator = []
    for row in table:
        accumilator.append([float(word) for word in row])
    final_tables.append(accumilator)

# These Datastructures help Finding the JPD for given and summation_variables. 
final_tables = [table6,table7,table8]+final_tables
main_keys = [A_keys,B_keys,C_keys,D_keys,E_keys,F_keys,G_keys,H_keys]
main_maps = [[],[],[],D_map,E_map,F_map,G_map,H_map] #Contains the conditionals. 


#Finds the join probability distribution value over the given and summation values. 
# summing_variables : [[random_variable_domain]]
# given_variables : [given_variable's_value_in_its_domain]
def sum_over(summing_variables,given_variables):
    summing_maps = get_key_map(summing_variables)
    #print(summing_variables)
    list_of_possible_vars = []
    for random_var in summing_variables:
        list_of_possible_vars+=random_var
    list_of_possible_vars+=given_variables

    #From List of possible Values Find out its posible index of the RV in the main_keys vector(This vector hold each Random variable's domain) and index of the value within its domain
    given_var_index = [] #(main_keys_index,sub_keys_index) --> a2 will be (0,1) when [['a1', 'a2'], ['b1', 'b2', 'b3', 'b4'], ['c1', 'c2'], ['d1', 'd2'], ['e1', 'e2'], ['f1', 'f2', 'f3', 'f4'], ['g1', 'g2', 'g3'], ['h1', 'h2', 'h3']] is main_keys
    for var_index in range(0,list_of_possible_vars.__len__()):
        for main_key_index in range(0,main_keys.__len__()):
            if list_of_possible_vars[var_index] in main_keys[main_key_index]:
                individual_key_position = next((i for i, item in enumerate(main_keys[main_key_index]) if item == list_of_possible_vars[var_index]), -1)
                given_var_index.append((main_key_index,individual_key_position))
    # print(given_var_index)
    # print(list_of_possible_vars)

    value_combos = [] 
    #Finds the combination of values that match the have the right conditionals matching all the variables. Probability is extracted here. 
    for map_index,domain_position in given_var_index: #domain_position : position of value in the actual domain of the RV. 
        if main_maps[map_index].__len__() > 0:
            sub_index =0 # This is to find the conditional Prob column for the final_tables
            for var in main_maps[map_index]:
                if intersection(list(var),list_of_possible_vars) == list(var):
                    value_combos.append((map_index,domain_position,main_keys[map_index][domain_position],final_tables[map_index][sub_index][domain_position],intersection(list(var),list_of_possible_vars)))
                sub_index+=1
        else:
           value_combos.append((map_index,domain_position,main_keys[map_index][domain_position],final_tables[map_index][domain_position],[]))
        
        
    #The below line finds all possible combinations of the given condition variables+summation_variables. 
    combo_keys = get_key_map(summing_variables+[[word] for word in given_variables ])#Key combinations to retrive the actual data for summation.  
    
    summation_values = []
    #For Each possible complete combination of summation and given values, Find the the appropriate values within the combo that club togather to be multiplied later. 
    for key_tuple in combo_keys:
        print(key_tuple)
        key_list = list(key_tuple)
        multiplication_values = []
        for value_object in value_combos: #(index_data_arrays,position_in_domain,probability_of_key_after_givens,actual_key,list_of_give_vars)
            if value_object[2] in key_list:
                if value_object[4].__len__() > 0:
                    #print(intersection(value_object[4],key_list),)
                    if intersection(value_object[4],key_list) == value_object[4]:
                        multiplication_values.append((value_object[2],value_object[3],value_object[4]))
                else:
                    multiplication_values.append((value_object[2],value_object[3],value_object[4]))
        # print("Appending Values For :",key_list,multiplication_values.__len__())
        # for val in multiplication_values:
        #     print(val)
        summation_values.append(multiplication_values)
    s = ""
    number_value = ""
    print(":::::::::::::::: SUMMING OVER VALUES ::::::::::::::::")
    sum_Index = 0
    sum_acc = 0
    for multiplication_values in summation_values: # Multiply the Values and sum them
        ######################Create Printing string And Summation Values###################### 
        acc = "("
        number_acc = "("
        mul_acc = None
        val_index =0
        for value_obj in multiplication_values:
            if value_obj[2].__len__() > 0 : 
                acc+= " P("+value_obj[0]+"|"+",".join(value_obj[2])+") *"
                number_acc+=" "+str(value_obj[1])+" *"
            elif val_index == multiplication_values.__len__() - 1:
                acc+= " P("+value_obj[0]+")"
                number_acc+=" "+str(value_obj[1])
            else:
                acc+= " P("+value_obj[0]+") *"
                number_acc+=" "+str(value_obj[1])+" *"
            val_index+=1

            if mul_acc == None:
                mul_acc = value_obj[1]
                continue
            else:
                mul_acc *= value_obj[1]
                         
        acc+=")"
        number_acc+=")"
        if sum_Index == summation_values.__len__() - 1:
            s+=acc
            number_value+=number_acc
        else:
            number_value+=number_acc +"+"+'\n'
            s+=acc + "+"+'\n'
        sum_Index+=1
        sum_acc+=mul_acc
    ##################################################################

    ##########################CREATE Summation  Value########################################
    print(s)
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print(":::::::::::::::::::::: In Numbers The SUM IS: :::::::::::::::::::::::")
    print(number_value)
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print(":::::::::::::::::::::: Actual SUM :::::::::::::::::::::::")
    print(sum_acc)
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    return sum_acc
        
print("############################## Solution For Q1)1 ##############################")
ans11 = sum_over([A_keys,D_keys,F_keys],['e1','c1','h2','g3','b2'])

ans12 = sum_over([A_keys,D_keys,F_keys,E_keys],['c1','h2','g3','b2'])

print('\n\n\n FINAL SUM For '+str(ans11/ans12)+'\n\n\n')

print("##########################################################################################")

print("############################## Solution For Q1)2 ##############################")
ans21 = sum_over([A_keys,E_keys,F_keys],['d1','c1','h3','g2','b4'])

ans22 = sum_over([A_keys,D_keys,F_keys,E_keys],['c1','h3','g2','b4'])

print('\n\n\n FINAL SUM For '+str(ans21/ans22)+'\n\n\n')

print("##########################################################################################")
tables = [table6,table7,table8] + tables # [table6,table7,table8,table1,table2,table5,table3,table4]
#final_table_domain_lengths = [table6.__len__(),table7.__len__(),table8.__len__()]+ final_table_domain_lengths
#print(final_table_domain_lengths)

############################################################ SAMPLING CODE BELOW :::: ################################################

num_samples = 10

def get_range_index(value,range_table):
    index = 0
    acc = 0
    for distribution_value in range_table:
        acc+=distribution_value
        #print("Comparing : ",value,acc)
        if(value<=acc ):
            return index
        index+=1
    print("It Should Never Reach Here!")
    return index

samples = [] # [[Rv_Domain_index],[Rv_Domain_index]] : Each Array is an RV.
for table in tables[:3]:
    #TODO : Handle Priors
   # print(table)
    random_distribution = numpy.random.uniform(0,1,num_samples)
    samples.append([get_range_index(particle,table)for particle in random_distribution])
# For Each Random Varaiable pick the index of the sample
#random_distribution_D = numpy.random.uniform(0,1,num_samples)

#samples_of_priors = samples[:3] --> Contains for A, B , C
#prior_symbols = ['a','b','c']
#print(final_tables[0])


def extract_samples(available_probability_distribution,some_random_distribution,prior_symbols,samples_of_priors,probability_index_map,random_var):
    return_samples = []
    for i in range(0,some_random_distribution.__len__()):
        current_samples = [] #[A,B,C,D,..]
        for sample in samples_of_priors:
            current_samples.append(sample[i])
        current_letter_index =0
        acc_arr = []
        for sample_value in current_samples:
            acc_arr.append(prior_symbols[current_letter_index]+str(sample_value+1))
            current_letter_index+=1
        comparing_map = tuple(acc_arr)
        index_in_distribution = next((i for i, item in enumerate(probability_index_map) if item == comparing_map), -1)
        if index_in_distribution == -1:
            print("THIS COMPUTATION WENT WRONG : ")
            break
        chosen_probability_distribution = available_probability_distribution[index_in_distribution]
        #print("Index Of Probability: ",index_in_distribution,comparing_map)
        #print("With Distribution :",chosen_probability_distribution)
        sampled_value = get_range_index(some_random_distribution[i],chosen_probability_distribution)
        #print("Index Of The RV : ",random_var,sampled_value,comparing_map,some_random_distribution[i])
        return_samples.append(sampled_value)
    return return_samples

    #TODO : Handle

A_samples = [get_range_index(particle,final_tables[0]) for particle in random_distribution]
B_samples = [get_range_index(particle,final_tables[1]) for particle in random_distribution]
C_samples = [get_range_index(particle,final_tables[2]) for particle in random_distribution]
D_samples = extract_samples(final_tables[3],numpy.random.uniform(0,1,num_samples),['a','b','c'],samples[0:3],D_map,'D')
E_samples = extract_samples(final_tables[4],numpy.random.uniform(0,1,num_samples),['a','b','c'],samples[0:3],E_map,'E')
F_samples = extract_samples(final_tables[5],numpy.random.uniform(0,1,num_samples),['d','e'],[D_samples,E_samples],F_map,'F')
G_samples = extract_samples(final_tables[6],numpy.random.uniform(0,1,num_samples),['d','e'],[D_samples,E_samples],G_map,'G')
H_samples = extract_samples(final_tables[7],numpy.random.uniform(0,1,num_samples),['d','e'],[D_samples,E_samples],H_map,'H')
result = list(map(lambda x : 'a'+str(x+1),A_samples))
#print(result)


