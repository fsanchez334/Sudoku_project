# -*- coding: utf-8 -*-
"""SudokuProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GZ0U9WB7oA8bacy8x6iUc3WSpbARt6Ww

## Step 1: Importing libraries
First, we import the libraries that we need to complete the project
"""

import numpy as np
from collections import defaultdict
import heapq

"""## Step 2: Defining the Sudoku Class
In this step, we define the Sudoku object. The board will be represent by a standard 9 X 9 board. We include important member variables such as the possible values we can choose from, as well as the length of the board.

We also include five member functions - each has their appropriate descriptions below
"""

class Sudoku:
  def __init__(self, starter):
    self.board = np.reshape(np.array(starter), (9, 9))
    self.length = len(self.board)
    self.options = set([x for x in range(1, 10)])

  def make_centers(self):
    #Here, we first make the centers
      proxy = (1, 1)
      stack = [proxy]
      collections_core = []
      center_tracker = defaultdict(lambda: [])
      for i in range(4):
        collections_core.append(stack[-1])
        for j in range(2):
            current_coor = stack.pop()
            other = (current_coor[0], current_coor[1] + 3)
            collections_core.append(other)
            stack.append(other)
        proxy = (proxy[0] + 3, proxy[1])
        stack.append(proxy)
      self.coordinates_appendix = defaultdict()
      for coordinate in collections_core:
        one = (coordinate[0] - 1, coordinate[1] - 1)
        two = (coordinate[0] - 1, coordinate[1])
        three = (coordinate[0] - 1, coordinate[1] + 1)
        four = (coordinate[0], coordinate[1] - 1)
        five = (coordinate[0], coordinate[1] + 1)
        six = (coordinate[0]+ 1, coordinate[1] - 1)
        seven = (coordinate[0] + 1, coordinate[1])
        eight = (coordinate[0] + 1, coordinate[1] + 1)
        container = {one, two, three, four, five, six, seven, eight}
        keys_ = {one: coordinate, two: coordinate, three: coordinate, 
                four: coordinate, five: coordinate, six: coordinate,
                seven: coordinate, eight: coordinate, coordinate:coordinate}
        center_tracker[coordinate]
        self.coordinates_appendix.update(keys_)
      return center_tracker
      

  def check_centers(self, coordinate):
    #Here we check what center the coordinate belongs to
    home_center = self.coordinates_appendix[coordinate]
    return home_center    

  def iteration(self):
    value_tracker = defaultdict(lambda: [])
    center_tracker = self.make_centers()
    for idx, x in np.ndenumerate(self.board):
      if idx in self.coordinates_appendix.values():
        center_tracker[idx].append(x)
        continue
      else:
        #Now check, what center coordinate belongs to
        home_center = self.check_centers(idx)
        center_tracker[home_center].append(x)

    for idx, x in np.ndenumerate(self.board):
      if x != 0:
        continue
      else:
        column = set(self.board[:, idx[1]])
        row = set(self.board[idx[0], :])
        container = column.union(row) #Shows values present in the rows and columns of a particular coordinate
        if 0 in container:
          container.remove(0)
        home_center = self.check_centers(idx)
        boxer_values = set(center_tracker[home_center])
        container = container.union(boxer_values)
        #Now, we need the values we can actually use for every coordinate
        valid_options = self.options.difference(container)
        #We then have to remove the options that are present in the squares
        #1st: Check which square the coordinate belongs to
        value_tracker[idx] = valid_options
    return value_tracker

  def make_move(self, index, value):
    self.board[index[0]][index[1]] = value

  def is_solved(self):
    shaper = self.board.flatten()
    if 0 in shaper:
      return False
    else:
      return True

"""## Step 3: Additional Helper Functions
The functions that follow are additional ones that can help us organize our work and analysis

"""

def no_moves(value_tracker):
  #Checks to see if an index has no available options
  for value in value_tracker.values():
    if len(value) == 0:
      return True
  return False
    

def index_queue(value_tracker):
  #Determine what order of indices we are going to fill out -> Minimum Remaining Value Heuristic
  heaper = []
  heapq.heapify(heaper)
  for key, value in value_tracker.items():
    heapq.heappush(heaper, (len(value), key))
  return heaper

#First: Pop off the queue to see which index to pop
def next_move(dictionary, queue, board):
  candidate_coor = heapq.heappop(queue)[1]
  #Now, access the value for this
  value = dictionary[candidate_coor].pop()
  #Now, get place the value into the appropriate spot
  board.make_move(candidate_coor, value)

def solve(boarder):
  tracker = boarder.iteration()
  if boarder.is_solved() or no_moves(tracker):
    print(boarder.board)
    return boarder.board
  else:
    queue = index_queue(tracker)
    coordinate = heapq.heappop(queue)[1]
    value = tracker[coordinate].pop()
    boarder.make_move(coordinate, value)
    solve(boarder)
    boarder.make_move(coordinate, 0)

"""## Step 4: Defining the Main Function"""

starter = "000260701680070090190004500820100040004602900050003028009300074040050036703018000"
start = [int(x) for x in starter]
boarder = Sudoku(start)
answer = solve(boarder)
answer