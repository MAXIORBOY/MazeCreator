# Maze Creator is a program created to automatically generate solvable mazes. The only required input from a user is a size (number of rows and columns) of a maze.

## Menu:
* [Rules](#rules)
* [Algorithm](#algorithm)
* [Implementation](#implementation)
* [Expected time to generate](#expected-time-to-generate)
* [Launch](#launch)
* [Technology](#technology)
* [Sources](#sources)
* [Screenshots](#screenshots)

## Rules:
1. Every maze (generated by the program) has exactly one entry and exit point.
2. Every maze (generated by the program) is a rectangle.
3. You cannot collide with an obstacle or a wall.
4. You cannot move diagonally.

## Algorithm:
1. Create a grid filled with paths inside of the grid and with obstacles on the grid's borders. Size of the grid is provided by the user. Class ```GridCreator``` is responsible for this.  
2. Generate an entry and exit point on borders of the grid. Class ```EntryExitGenerator``` is responsible for this.   
3. Create a solution path, a path which connects the entry and exit point. Class ```SolutionPathCreator``` is responsible for this.  
4. Add internal walls into the grid. Class ```InternalWallsCreator``` is responsible for this.  
5. Connect disjointed paths. Class ```PathConnector``` is responsible for this.  
6. Make sure that the solution path is the optimal path from start to finish. Class ```SolutionPathOptimalMaker``` is responsible for this.  
7. Remove isolated paths. Class ```IsolatedPathsRemover``` is responsible for this.   
8. (Optional) Display generated maze. Class ```GridDisplay``` is responsible for this.  
9. (Optional) Save all data of the generated maze. Class ```SaveData``` is responsible for this.  

## Implementation:
```MazeGenerator.__init__(self, rows, columns, display_maze=True, save_data=True)```
* ```rows``` - (int) a desired number of rows of a maze. Must be greater or equal to 6, however values below 20 are not recommended.
* ```columns``` - (int) a desired number of columns of a maze. Must be greater or equal to 6, however values below 20 are not recommended.
* ```display_maze``` - (bool) display the maze after generation process. Default = True.
* ```save_data``` - (bool) save all necessary data about the generated maze. Default = True.  
<br>   

```MazeLoader.__init__(self, filename, display_maze=True)```
* ```filename``` - (str) full name of a file which contains data about a generated maze. Currently the formats ```.csv``` and ```.pickle``` are supported. ```csv``` save file stores only the data about a grid. ```pickle``` save file stores all data.
* ```display_maze``` - (bool) display the maze after data load. Default = True.

## Expected time to generate:
Tests were based on 10 attempts.
* 40 x 40 - 17 seconds
* 50 x 50 - 41 seconds
* 60 x 60 - 2 minutes 29 seconds
* 70 x 70 - 5 minutes 13 seconds
* 80 x 80 - 10 minutes 36 seconds

## Launch:
* To generate a new maze use the ```MazeCreator``` class and launch the ```generate_maze``` method.
* To load data of a previously generated maze use the ```MazeLoader``` class and launch the ```load_grid_from_csv``` or the ```load_data_from_pickle_file``` method.

## Technology:   
* ```Python``` 3.8  
* ```numpy``` 1.19.4  
* ```pandas``` 1.1.5
* ```matplotlib``` 3.3.3

## Sources:
* A* algorithm explanation video: https://www.youtube.com/watch?v=-L-WgKMFuhE

## Screenshots:
a yellow square - a path  
a green square - an obstacle or a wall  

* 100 x 100 example maze:
![100x100](https://user-images.githubusercontent.com/71539614/103317850-c5a6ee00-4a2c-11eb-9431-c2f1810be885.png)

* (1) 50 x 50 example maze:
![50x50-1](https://user-images.githubusercontent.com/71539614/103319074-c3df2980-4a30-11eb-86cd-b2af835ceebc.png)

* (2) 50 x 50 example maze:
![50x50-2](https://user-images.githubusercontent.com/71539614/103319073-c3469300-4a30-11eb-8a4d-d9ae6454322b.png)
