Project \#2 Light Up Solver
---------------------------

# Introduction

In this project you will work in groups of up to three to write a Python program to solve the Light Up
puzzle using a SAT solver.
In the puzzle Light Up ([http://www.nikoli.co.jp/en/puzzles/akari][akari]), you are presented with a grid with obstacles and numbers.
When lights are placed in empty spaces on the puzzle, they illuminate in each of the four directions on the grid until a wall, obstacle, or number is reached.
The object of the puzzle is to place lights such that each empty space on the grid is illuminated, no two lights can light one another, and for each
number on the grid, exactly that many lights are adjacent to that space.

[akari]:http://www.nikoli.co.jp/en/puzzles/akari.html

Your program should read in a puzzle from a textfile given as a command-line argument, encode this instance as a boolean forumula
in CNF such that satisfying assignments correspond to solutions to the puzzle, and use a SAT solver from the Python-SAT package to
find a satisfying assignment to this formula (or state that none exist).

Five puzzles have been included below (and textfiles for each are included in the starter code on github).
In each puzzle, "`.`" represents an empty space, "`X`" represents an obstacle, and each number "`0`", "`1`", "`2`", "`3`", "`4`" represents
the constraint that exactly that many lights are adjacent in a solution.

**Puzzle 1**
```
..X
.1.
```

**Puzzle 2**
```
....
.1.X
1X..
..2.
```

**Puzzle 3**
```
.0...2
...X..
2X..4.
..1...
....X.
```

**Puzzle 4** [Source][puzzle4]
```
..X...X
.4..1.X
...2...
.X...X.
...X...
X.X..1.
1...1..
```

**Puzzle 5** [Source][puzzle5]
```
X..X.....X
.......X..
.3....0...
..2..X...1
...10X....
....1XX...
X...2..2..
...X....X.
..1.......
0.....1..0
```

[puzzle4]: http://www.nikoli.co.jp/en/puzzles/akari.html 
[puzzle5]: https://en.wikipedia.org/wiki/Light_Up_(puzzle)

Given a puzzle as described above, a correct program will either output that no solution exists, or print a solution with the lights represented as `O`.
For example, given Maze 4 above, a correct program outputs the following.
```
.OX..OX
O4O.1.X
.O.2O..
.X.O.X.
...X..O
X.XO.1.
1O..1O.
```

## Writeup

Along with submitting your code, your group must also submit a 1--2 page writeup that contains the following:
  * A description of the problem.
  * A Formal description of your encoding of this problem in SAT.
  * A discussion of your implementation.

## Checkpoint

As a project checkpoint, you must schedule a time for your group to meet with me to discuss your
initial implementation and your plans for the project by Friday, October 28. Note that you should
have _at least_ the initial code for your program implemented and a good idea of your SAT formulation of the problem
by this meeting, and you should be prepared to discuss your plans for finishing the
project. Failure to schedule and attend this meeting will result in a penalty on your project
grade.

## Submission

Make sure to commit to your team's github repository as you make changes to your project. The project is due Friday, November 4 at 11:59 PM. (Note that as stated in the syllabus projects can be submitted up to two days late for a 10% penalty each day.) A complete
submission consists of the following files.
  * Your writeup as a single PDF file, which must be named `project2.pdf`.
  * Your source code as `lightup.py`.
  * A short textfile that describes how to run your program as `readme.txt`. This _must_ clearly state how to input a puzzle for your program to solve.
  * Your discussion log as `discussion.txt`.

When you are ready to submit your assignment, create a "Release" on github. This will tag the commit
and make a downloadable archive of the state of the files. I will grade the most-recent release created
within the deadline (or late deadline when submitting late). Note that if you are using github throughout your
development process, you should only need to create your release once for the deadline, since your incremental
progress will be saved in the commit history.

## Grading
  * Correctness/Efficiency of program to solve LightUp using a SAT solver: 50 points
  * Code clarity/style: 20 points.
  * Writeup: 30 points.

Programming Style: You will be graded
not only on whether your program works correctly, but also on
programming style, such as the use of informative names, good
comments, easily readable formatting, and a good balance between
compactness and clarity (e.g., do not define lots of unnecessary
variables). Create appropriate
functions for tasks that can be encapsulated.
