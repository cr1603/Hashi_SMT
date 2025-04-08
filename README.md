# Topic: Solving and generating puzzles with a connectivity constraint

This project solves the Hashi puzzle with the SMT solver cvc5. It can also generate puzzles.

## Puzzle:
Hashi

### Hashi
**Connectivity constraint:**
All islands must be connected to each other

**Other constraints:**
1. at most, two bridges can be drawn between two islands
2. the number of bridges connected to an island must correspond to the number shown on the respective island
3. the numbers on the islands range from 1 to 8
4. bridges can only be drawn horizontally or vertically
5. bridges cannot cross each other


## How this project works
1. You need an SMT solver in the same folder as all the files in this project. This project was written to run cvc5.
2. To solve a puzzle, you need an input file in a folder "input" in the same folder as the other files in this project. For the easiest way to run this project, the input file is named test{number}.txt. In run_project.py, change test_to_run to the corresponding number.
3. There is no need to change anything to generate puzzles
4. Follow the instructions on the console (enter s for solve, g for generate, numbers for width and height)
5. Have fun!
