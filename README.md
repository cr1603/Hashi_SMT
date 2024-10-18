# Charlotte_thesis

# Topic: Solving and generating puzzles with a connectivity constraint

## Puzzles:
1. Hashi
2. Masyu

### Hashi
**Connectivity constraint:**
All islands must be connected to each other

**Other constraints:**
1. at most, two bridges can be drawn between two islands
2. the number of bridges connected to an island must correspond to the number shown on the respective island
3. the numbers on the islands range from 1 to 8
4. bridges can only be drawn horizontally or vertically
5. bridges cannot cross each other


### Masyu
**Connectivity constraint:**
The drawn line must create a continuous loop at the end

**Other constraints:**
1. the drawn lines cannot cross each other
2. there are no branches to the line (if stretched the line would become a rectangle/circle)
3. the line goes through all black and white pearls
4. white pearls are always crossed straight through, but the line turns in the previous OR the next cell
5. black pearls are always turned upon, but the line crosses straight through the previous AND the next cell
