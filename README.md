# Regret-Based Algorithm for Single Machine Scheduling

## Overview
In single machine scheduling problems with setup times dependent on the sequence of tasks, the total time varies based on the order of operations. This code aims to find the optimal job sequence that minimizes total time using a Regret based Algorithm and a Branch and Bound Method.

## Code Description
The code consists of three main components:
- `class RegretAlgorithm`: Implements the Regret Algorithm to find the optimal Hamiltonian path and the minimum total time (Cmax) for N tasks, based on an NxN matrix of setup times.
- `stack.py`: A module implementing a stack using a linked list, used in the DFS process.
- `class RegretBBAlgorithm(RegretAlgorithm)`: Enhances RegretAlgorithm with a DFS-based Branch and Bound method to verify the optimality of the solution.

### Class RegretAlgorithm
- Handles an NxN matrix of setup times, with options for either user-defined or randomly generated matrices.
- Implements the regret calculation to choose the best next step and update the total cost (Cmax).
- Manages job sequences to avoid sub-tours and ensure a connected path.

### Module: Stack
- Implements a stack data structure using linked lists, facilitating the DFS process.

### Class Regret + Branch and Bound Algorithm
- Inherits from `RegretAlgorithm` and uses the `StackLink` from the stack module for DFS.
- Adds a `branch()` method to store lower bound values in each iteration.
- Uses `optimality_check()` to traverse bounds via DFS and confirm the global optimality of the final Cmax value.

## Example
Demonstrates the combined Regret and Branch and Bound Algorithm for a random 4x4 matrix. The final Cmax of 23 is verified as the global optimum through DFS traversal of all bounds.

![Single Machine Scheduling Result](/images/result.png "Scheduling Result")

