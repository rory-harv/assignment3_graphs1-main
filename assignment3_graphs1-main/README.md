# assignment3_graphs1
new repo for assignment 3 
(README for Project2 Above Assignment 3 README)

Project 2 - Oregon Pathfinder

Name: Rory Harvey

Part A. Program Usage Instructions

-> The code will initially prompt the user to make a choice on what algorithm they would like to perform on their graph data. Then, after the choice, said algorithm will run and produce a desired path between two inputted vertices (start and goal). The code will then prompt the user as to whether or not they would like to continue using the pathfinder, or terminate the code. 

-> When prompted, the user inputs a command into the terminal for their choice of algorithm. They will be prompted with 3 choices of algorithms, and depending on their input (1-3), said corresponding algorithm wull be initiated. 

-> Example Runs:
-- -------------------------------------------------------------------------------------

Select Pathfinding Algorithm:
1 Dijkstra's Algorithm
2 Greedy Best-First Search
3 A* Algorithm
Enter Choice (1-3): 1
Enter the start vertex name: Salem
Enter the goal vertex name: Newport
Path from Salem to Newport: 
-> Salem
-> Portland
-> Newport

Total Distance Travelled: 164.0 miles
Total Vertices Explored: 6
Total Edges Explored: 20
Execution Time: 0.00019659986719489098 seconds

Would you like to use Oregon Pathfinder again (y/n)?: n
Thank you for using Oregon Pathfinder!

------------------------------------------------------------------------------------

Select Pathfinding Algorithm:
1 Dijkstra's Algorithm
2 Greedy Best-First Search
3 A* Algorithm
Enter Choice (1-3): 2
Enter the start vertex name: Corvallis
Enter the goal vertex name: Astoria
Path from Corvallis to Astoria: 
-> Corvallis
-> Newport
-> Tillamook
-> Seaside
-> Astoria

Total Distance Travelled: 210.0 miles
Total Vertices Explored: 13
Total Edges Explored: 35
Execution Time: 0.008388799848034978 seconds

Would you like to use Oregon Pathfinder again (y/n)?: n
Thank you for using Oregon Pathfinder!

-- ----------------------------------------------------------------------------------

Select Pathfinding Algorithm:
1 Dijkstra's Algorithm
2 Greedy Best-First Search
3 A* Algorithm
Enter Choice (1-3): 3
Enter the start vertex name: Pendleton
Enter the goal vertex name: Bend
Path from Pendleton to Bend: 
-> Pendleton
-> The_Dalles
-> Madras
-> Redmond
-> Bend

Total Distance Travelled: 265.0 miles
Total Vertices Explored: 7
Total Edges Explored: 15
Execution Time: 0.003787300083786249 seconds

Would you like to use Oregon Pathfinder again (y/n)?: n
Thank you for using Oregon Pathfinder!

-- ---------------------------------------------------------------------------------

Part B. Algorithm Analysis




------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
Assignment 3:

Name: Rory Harvey 

DFS -> searches graph data using a stack to track information about the graph (edges, vertices). creates adjacency lists and determines which vertices to add to the overall output for the search depending on whether or not they have been previously visited by searching vertices' adjacency lists.

BFS -> searches graph data using a queue to track information about the graph (edges, vertices). creates adjacency lists for each vertex, and determines which vertices to add to the overall output for the search depending on if they have been previously visited.

Instructions: run program.py file for desired DFS and BFS outputs based on inputted text file path name.
-> IF FileNotFoundError OCCURS: worked w/Prof. Cordova to resolve issue, but still somehow present when attempting to run the assignment from full repo
    -> Solution: open starter folder (NOT entire repo) and run program.py file, use python debugger if necessary. 

Design Decisions: double checking if vertices are already present in the output array due to the fact that they would be added twice when reviewing a new adj_list otherwise. 


Input: graph.txt file

Depth First Search Outputs:

Enter the start vertex name: Salem
Salem
Portland
Eugene
Corvallis
Newport
Tillamook
Florence
Coos_Bay
Roseburg
Medford
Ashland
Crater_Lake
Seaside
Astoria
Bend
Redmond
Burns
Madras
The_Dalles
Hood_River
Pendleton
Ontario

Breadth First Search Outputs:

Enter the start vertex name: Salem
Salem
Portland
Eugene
Corvallis
Astoria
Hood_River
Newport
Bend
Crater_Lake
Roseburg
Seaside
The_Dalles
Tillamook
Florence
Redmond
Burns
Medford
Coos_Bay
Pendleton
Madras
Ontario


