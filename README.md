# Frequency Reuse Game
A simple game developed using Tkinter in Python for understanding cellular frequency reuse to find co-channel cells in a given cellular system.

Enter non-negative values for `i` and `j`, then select any cell as a starting point. Once selected the goal to select all immediate co-channel cells for the given cell where the given group of channels can be used again. `N`, calculated using `i` and `j`, gives us the number of cells in a cluster. The minimum adjacent set cells which each use different frequencies is called a cluster. The value of `N` is a function of how much interference a mobile or base station can tolerate while maintaining a sufficient quality of communications.

The value N is calculated by: `N = i^2 + i*j + j^2`

Once cells are selected, user can click `Finish` to view the correct cells and gets assigned a score based on how many correct cells were identified.

To find the nearest co-channel neighbours of a particular cell,
1. Move `i` cells along any chain of hexagons.
2. Turn 60 degrees counter-clockwise and move `j` cells.

Made in October 2021.

#### References:
https://github.com/noobien/pytk-hexagon-grid  
http://vlabs.iitkgp.ernet.in/fcmc/exp6A/index.html  
https://www.redblobgames.com/grids/hexagons/  

#### Screenshots:

![sample](/sample.png?raw=true)
