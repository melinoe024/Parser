import sys
import pandas as pd


# get the input strinng from the command line
input_file = open(sys.argv[1], 'r')
input_string = input_file.read()
input_file.close()

# error recovery option
error_on = False
if len(sys.argv) > 2:
    if (str(sys.argv[2]) == 'error'):
        error_on = True

# remove whitespaces
input_string = input_string.replace(" ", "")
input_string = input_string.replace("\n", "")
input_string = input_string.replace("\t", "")


# VARIABLES and TERMINALS
var = ['L','A','E','B','C','D','F','V','T']
ter = ['a','b','c','d','0','1','2','3','+','-','*','print','if','(',')','$']

# FIRSTS
first = {'L': ['a','b','c','d','0','1','2','3','('],
          'A': ['a','b','c','d','0','1','2','3','ε','('],
          'E': ['a','b','c','d','0','1','2','3','('],
          'B': ['if','+','-','*','print'],
          'C': ['if'],
          'D': ['a','b','c','d','0','1','2','3','ε','('],
          'F': ['+','-','*','print'],
          'V': ['a','b','c','d'],
          'T': ['0','1','2','3']}

# input '1' = one of [+,-,*]
# input '0' = others
dfa = {0:{'0':0, '1':1},
       1:{'0':1, '1':2},
       2:{'0':2, '1':0}}

# create a parse table
df = pd.DataFrame(index=var, columns=ter)
df = df.fillna('none')

# fill in the values of the parse tale
df.set_value('L', 'a', 'EA')
df.set_value('A', 'a', 'L')
df.set_value('E', 'a', 'V')
df.set_value('D', 'a', 'E')
df.set_value('V', 'a', 'a')

df.set_value('L', 'b', 'EA')
df.set_value('A', 'b', 'L')
df.set_value('E', 'b', 'V')
df.set_value('D', 'b', 'E')
df.set_value('V', 'b', 'b')

df.set_value('L', 'c', 'EA')
df.set_value('A', 'c', 'L')
df.set_value('E', 'c', 'V')
df.set_value('D', 'c', 'E')
df.set_value('V', 'c', 'c')

df.set_value('L', 'd', 'EA')
df.set_value('A', 'd', 'L')
df.set_value('E', 'd', 'V')
df.set_value('D', 'd', 'E')
df.set_value('V', 'd', 'd')

df.set_value('L', '0', 'EA')
df.set_value('A', '0', 'L')
df.set_value('E', '0', 'T')
df.set_value('D', '0', 'E')
df.set_value('T', '0', '0')

df.set_value('L', '1', 'EA')
df.set_value('A', '1', 'L')
df.set_value('E', '1', 'T')
df.set_value('D', '1', 'E')
df.set_value('T', '1', '1')

df.set_value('L', '2', 'EA')
df.set_value('A', '2', 'L')
df.set_value('E', '2', 'T')
df.set_value('D', '2', 'E')
df.set_value('T', '2', '2')

df.set_value('L', '3', 'EA')
df.set_value('A', '3', 'L')
df.set_value('E', '3', 'T')
df.set_value('D', '3', 'E')
df.set_value('T', '3', '3')

df.set_value('B', '+', 'F')
df.set_value('F', '+', '+L')

df.set_value('B', '-', 'F')
df.set_value('F', '-', '-L')

df.set_value('B', '*', 'F')
df.set_value('F', '*', '*L')

df.set_value('B', 'print', 'F')
df.set_value('F', 'print', 'printL')

df.set_value('B', 'if', 'C')
df.set_value('C', 'if', 'ifEED')

df.set_value('L', '(', 'EA')
df.set_value('E', '(', '(B)')
df.set_value('D', '(', 'E')

df.set_value('A', ')', '')
df.set_value('D', ')', '')

df.set_value('A', '$', '')



# make the list elements into a single string
# inputs - a reversed list 
def getString(input_list):
    output_list = []
    # reverse the reversed list (to normal) 
    for i in range(len(input_list)-1, -1, -1):
        output_list.append(input_list[i])
    
    return ''.join(output_list)


# check if there exists a rule for the current state
def matching_rule(unscanned, stack):
    # unexpected terminal value
    if (unscanned[-1] not in ter):
        rule = 'none'
    # unexpected variable value
    elif (stack[-1] not in var):
        rule = 'none'
    # else, return the rule with given terminal and variable
    else:
        rule = df[unscanned[-1]][stack[-1]]
    return rule


# add the given string to the list (stack)
def add_new(string, input_list):
    # changing the print and if, so that by observing the first character we can decide to add print or if
    string = string.replace('print', 'P')
    string = string.replace('if', 'I')
    # to make the list to work as a stack, put them in the reversed order
    for i in range(len(string)-1,-1,-1):
        # we want 'print' and 'if' to be treated as the same symbol, not one by one
        if (string[i] == 'P'):
            input_list.append('print')
        elif (string[i] == 'I'):
            input_list.append('if')
        else:
            input_list.append(string[i])
        
    return input_list


# change the input list format to {..., ..., ...} format
def list_format_change(input_list):
    output_string = "{"
    for i in range(len(input_list)):
        if i != 0:
            output_string += ", "
        output_string += str(input_list[i])
    output_string += "}"
    return output_string





#############################################################################################
#################################### 5.2 RegEx ##############################################
#############################################################################################

# changes the dfa state 
def dfa_state(input_string):
    state = 0
    
    # for each element of input_string, if the current element is an arithmetic operation, change the state
    # 0 -> 1, 1-> 2, 2-> 0
    for i in input_string:
        if i in ['+', '-', '*']:
            state = dfa[state]['1']
        else:
            state = dfa[state]['0']
        
    return state
    

# this happens if and only if the input_string starts with n:
# i.e. input_string[0] = one of 0, 1, 2 and input_string[1] is a colon
if (len(input_string) >= 2):
    if ((input_string[0] in ['0','1','2']) and (input_string[1] == ':')):
        # parse the string after colon to dfa
        state = dfa_state(input_string[2:])
        
        # if rejected, the program will exit 
        if (str(state) != input_string[0]):
            print('REJECTED, the language does not meet the DFA condition.')
            exit()
        # if not rejected, the program will continue
        else:
            print('The language meets the DFA condition.')
            input_string = input_string[2:]




#############################################################################################
#################################### 5.1 Parser #############################################
#############################################################################################


# setting the lists, lists should work like stacks 
unscanned = []
stack = []
unscanned.append('$')
stack.append('$')
stack.append('L')
unscanned = add_new(input_string, unscanned)


while 1:
    print("{}          {}".format(getString(unscanned), getString(stack)))

    # base case, if both unscanned and stack have only $ left, break
    if (len(unscanned) == 1 and len(stack) == 1):
        if (unscanned[-1] == '$' and stack[-1] == '$'):
            print('ACCEPTED')
            break
        
    # if the tops are equal, remove each top
    elif (unscanned[-1] == stack[-1]):
        del stack[-1]
        del unscanned[-1]
            
    else:
        rule = matching_rule(unscanned, stack)
        # if there exists a rule, replace the current stack top to the new one
        if (rule != 'none'):
            del stack[-1]
            stack = add_new(rule, stack)
            
            
        else:
            if (error_on == False):
                print('REJECTED')
                break
            else:
    #############################################################################################
    ################################## 6 Extension, Error Recovery ##############################
    #############################################################################################

    # to run the extension code, write 'python parser.py input_file error' on the command line
        
                # if the top of the stack is a terminal
                if (stack[-1] in ter):
                    print('Error: got {}, but expected {}.'.format(unscanned[-1], stack[-1]))
                    
                    # if unscanned is empty, then ADD
                    if (len(unscanned) == 1):
                        user_input = input('Add input? ')
                        # check if the input is valid
                        while True:
                            if (user_input != stack[-1]):
                                user_input = input('Wrong input given. Add input? ')
                            else:
                                break
                        unscanned = add_new(user_input, unscanned)
                    
                    # if unscanned has different input, then DELETE
                    else:
                        user_input = input('Delete input? [Y/N]')
                    
                        if (user_input == 'Y'):
                            del unscanned[-1]
                        elif (user_input == 'N'):
                            print('REJECTED')
                            break
                        # check if the input is valid
                        else:
                            while True:
                                if (user_input not in ['Y', 'N']):
                                    user_input = input('Wrong input given. Delete input? [Y/N] ')
                                else:
                                    break
                
                # if the top of the stack is a variable
                elif (stack[-1] in var):
                    print('Error: got {}, but expected {}.'.format(unscanned[-1], list_format_change(first[stack[-1]])))
                    
                    # if unscanned is empty, then ADD
                    if (len(unscanned) == 1):
                        user_input = input('Add input? ')
                        # check if the input is valid
                        while True:
                            if (user_input not in first[stack[-1]]):
                                user_input = input('Wrong input given. Add input? ')
                            else:
                                break
                        unscanned = add_new(user_input, unscanned)
                    
                    # just different value, then REPLACE
                    else:
                        user_input = input('Replace input? ')
                       
                        # check if the input is valid
                        while True:
                            if (user_input not in first[stack[-1]]):
                                user_input = input('Wrong input given. Add input? ')
                            else:
                                break
                        # first remove the current head, and then add the new one
                        del unscanned[-1]
                        unscanned = add_new(user_input, unscanned)
                        
                else:
                    print('REJECTED')
                    break
            