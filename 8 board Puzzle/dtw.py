# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 11:30:58 2017

@author: gaurav
"""

import time
import numpy as np
from multiprocessing import Queue 
from Queue import PriorityQueue
import sys

#if sys.platform == "win32":
#    import psutil
#else:
##    import resource
#method = sys.argv[1]
#board_statex = sys.argv[2]


def Write_file(output):
    file = open('output.txt','w')
#    if sys.platform == "win32":
#        usage = 0#psutil.Process().memory_info().rss /1048576
#        print('max_ram_usage: %s\n' %  usage)
#    else:
#        usage = resource.int(getrusage(resource.RUSAGE_SELF).ru_maxrss)/1048576
#        print('max_ram_usage: %s\n' % usage)
        
    file.write('path_to_goal: %s\n' % output[0])
    file.write('cost_of_path: %s\n' % output[1])
    file.write('nodes_expanded: %s\n' % output[2])
    file.write('search_depth: %s\n' % output[3])
    file.write('max_search_depth: %s\n' % output[4])
    file.write('running_time: %s\n' % output[5])
#    if sys.platform == "win32":
#        usage = 0 #psutil.Process().memory_info().rss /1048576
#        file.write('max_ram_usage: %s\n' %  usage)
#    else:
#        usage = resource.int(getrusage(resource.RUSAGE_SELF).ru_maxrss)/1048576
#        file.write('max_ram_usage: %s\n' % usage)

def valid_moves(state):
	valid_moves = ['Up','Down','Left','Right']
	zero_index = state.index(0)
	column_pos = zero_index%3

	if column_pos==0:valid_moves.remove('Left')
	if column_pos==2:valid_moves.remove('Right')
	if (zero_index - 3) < 0: valid_moves.remove('Up')
	if (zero_index + 3) > 8: valid_moves.remove('Down')

	return valid_moves

def neighbors(state):

	
	valid_move = valid_moves(state)
	neighbors = [None]*4	
	zero_index = state.index(0)

	for moves in valid_move:
		new_board = list(state)

		if moves =='Up':
			temp = new_board[zero_index-3]
			new_board[zero_index - 3] = new_board[zero_index]
			new_board[zero_index] = temp
			neighbors[0] = new_board

		if moves=='Down':
			new_board = list(state)
			temp = new_board[zero_index+3]
			new_board[zero_index+3] = new_board[zero_index]
			new_board[zero_index] = temp
			neighbors[1] = new_board

		if moves == 'Right':
			new_board = list(state)
			temp = new_board[zero_index+1]
			new_board[zero_index+1] = new_board[zero_index]
			new_board[zero_index] = temp
			neighbors[3] = new_board
		
		if moves == 'Left':
			new_board = list(state)
			temp = new_board[zero_index-1]
			new_board[zero_index-1] = new_board[zero_index]
			new_board[zero_index] = temp
			neighbors[2] = new_board


	return neighbors

class Node:
    def __init__(self,state,priority=0):	
        self.state = state
        self.priority = priority
        self.parent = None
        self.depth = 0
        self.path_cost = 0
        self.key =  "".join(str(x) for x in self.state)

#    def _compare(self, other, method):
#        try:
#            return method(self._cmpkey(), other._cmpkey())
#        except (AttributeError, TypeError):
#            return NotImplemented

    def __lt__(self, other):
        return self.priority < other.priority
    
    def __gt__(self, other):
        return self.priority > other.priority
    
#    def __eq__(self,other):
#        return self.priority == other.priority
		
    def set_state(self,new_state):
        self.state = new_state
    
    def set_priority(self):
        self.priority = heur(self.state) + self.depth
        
    def set_parent(self,new_parent):
        self.parent = new_parent
        
    def set_depth(self):			
        self.depth = self.parent.depth + 1
    
    def path_cost(self,path_cost):
        self.path_cost = path_cost + 1
        
    def get_dir(self,new_dir):
        self.dir = new_dir

	# def add(self,node):
	# 	self.Node[node.key]=node

	# def add_to_frontierbfs(self,node):
	# 	self.fron_key_holder.append(node.key)



	# def get_stamp(self): #returns string stamp of 'self.loc'
	# 	return "".join(str(x) for x in self.state)

    def get_path(self):
        path = []
        x = self
        while x.parent != None:
            path.append(x.dir)
            x = x.parent

        return(list(reversed(path)))

    def goal_check(self):
        goal = [0,1,2,3,4,5,6,7,8]
        return(self.state == goal)

def BFS(initialState):
    frontier = []
    state=Node(initialState)
    #state.set_depth(0)
    state.set_parent(None)
    frontier.append(state)
#    explored = set()
    exploredstamps= set()
    exploredstamps.add(state.key)
    UDLR=["Up","Down","Left","Right"]
    max_depth=0
    max_mem=0
    exec_time = time.time()
    while not(frontier==[]): 
        state = frontier.pop(0)
		
        if (state.goal_check()):
            direction = [UDLR[i] for i in state.get_path()]
            cost_of_path = len(state.get_path())
            nodes_expanded = len(exploredstamps)-len(frontier)-1
            search_depth = state.depth
            max_sdepth = max_depth
            time_elapsed =time.time()-exec_time
            mem_consumed = max_mem
            
            output = [direction,cost_of_path,nodes_expanded,search_depth,max_sdepth,time_elapsed,mem_consumed]
            Write_file(output)
#            print(output[1])
#            np.savetxt(fname + ".txt", data,newline =",", delimiter ='\r\n')
##            Write(state,path,expanded,depth,max_depth,exec_times)
#            return [[UDLR[i] for i in state.get_path()],
#		      len(state.get_path()), len(exploredstamps)-len(frontier)-1, 
#              state.depth, max_depth,time.time()-exec_time,max_mem]
#            print(output[1])
            return output

        successor = neighbors(state.state)
        for index,item in enumerate(successor):
             if item!=None:
                 child=Node(item)
                 
                 if not(child.key in exploredstamps):
                     child.set_parent(state)
                     child.set_depth()
                     
                     child.get_dir(index)
                     frontier.append(child)
                     exploredstamps.add(child.key)
                     max_depth=max(max_depth,child.depth)
                     
    return False

#def DFS(initialState):
#    frontier = []
#    state=Node(initialState)
#    frontier.append(state)
#	#    explored = set()
#    exploredstamps= set()
#    exploredstamps.add(state.key)
#    UDLR=list(reversed(["Right","Left","Down","Up"]))
#    max_fringe_size=0
#    max_depth=0
#    max_mem=0
#    print(frontier[0].state)
#    
#    while not(frontier==[]): 
#        max_fringe_size=max(max_fringe_size,len(frontier))
#        state = frontier.pop()
#        
#        if (state.goal_check()): 
#            return [[UDLR[i] for i in state.get_path()],len(state.get_path()), 
#					len(exploredstamps)-len(frontier)-1, len(frontier), max_fringe_size, 
#					state.depth, max_depth,time.time(),max_mem]
#            successor = list(reversed(neighbors(state.state)))
#            
#            for index,item in enumerate(successor):
#                if item!=None:
#                    child=Node(item)
#                    
#                    if not(child.key in exploredstamps):
#                        child.set_parent(state)
#                        child.set_depth(state.depth+1)
#                        child.get_dir(index)
#                        frontier.append(child)
#					#explored.add(child)
#                        exploredstamps.add(child.key)
#                        max_depth=max(max_depth,child.depth)
#                        
#    return False

def DFS(initialState):
    frontier = []
    state=Node(initialState)
    #state.set_depth(0)
    state.set_parent(None)
    frontier.append(state)
#    explored = set()
    exploredstamps= set()
    exploredstamps.add(state.key)
    UDLR=["Up","Down","Left","Right"]
    UDLR = UDLR[::-1]
    max_depth=0
    max_mem=0
    exec_time = time.time()
    while not(frontier==[]): 
        state = frontier.pop()
		
        if (state.goal_check()):
            direction = [UDLR[i] for i in state.get_path()]
            cost_of_path = len(state.get_path())
            nodes_expanded = len(exploredstamps)-len(frontier)-1
            search_depth = state.depth
            max_sdepth = max_depth
            time_elapsed =time.time()-exec_time
            mem_consumed = max_mem
            
#            output = [direction,cost_of_path,nodes_expanded,search_depth,max_sdepth,time_elapsed,mem_consumed]
#            Write_file(output)
            return [[UDLR[i] for i in state.get_path()],
		len(state.get_path()), len(exploredstamps)-len(frontier)-1, 
		state.depth, max_depth,time.time()-exec_time,max_mem]

        successor = neighbors(state.state)
        for index,item in enumerate(successor):
             if item!=None:
                 child=Node(item)
                 
                 if not(child.key in exploredstamps):
                     child.set_parent(state)
                     child.set_depth()
                     
                     child.get_dir(index)
                     frontier.append(child)
                     exploredstamps.add(child.key)
                     max_depth=max(max_depth,child.depth)
                     
    return False



def heur(state):
       i = 0
       x = 0
       for Number in state:
            Heuristic = (abs(Number//3 - i//3)) + (abs(Number%3 - i%3))
            #print(x)
            x = x+ Heuristic
            i += 1 

       return x
   


def AST(state):
    frontier = PriorityQueue()
    f = []
    explored = set()
    start = Node(state)
    count = 0
    UDLR=["Up","Down","Left","Right"]
    counter= 1
    frontier.put((heur(state),count,start))
    f.append(start)
    explored.add(start.key)
    exec_time = time.time()
    max_depth = 0
    max_mem = 0
    nodes_exp = 0
    
    while frontier:
        (priority,tcount,node) = frontier.get()
        if node.goal_check():
            direction = [UDLR[i] for i in node.get_path()]
            cost_of_path = len(node.get_path())
            nodes_expanded = nodes_exp
            search_depth = node.depth
            max_sdepth = max_depth
            time_elapsed =time.time()-exec_time
            mem_consumed = max_mem
            
            output = [direction,cost_of_path,nodes_expanded,search_depth,max_sdepth,time_elapsed,mem_consumed]
            Write_file(output)
#            print(output[1])
            return[[UDLR[i] for i in node.get_path()],len(node.get_path()),
                    nodes_exp,node.depth, max_depth,time.time()-exec_time,max_mem]
        
        
        successor = neighbors(node.state)
        nodes_exp += 1
        for index,value in enumerate(successor):
            if value != None:
                child = Node(value)
                
                if child.key not in explored:
                    child.set_parent(node)
                    child.set_depth() 
                    
                    child.get_dir(index)
                    score =  heur(value) + child.depth + 1
                    frontier.put((score,count,child))
                    f.append(child)
                   # print(heur(value))
                    explored.add(child.key)
                    max_depth=max(max_depth,child.depth)
#                    print(child.state)
                    #print(score)
                    count += 1
                    counter += 1
                   
    return False

#def Write(state,path,expanded,depth,max_depth,exec_time):
#    file = open('output.txt', 'w')
#
#    path = path
#    nodes_expanded = expanded
#    cost = len(path)
#    search_depth = depth
#    depth_max = max_depth
#    time = exec_time
#    
#    file.write('path_to_goal: %s\n' % path)
#    file.write('cost_of_path: %s\n' % cost)
#    file.write('nodes_expanded: %s\n' % nodes_expanded)
#    file.write('search_depth: %s\n' % search_depth)
#    file.write('max_search_depth: %s\n' % depth_max)
#    file.write('running_time: %.8f\n' % time)
#    
#    if sys.platform == "win32":
#        usage = psutil.Process().memory_info().rss /1048576
#        file.write('max_ram_usage: %.8f\n' %  usage)
#    else:
#        usage = resource.int(getrusage(resource.RUSAGE_SELF).ru_maxrss)/1048576
#        file.write('max_ram_usage: %.8f\n' % usage)
#        
#        
print(DFS([1,2,5,3,4,0,6,7,8]))

#if method == "bfs":
#    board_state = [int(i) for i in board_statex]
#    BFS(board_statex)

#print(BFS([1,2,5,3,4,0,6,7,8]))

#if method == "DFS" :
#    board_state = [int(i) for i in board_statex]    
#    DFS(board_state)
##
#else:
#    board_state = [int(i) for i in board_statex]    
#    AST(board_state)


## 1,2,5,3,4,0,6,7,8
#
#print('s')
##print(method)
##print(type(board_statex))
#board_state = []
#for i in board_statex.split(','):
#    tem = int(i)
#    board_state.append(tem)
#    
#
#if __name__ == '__main__':
#    if method == 'bfs' :
#        
#        print(board_state)
#        BFS(board_state)
#    
#    elif method == 'dfs':
##        print(board_state)
#        DFS(board_state)
#    
#    else: AST(board_state)
#     
# 	file = open('output.txt', 'w')
# 	file.write('cost_of_path: %s\n' % len(state.path_to_goal))
# 	file.write('max_search_depth: %s\n' % max_depth)
# 	file.write('running_time: %s\n' % time.time())z


'''x = PriorityQueue()
	
	for value in successors::
		priori = heur(value)
		x.put((priori,Node(value,priori)))
'''