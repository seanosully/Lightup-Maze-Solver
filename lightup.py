# lightup.py
#
# Sean, Kyle, Tristan
# Prof. Fitzsimmons
# Artificial Intelligence
# Project 2 
# 
# Description: Akari puzzle solver using SAT solver
# 
# Usage: python3 lightup.py puzzle{number}.txt
# 
import sys
from pysat.solvers import Glucose3
from itertools import combinations


def read_file(filename): 
    print("reading " + filename)
    x = 0
    y = 0
    obstacles = []

    puzzle = open(filename)

    puzzleArray = []
    zeros = []
    ones = []
    twos = []
    threes =[]
    fours = [] 
    numRows = 0 
    print("Unsolved Puzzle:")
    for row in puzzle:
        for char in row:
            if char == '0': 
                zeros.append((x,y))  # stored in tuple

            if char == '1':
                ones.append((x,y))  # stored in tuple

            if char == '2':
                twos.append((x,y))  # stored in tuple

            if char == '3':
                threes.append((x,y))  # stored in tuple

            if char == '4':
                fours.append((x,y))  # stored in tuple

            if char == 'X':
                obstacles.append((x,y))  # obstacle not in tuple because it is only one square
            y = y+1
        y = 0
        x = x+1

        row = row.rstrip('\n')
        puzzleArray.append(row) 
        print (row)  # print the unsolved maze 
        numRows += 1
    print()
    return puzzleArray, zeros, ones, twos, threes, fours, obstacles, numRows

# Makes sure that no two lights ae shining are on each other
def rowcol_rules(rows,cols,obstacles,zeros,ones,twos,threes,fours,gridVariables,phi):
    for r in range(rows):
        prevBarrier = 0       # trackers for when barriers are hit and where to index from
        lastBarrier=0
        barrier = False       
        for c in range(cols):
            if (((r,c) in obstacles) or ((r,c) in zeros) or ((r,c) in ones) or ((r,c) in twos) or ((r,c) in threes) or ((r,c) in fours)):
                phi.add_clause([-1*gridVariables[r,c]]) # some sort of barrier hit, make that false 
                barrier = True                          # set new indicies from barrier 
                lastBarrier = c
                for pair in combinations(range(prevBarrier, lastBarrier), 2): # for every combination of squares before the last barrier 
                    phi.add_clause([-1*gridVariables[r,pair[0]], -1*gridVariables[r,pair[1]]])
                prevBarrier = lastBarrier # set prev barrier 
        if barrier is False: # if no barrier is hit then do the combinations 
            for pair in combinations(range(cols), 2): 
                phi.add_clause([-1*gridVariables[r,pair[0]],-1*gridVariables[r,pair[1]]]) 
        barrier = False
        for colPair in combinations(range(lastBarrier+1, cols), 2): # for every combination past the last barrier til the end --> no more barriers in col
            phi.add_clause([-1*gridVariables[r,colPair[0]], -1*gridVariables[r,colPair[1]]])
    
    for c in range(cols):
        prevBarrier = 0   # barrier trackers reset
        lastBarrier=0
        barrier = False
        for r in range(rows):  #traverse the rows in a constant col
            if (((r,c) in obstacles) or ((r,c) in zeros) or ((r,c) in ones) or ((r,c) in twos) or ((r,c) in threes) or ((r,c) in fours)):
                phi.add_clause([-1*gridVariables[r,c]]) # obstacle hit  
                barrier = True                          
                lastBarrier = r
                for pair in combinations(range(prevBarrier,lastBarrier),2): # for each pair of combinations from the range of the prev barrier to the last barrier 
                    phi.add_clause([-1*gridVariables[pair[0],c], -1*gridVariables[pair[1],c]])
                prevBarrier = lastBarrier
        if barrier is False:                                                # if no barrier is found then do every combination of squares in the row
            for pair in combinations(range(rows), 2):
                phi.add_clause([-1*gridVariables[pair[0],c],-1*gridVariables[pair[1],c]])
        barrier = False 
        
        for rowPair in combinations(range(lastBarrier+1, rows), 2):  #for each pair of rows past the barrier, add new clause 
            phi.add_clause([-1*gridVariables[rowPair[0],c], -1*gridVariables[rowPair[1],c]])
            

# Makes sure that every square is properly lit up 
def light_rules(rows,cols,obstacles,zeros,ones,twos,threes,fours,gridVariables,phi):
    for r in range(rows):
        for c1 in range(cols):
            if not (((r,c1) in obstacles) or ((r,c1) in zeros) or ((r,c1) in ones) or ((r,c1) in twos) or ((r,c1) in threes) or ((r,c1) in fours)):
                currentRule=[]
                cc= c1
                for rr in range(r,rows): # goes right and makes sure the squares are illuminated properly
                    if (((rr,cc) in obstacles) or ((rr,cc) in zeros) or ((rr,cc) in ones) or ((rr,cc) in twos) or ((rr,cc) in threes) or ((rr,cc) in fours)):
                        break
                    if (gridVariables[(rr,cc)] not in currentRule):
                        currentRule.append(gridVariables[(rr,cc)])
                cr= r
                for cd in range(c1, cols): # goes up and makes sure the squares are illuminated properly
                    if (((cr,cd) in obstacles or ((cr,cd) in zeros) or ((cr,cd) in ones) or ((cr,cd) in twos) or ((cr,cd) in threes) or ((cr,cd) in fours))):
                        break
                    if (gridVariables[(cr,cd)] not in currentRule):
                        currentRule.append(gridVariables[(cr,cd)])
                cc= c1
                for rl in range(r, -1, -1): # goes left and makes sure the squares are illuminated properly
                    if (((rl,cc) in obstacles) or ((rl,cc) in zeros) or ((rl,cc) in ones) or ((rl,cc) in twos) or ((rl,cc) in threes) or ((rl,cc) in fours)):
                        break
                    if (gridVariables[(rl,cc)] not in currentRule):
                        currentRule.append(gridVariables[(rl,cc)])
                cr= r
                for cu in range(c1, -1, -1): # goes down and makes sure the squares are illuminated properly
                    if (((cr,cu) in obstacles) or ((cr,cu) in zeros) or ((cr,cu) in ones) or ((cr,cu) in twos) or ((cr,cu) in threes) or ((cr,cu) in fours)):
                        break
                    if (gridVariables[(cr,cu)] not in currentRule):
                        currentRule.append(gridVariables[(cr,cu)])
                    
                phi.add_clause(currentRule)        
                currentRule= [] # reset 

# Returns list of adjacent gridVariables values and positions for a given (row,col).  
def neighbors(grid,row,col,obs,zero,one,two,three,four): 
    neighbors = []
    # each conditional keeps the addition and subtraction of the rows and cols inbounds
    if  ((row + 1 < rows) and (grid[(row+1,col)] > 0) and (((row+1,col) not in obs) or ((row+1,col) not in zero) or ((row+1,col) not in one) or ((row+1,col) not in two) or ((row+1,col) not in three) or ((row+1,col) not in four))):
        neighbors.append(grid[(row+1,col)]) # right neighbor
    if  ((col + 1 < cols) and (grid[(row,col+1)] > 0) and (((row,col+1) not in obs) or ((row,col+1) not in zero) or ((row,col+1) not in one) or ((row,col+1) not in two) or ((row,col+1) not in three) or ((row,col+1) not in four))):
        neighbors.append(grid[(row,col+1)]) # below neighbor
    if  ((row - 1 >= 0) and (grid[(row-1,col)] > 0) and (((row-1,col) not in obs) or ((row-1,col) not in zero) or ((row-1,col) not in one) or ((row-1,col) not in two) or ((row-1,col) not in three) or ((row-1,col) not in four))):
        neighbors.append(grid[(row-1,col)]) # left neighbor
    if  ((col - 1 >= 0) and (grid[(row,col-1)] > 0) and (((row,col-1) not in obs) or ((row,col-1) not in zero) or ((row,col-1) not in one) or ((row,col-1) not in two) or ((row,col-1) not in three) or ((row,col-1) not in four))):
        neighbors.append(grid[(row,col-1)]) # above neighbor 
    
    return neighbors

#Implements clauses based on the assigned number in the puzzle
def number_rules(rows,cols,obs,zero,one,two,three,four,gridVariables,phi):
    for r in range(rows):
        for c in range(cols):
            adjacent= neighbors(gridVariables,r,c,obs,zero,one,two,three,four) # get adjacent square values 
            if ((r,c) in four):
                if len(adjacent)<4: # not enough squares to satisfy the condition
                    sys.exit("No Solution! ")
                else: # make every square true
                    phi.add_clause([adjacent[0]])
                    phi.add_clause([adjacent[1]])
                    phi.add_clause([adjacent[2]])
                    phi.add_clause([adjacent[3]])
                phi.add_clause([-1*gridVariables[r,c]])
            elif ((r,c) in three): #  3's case
                if len(adjacent)<3:
                    sys.exit("No Solution! ")
                elif len(adjacent)== 3: # 3 adjacent squares are all true
                    phi.add_clause([adjacent[0]])
                    phi.add_clause([adjacent[1]])
                    phi.add_clause([adjacent[2]])
                else: # combinations of 3 lamps surrounding the number
                    phi.add_clause([adjacent[0],adjacent[1],adjacent[2],adjacent[3]])
                    phi.add_clause([adjacent[0],adjacent[1],adjacent[2],-1*adjacent[3]])
                    phi.add_clause([adjacent[0],adjacent[1],-1*adjacent[2],adjacent[3]])
                    phi.add_clause([adjacent[0],-1*adjacent[1],adjacent[2],adjacent[3]])
                    phi.add_clause([-1*adjacent[0],adjacent[1],adjacent[2],adjacent[3]])
                    phi.add_clause([adjacent[0],adjacent[1],-1*adjacent[2],-1*adjacent[3]])
                    phi.add_clause([adjacent[0],-1*adjacent[1],adjacent[2],-1*adjacent[3]])
                    phi.add_clause([-1*adjacent[0],adjacent[1],adjacent[2],-1*adjacent[3]])
                    phi.add_clause([adjacent[0],-1*adjacent[1],-1*adjacent[2],adjacent[3]])
                    phi.add_clause([-1*adjacent[0],adjacent[1],-1*adjacent[2],adjacent[3]])
                    phi.add_clause([-1*adjacent[0],-1*adjacent[1],adjacent[2],adjacent[3]])
                    phi.add_clause([-1*adjacent[0],-1*adjacent[1],-1*adjacent[2],-1*adjacent[3]])
                phi.add_clause([-1*gridVariables[r,c]])
            elif ((r,c) in two): # 2's case 
                if len(adjacent)<2:
                    sys.exit("No Solution! ")
                if len(adjacent)==2: # 2 adjacent squares are true
                    phi.add_clause([adjacent[0]])
                    phi.add_clause([adjacent[1]])
                elif len(adjacent)==3: # 2 lights must be true with 3 valid adjacent squares
                    phi.add_clause([adjacent[0],adjacent[1],adjacent[2]])
                    phi.add_clause([-1*adjacent[0],adjacent[1],adjacent[2]])
                    phi.add_clause([adjacent[0],-1*adjacent[1],adjacent[2]])
                    phi.add_clause([adjacent[0],adjacent[1],-1*adjacent[2]])
                    phi.add_clause([-1*adjacent[0],-1*adjacent[1],-1*adjacent[2]])
                else: # 2 lights must be true with 4 valid adjacent squares
                    phi.add_clause([adjacent[0],adjacent[1],adjacent[2], adjacent[3]])
                    phi.add_clause([adjacent[0],adjacent[1],adjacent[2], -1*adjacent[3]])
                    phi.add_clause([adjacent[0],adjacent[1],-1*adjacent[2], adjacent[3]])
                    phi.add_clause([adjacent[0],-1*adjacent[1],adjacent[2], adjacent[3]])
                    phi.add_clause([-1*adjacent[0],adjacent[1],adjacent[2], adjacent[3]])
                    phi.add_clause([-1*adjacent[0],-1*adjacent[1],-1*adjacent[2], adjacent[3]])
                    phi.add_clause([-1*adjacent[0],-1*adjacent[1],adjacent[2], -1*adjacent[3]])
                    phi.add_clause([-1*adjacent[0],adjacent[1],-1*adjacent[2], -1*adjacent[3]])
                    phi.add_clause([adjacent[0],-1*adjacent[1],-1*adjacent[2], -1*adjacent[3]])
                    phi.add_clause([-1*adjacent[0],-1*adjacent[1],-1*adjacent[2], -1*adjacent[3]])
                    
                phi.add_clause([-1*gridVariables[r,c]]) 

            elif ((r,c) in one): #ones case 
                if len(adjacent)<1: # no neighbors
                    sys.exit("No Solution! ")
                elif len(adjacent)==1: # one neighbor is true 
                    phi.add_clause([adjacent[0]])
                elif len(adjacent)==2: # two neighbors and one must be true 
                    phi.add_clause([-1*adjacent[0],-1*adjacent[1]])
                    phi.add_clause([adjacent[1],adjacent[0]])
                elif len(adjacent)==3: # three neighbors with one light being true 
                    phi.add_clause([-1*adjacent[0],-1*adjacent[1], -1*adjacent[2]])
                    phi.add_clause([adjacent[0],-1*adjacent[1], -1*adjacent[2]])
                    phi.add_clause([-1*adjacent[0],adjacent[1], -1*adjacent[2]])
                    phi.add_clause([-1*adjacent[0],-1*adjacent[1], adjacent[2]])
                    phi.add_clause([adjacent[0],adjacent[1], adjacent[2]])
                    
                else: # four neighbors and one light should be true
                    phi.add_clause([adjacent[0],adjacent[1], adjacent[2],adjacent[3]])

                    phi.add_clause([adjacent[0],adjacent[1], -1*adjacent[2],-1*adjacent[3]])
                    phi.add_clause([adjacent[0],-1*adjacent[1], adjacent[2],-1*adjacent[3]])
                    phi.add_clause([-1*adjacent[0],adjacent[1], adjacent[2],-1*adjacent[3]])
                    phi.add_clause([adjacent[0],-1*adjacent[1], -1*adjacent[2],adjacent[3]])
                    phi.add_clause([-1*adjacent[0],adjacent[1], -1*adjacent[2],adjacent[3]])
                    phi.add_clause([-1*adjacent[0],-1*adjacent[1], adjacent[2],adjacent[3]])

                    phi.add_clause([-1*adjacent[0],-1*adjacent[1], -1*adjacent[2],adjacent[3]])
                    phi.add_clause([-1*adjacent[0],-1*adjacent[1], adjacent[2],-1*adjacent[3]])
                    phi.add_clause([-1*adjacent[0],adjacent[1], -1*adjacent[2],-1*adjacent[3]])
                    phi.add_clause([adjacent[0],-1*adjacent[1], -1*adjacent[2],-1*adjacent[3]])
                    phi.add_clause([-1*adjacent[0],-1*adjacent[1], -1*adjacent[2],-1*adjacent[3]])
                    
                phi.add_clause([-1*gridVariables[r,c]])

            elif ((r,c) in zero): #zeroes case 
                for i in adjacent: # all adjacent squares should not be lights 
                    phi.add_clause([-1*i])
                phi.add_clause([-1*gridVariables[r,c]])

def main():  
    if len(sys.argv) != 2: # make sure user inputs correct amount of arguments, otherwise exit
        print("Usage: python3 lightup.py puzzleFile")
        sys.exit(1)
    else: 
        global cols               # declare global so rows and cols can be used as global values
        global rows
        puzzleFile = sys.argv[1]
        puzzleArray,zerosLocation, onesLocation,twosLocation,threesLocation,foursLocation,obstacles,rows = read_file(puzzleFile) # read file in 
        cols = len(puzzleArray[0]) # this is how many columns there are 
        
        #print(puzzleArray,zerosLocation,onesLocation,twosLocation,threesLocation,foursLocation,obstacles,rows,cols) # print to make sure everything was being read correctly 
        val = 1
        output = {}
        gridVariables = dict()
        for r in range(rows): # number of rows 
            for c in range(cols): # number of columns
                if ((r,c) in zerosLocation) or ((r,c) in onesLocation) or ((r,c) in twosLocation) or ((r,c) in threesLocation) or ((r,c) in foursLocation) or ((r,c) in obstacles): 
                    # If not a '.', then it should be a false square
                    gridVariables[(r,c)] = -1*val
                    output[val] = (r,c)
                else: # otherwise true     
                    gridVariables[(r,c)] = val
                    output[val] = (r,c)
                val += 1
        
        phi = Glucose3() # start solving the puzzle with these rule functions 
        number_rules(rows,cols,obstacles,zerosLocation,onesLocation,twosLocation,threesLocation,foursLocation,gridVariables,phi)
        light_rules(rows,cols,obstacles,zerosLocation,onesLocation,twosLocation,threesLocation,foursLocation,gridVariables,phi)
        rowcol_rules(rows,cols,obstacles,zerosLocation,onesLocation,twosLocation,threesLocation,foursLocation,gridVariables,phi)
    
    count = 0
    phi.solve()
    m = phi.get_model() # print solution
    if m == None: # if no models found, then No Solution! 
        sys.exit("No Solution Found!")
    else: 
        print("Solution:") # print out the solution 
        for r in range(rows):
            for c in range(cols):
                if(gridVariables[(r,c)] in m):
                    print("O",end="")
                elif((r,c) in obstacles):
                        print("X",end="")
                elif((r,c) in zerosLocation):
                    print("0",end="")
                elif((r,c) in onesLocation):
                    print("1",end="")
                elif((r,c) in twosLocation):
                    print("2",end="")
                elif((r,c) in threesLocation):
                    print("3",end="")
                elif((r,c) in foursLocation):
                    print("4",end="")
                else:
                    #print(rrows,cols)
                    print(".",end="")
            print()
        print()

    for s in phi.enum_models(): # increment count for however  models there are
        count +=1
    print("Total number of models: %d" %(count))
if __name__ == "__main__":
    main()