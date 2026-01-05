---
layout: default
title: Project Documentation
parent: "A4: Agent-Based Modeling for Surface Panelization"
nav_order: 2
nav_exclude: false
search_exclude: false
---

# Assignment 4: Agent-Based Modeling for Surface Panelization

[View on GitHub]({{ site.github.repository_url }})

![Example Structural Panelization](images/agent_based.jpg)

## Objective

In this assignment, you will develop an **agent-based system for surface rationalization** using **Object-Oriented Programming (OOP)** in Python. Building on the surface you generated in Assignment 3 (or a comparable heightmap-driven surface), you will design agents that respond to geometric signals and collectively produce **panelization patterns**. The core idea is that agents move, interact, and make decisions based on how they sample the geometry, and their trajectories and interactions become the basis for a rationalized panelization of that surface.

Your implementation must incorporate **at least two types of geometric signals** (chosen from curvature, slope, vector fields, scalar fields, and spatial influences) when defining agent behavior. The primary outputs of this assignment are: (1) a rationalized panelization of your surface and (2) simulated agent trajectories and fields that you document and analyze.

---

## Repository Structure

```
A4/
├── index.md                    # Do not edit front matter or content
├── README.md                   # Project documentation; Keep front matter, replace the rest with your project documentation
├── BRIEF.md                    # Assignment brief; Do not edit front matter or content
├── agent_panelization.gh       # Your grasshopper definition
├── surface_generator.py        # Your surface_generator implementation
├── agent_builder.py            # Your agent_builder implementation
├── agent_simulator.py          # Your agent_simulator implementation
├── ...                         # Any additional implementation
└── images/                     # Add diagram, intermediary, and final images here
    ├── agent_based.png         # Assignment brief image; Do not delete
    └── ...
```
## Table of Contents

- [Project Overview](#project-overview)
- [Pseudo-Code](#pseudo-code)
- [Technical Explanation](#technical-explanation)
- [Design Variations](#design-variations)
- [Challenges and Solutions](#challenges-and-solutions)
- [AI Acknowledgments](#ai-acknowledgments)
- [References](#references)

---
## Project Overview

This project explores Agent-Based Modeling for Surface Panelization. The surface is generated as a heightmap-based mesh, where agents are placed randomly. The agents move from point to point across the surface with the goal of reaching the point farthest from their starting position. During their movement, the agents follow two main rules: they move more slowly on steep areas and faster on flat areas.

The agents' movement is recorded as trajectories, which can be used as a basis for panelization. The result is a non-uniform structure that reflects the agents' local decisions and adapts to the geometry of the surface. This will be explored in more detail throughout the documentation of the project.

---

## Pseudo-Code
This project consist of three python moduls:

- `surface_generator.py` — base surface generation using a NumPy heightmap.
- `agent_builder.py` — agent class definitions and agent initialization.
- `agent_simulator.py` — simulation loop and visualization. 

The pseudo-code for each module is described in detail below.

### Surface generator (heightmap)

1. **Setting up the python component**

    Input:
    - srf (surface): Rhino surface object
    - U (int): number of divisions along U direction
    - V (int): number of divisions along V direction
    - amp (float): amplitude, maximum height displacement
    - freq_u (float): frequency of wave in U direction
    - freq_v (float): frequency of wave in V direction
    - heightmap_type (int): 
        - 0 = sinusoidal 
        - 1 = radial + noise
    - seed (int): random seed for reproducibility
    
    Output:
    - pts_tree: containing the displaced 3D points 
    - edges: line objects representing the wireframe
    - mesh: mesh constructed from quad faces (tesselation 1) 
    - tri_mesh: mesh constructed from triangular faces (tesselation 2)
    
2. **Define Heightmap generation logic**
    - Initialize random seed to ensure reproducibility
    - Get Surface Domains for both U and V directions (start and end parameters)
    - Create coordinate grids by generating evenly spaced values across the U and V domains
    - **If** heightmap_type is 0 (Sinusoidal):
        - Calculate height (H) using a sinewave based on U/V frequencies and amplitude

    - **Else** if heightmap_type is 1 (Radial + Noise):
        - Find the center point of the U and V domains
        - Calculate the radial distance from each grid point to the center
        - Normalize distances and calculate a radial falloff (fading from center)
        - Generate a random noise array and combine it with the radial falloff and amplitude

3. **Sample Surface and apply displacement**
    - **For** each coordinate pair in the U and V grids:
        - Evaluate the surface to find the 3D base point
        - Calculate the surface normal (the perpendicular direction) at that point
        - Extract the corresponding height value from the heightmap
        - Move point: Create a new 3D point by moving the base point along the normal vector by the height value
    - Store these displaced points in a 2D list (rows and columns).

4. **Generate grid edges**
    - **For** every row and column in the point grid:
        - If there is a neighbor in the U direction:
            - Create a line (edge) between the current point and the next point in the row.
        - If there is a neighbor in the V direction:
            - Create a line (edge) between the current point and the next point in the column.

5. **Construct quad mesh (tesselation 1)**
    - Flatten the 2D point grid into a 1D list of vertices.
    - **For** each cell in the grid (excluding the last row/column):
        - Identify the four corner indices (A, B, C, D) of the current cell.
        - Define a quad face using these four indices.
    - Assemble the mesh using all vertices and quad faces.

6. **Construct triangulated mesh (tesselation 2)**
    - Use the same flattened list of vertices.
    - **For** each cell in the grid:
        - Identify the four corner indices (A, B, C, D).
    - Split the quad into two triangles:
        - Triangle 1: Connect indices A, B, and C.
        - Triangle 2: Connect indices A, C, and D.
    - Assemble the mesh using all vertices and the resulting triangular faces.

7. **Final Execution and Output**
    - Run the heightmap and sampling functions to generate the displaced points.
    - Convert the point list into a DataTree
    - Return the point tree, the list of edges, the quad mesh, and the triangular mesh.