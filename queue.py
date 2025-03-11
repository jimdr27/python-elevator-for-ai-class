#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 11:31:41 2023

@author: rhee
"""

import copy
import sys

sys.setrecursionlimit(10**6) 

def manhattan(a):
    return sum(abs(val1-val2) for val1, val2 in zip([a[1],a[2], a[3], a[4]],[0, 0, 0, 0]))
def manhattan_q(a):
    last=a[-1]
    return sum(abs(val1-val2) for val1, val2 in zip([last[1], last[2], last[3], last[4]],[0, 0, 0, 0]))
    

"""
------------------------- μεταβλητές μετάβασης ------------------------------
"""
    
def go_to_floor1(state):
    if state[5]<8 and state[1]>0:
        if state[1]>8-state[5]:
            new_state = [1] + [state[1] + state[5] - 8] + [state[2]] + [state[3]] + [state[4]] + [8]
        else:
            new_state = [1] + [0] + [state[2]] + [state[3]] + [state[4]] + [state[1] + state[5]]
        return new_state
 
def go_to_floor2(state):
    if state[5]<8 and state[2]>0:
        if state[2]>8-state[5]:
                new_state = [2] + [state[1]] + [state[2]+state[5]-8] + [state[3]] + [state[4]] + [8] 
        else:
                new_state = [2] + [state[1]] + [0] + [state[3]] + [state[4]] + [state[2] + state[5]]
        return new_state

def go_to_floor3(state):
    if state[5]<8 and state[3]>0:
        if state[3]>8-state[5]:
            new_state = [3] + [state[1]] + [state[2]] + [state[3]+state[5]-8] + [state[4]] + [8]
        else:
            new_state = [3] + [state[1]] + [state[2]] + [0] + [state[4]] + [state[3] + state[5]]
        return new_state

def go_to_floor4(state):
    if state[5]<8 and state[4]>0:
        if state[4]>8-state[5]:
            new_state = [4] + [state[1]] + [state[2]] + [state[3]] + [state[4]+state[5]-8] + [8]
        else:
            new_state = [4] + [state[1]] + [state[2]] + [state[3]] + [0] + [state[4] + state[5]]
        return new_state

def go_to_roof(state):
    if(state[5]==8):
        new_state = [5] + [state[1]] + [state[2]] + [state[3]] + [state[4]] + [0]
        return new_state;
    else:
        if(state[1]==0):
            if(state[2]==0):
                if(state[3]==0):
                    if(state[4]==0):
                        new_state = [5] + [state[1]] + [state[2]] + [state[3]] + [state[4]] + [0]
                        print("ola empty")
                        return new_state;

"""
-------------------------------------- findchildren --------------------------------------
"""

def find_children(state):
    
    children=[]
    
    floor1_state=copy.deepcopy(state)
    floor1_child=go_to_floor1(floor1_state)

    floor2_state=copy.deepcopy(state)
    floor2_child=go_to_floor2(floor2_state)

    floor3_state=copy.deepcopy(state)
    floor3_child=go_to_floor3(floor3_state)

    floor4_state=copy.deepcopy(state)
    floor4_child=go_to_floor4(floor4_state)

    roof_state=copy.deepcopy(state)
    roof_child=go_to_roof(roof_state)
    
    if floor1_child!=None: 
        children.append(floor1_child)

    if floor2_child!=None: 
        children.append(floor2_child)
    
    if floor3_child!=None: 
        children.append(floor3_child)
    
    if floor4_child!=None: 
        children.append(floor4_child)
    
    if roof_child!=None: 
        children.append(roof_child)
        
    return children

""" ----------------------------------------------------------------------------
** initialization of front
** Αρχικοποίηση Μετώπου
"""

def make_front(state):
    return [state]
    
""" ----------------------------------------------------------------------------
**** expanding front
**** επέκταση μετώπου    
"""

def expand_front(front, method):  
    if method=='DFS':        
        if front:
            print("Front:")
            print(front)
            node=front.pop(0)
            for child in find_children(node):     
                front.insert(0,child)
    
    elif method=='BFS':
        if front:
            print("Front:")
            print(front)
            node=front.pop(0)
            for child in find_children(node):     
                front.append(child)
    elif method=='Heuristic':  
        if front:
            print("Front:")
            print(front)
            node=front.pop(0)
            for child in find_children(node):     
                front.append(child)
                front.sort(key=manhattan)
            if len(front)>5:
                while len(front)>5:
                    del front[-1]
    return front
   
""" ----------------------------------------------------------------------------
** initialization of queue
** Αρχικοποίηση ουράς
"""

def make_queue(state):
    return [[state]]

""" ----------------------------------------------------------------------------
**** expanding queue
**** επέκταση ουράς
"""

def extend_queue(queue, method):
    if method=='DFS':
        print("Queue:")
        print(queue)
        node=queue.pop(0)
        queue_copy=copy.deepcopy(queue)
        children=find_children(node[-1])
        for child in children:
            path=copy.deepcopy(node)
            path.append(child)
            queue_copy.insert(0,path)
    
    elif method=='BFS':
        print("Queue:")
        print(queue)
        node=queue.pop(0)
        queue_copy=copy.deepcopy(queue)
        children=find_children(node[-1])
        for child in children:
            path=copy.deepcopy(node)
            path.append(child)
            queue_copy.append(path) # η διαφορά στο queue μεταξύ του DFS και του BFS είναι εδώ
                                    # βάζοντας το κάθε καινούργιο παιδί στην αρχή είναι συνοδευτικό με το
                                    # DFS έτσι ώστε να ακολουθεί την ίδια "ιεραρχία" με τον ίδιο τον αλγόριθμο

    elif method=='Heuristic':    
        """print("Queue:")
        print(queue)
        queue_copy=copy.deepcopy(queue)
        queue.clear()
        queue_copy.sort(key=manhattan_q)
        if len(queue_copy)<5:
            length=len(queue_copy)
        else:
            length=5
        for i in range(length):
            node=queue_copy[i]
            children = find_children(node[-1])
            for child in children:
                path = copy.deepcopy(queue_copy[i])
                path.append(child)
                queue.append(path)
        queue_copy=copy.deepcopy(queue)"""
        print("Queue:")
        print(queue)
        node=queue.pop(0)
        queue_copy=copy.deepcopy(queue)
        children=find_children(node[-1])
        for child in children:
            path=copy.deepcopy(node)
            path.append(child)
            queue_copy.append(path)
            queue_copy.sort(key=manhattan_q)
        if len(queue_copy)>5:
            while len(queue_copy)>5:
                del queue_copy[-1]
    #else: "other methods to be added"
        
    
    return queue_copy
    

"""
-------------------------------------------------------------------------------
"""

def find_solution(front, queue, closed, goal, method, i):
#def find_solution(front, queue, closed, method):
       
    if not front:
        print('_NO_SOLUTION_FOUND_')
    
    elif front[0] in closed:
        new_front=copy.deepcopy(front)
        new_front.pop(0)
        new_queue=copy.deepcopy(queue)
        new_queue.pop(0)
        find_solution(new_front, new_queue, closed, goal, method, i)
        #find_solution(new_front, new_queue, closed, method)
    
    #elif is_goal_state(front[0]):
    elif front[0]==goal:        
        print('_GOAL_FOUND_')
        #print(front[0])
        print("Steps: ", i)
        print(queue[0])
        
    else:
        i=i+1
        closed.append(front[0])
        front_copy=copy.deepcopy(front)
        front_children=expand_front(front_copy, method)
        queue_copy=copy.deepcopy(queue)
        queue_children=extend_queue(queue_copy, method)
        closed_copy=copy.deepcopy(closed)
        find_solution(front_children, queue_children, closed_copy, goal, method, i)
        #find_solution(front_children, queue_children, closed_copy, method)
"""
-------------------------------------------------------------------------------
"""

def main():
    
    i=0 # δείκτης για καταγραφή μεγέθους path
    initial_state = [0, 9, 4, 12, 7, 0]
    """ ----------------------------------------------------------------------------
    **** [όροφος ασανσέρ, ένοικοι 1ου, ένοικοι 2ου, ένοικοι 3ου, ένοικοι 4ου, άτομα στο ασανσέρ]
    """
    goal = [5, 0, 0, 0, 0, 0]
    method=None # αρχικοποίηση του method ως κενή μεταβλητή για να λειτουργήσει η while που ελέγχει την είσοδο
    while method!='DFS' and method != 'BFS' and method !='Heuristic':
        method=input("What algorithm should be used? (Valid options: DFS, BFS, Heuristic) \n")
        if method=='DFS' or method == 'BFS' or method =='Heuristic': break
    
    """ ----------------------------------------------------------------------------
    **** starting search
    **** έναρξη αναζήτησης
    """
    
    print('____BEGIN__SEARCHING____')
    find_solution(make_front(initial_state), make_queue(initial_state), [], goal, method, i)
    
if __name__ == "__main__":
    main()
