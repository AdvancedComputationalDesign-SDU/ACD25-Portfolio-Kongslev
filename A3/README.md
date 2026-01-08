---
layout: default
title: Project Documentation
parent: "A3: Parametric Structural Canopy"
nav_order: 2
nav_exclude: false
search_exclude: false
---

# Assignment 3: Parametric Structural Canopy

[View on GitHub]({{ site.github.repository_url }})

![Example Canopy](images/canopy.jpg)

## Objective

In this assignment you will design and generate a **parametric structural canopy** in **Grasshopper** using the **GhPython (Python 3)** component. You will combine: (1) a **NumPy-driven heightmap** that modulates a NURBS surface, (2) **tessellation** of the resulting surface, and (3) **recursive, branching vertical supports** with controlled randomness. Your goal is to produce a small **family of design solutions** by varying parameters and algorithms, then communicate your process and results in a clear, reproducible report. You are asked to present **three** visually distinct designs. Each design must vary at least **two** of the implemented computational logic (heightmap-based surface geometry, tessellation strategy, branching supports).

---

## Repository Structure

```
A3/
├── index.md                    # Do not edit front matter or content
├── README.md                   # Project documentation; Keep front matter, replace the rest with your project documentation
├── BRIEF.md                    # Assignment brief; Do not edit front matter or content
├── parametric_canopy.py        # Your code implementation
├── parametric_canopy.gh        # Your grasshopper definition
└── images/                     # Add diagram, intermediary, and final images here
    ├── canopy.png              # Assignment brief image; Do not delete
    └── ...
```
``
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
This project explores the generation of a parametric canopy structure. The canopy surface is created as a heightmap-based mesh using NumPy. Structural supports are placed beneath the canopy to carry the surface, which functions as a roof. From these supports, branching elements are generated using a recursive growth algorithm inspired by natural tree structures. The methods for this will be explained in detail throughout the project documentation.
---

## Pseudo-Code
This project consist of two python moduls but has been combined for the documentation in the file: `parametric_canopy.py`
the two modules consist of:

- `surface_generator.py` — base surface generation using a NumPy heightmap.
- `support_generator.py` — support generation using branching logic.

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
    - support_height(float): height of the surface 
    
    Output:
    - pts_tree: containing the displaced 3D points 
    - edges: line objects representing the wireframe
    - mesh: mesh constructed from quad faces (tesselation 1) 
    - tri_mesh: mesh constructed from triangular faces (tesselation 2)
    

2. **Define heightmap generation logic**
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

3. **Combine surface with the heightmap**
    - **For** each coordinate pair in the U and V grids:
        - Evaluate the surface to find the 3D base point
        - Calculate the surface normal (the perpendicular direction) at that point
        - Extract the corresponding height value from the heightmap
        - Move point: Create a new 3D point by moving the base point along the normal vector by the height value
    - Store these displaced points in a 2D list (rows and columns)

4. **Generate Uniform Grid**
    - combine the surface with evenly spaced U and V parameters
    - Store the surface points as a flat reference grid

5. **Tesselation strategy**
    - Convert the structured grid of points into discrete geometric elements.
    - Connect neighboring points to form a wireframe grid (edges).
    - Group sets of four neighboring points to create quad faces (tessellation 1)
    - split each quad into two triangles to generate a triangular tessellation (tessellation 2)

6. **Move the final mesh (using offset)**
    - Take the generated mesh and calculate the direction each part is facing
    - Push every vertex of the mesh upwards by a specific support_height
    - Rebuild the mesh at this new offset position.

7. **Main execution: Output**
    - Convert the data into a format Rhino can display .
    - output: 
        - the mesh 
        - the triangular mesh
        - the wireframe edges
        - the point structure 


### Support generator (tree like structure)

1. **Setting up the python component**

    Input:
    - gen (int): generator, cotrole the growth
    - len (int): length of the support
    - angle (float): number of divisions along V direction
    - mesh (mesh): mesh from the surface generator module
    - offset_ratio (float): placement of the supports 
    - base_offset (float):  
    
    Output:
    - lines: support structure lines 
 
1. **creating the branching (growth) logic** 
    - define the grow using:
        - pt = starting point
        - V = growth direction vector
        - len = current segment length
        - g = current generation
    - **if** reached the maximum number of generations (the limit):
        - Stop the grow

    - intersection with mesh: 
        - find the closest point on the mesh 
        - calculate the distance
        - **if** distance to mesh < Len * 0.3 (0.3 can be changed) 
            - stop the grow
    
    - grow in random directions:
        - Create a random tilt to make the branching look organic
        - Calculate two new paths (Branch A and Branch B) by rotating away from the main direction.

    - Create the lines:
    - Place two new points at the end of the paths
    - Draw a line from the start to each new point

2. **Repeat (Recursion)**
    - Start the "Grow" logic again from the new points
        - For every new step, make the length slightly shorter

3. **Calculate the placement of the support**
    - find the lowest point on the mesh bounding box 
    - For each of the 4 support positions:
        - Find the midpoint of the mesh.
        - Move out toward the corners, but use an **offset ratio** to keep them inside the edges
        - Place the start point below the canopy

4. **Create the support structure**
    - for each of the 4 calculated start positions:
        - Step A: Draw a vertical line (the trunk) straight up.
        - Step B: Start the Grow logic (from Step 1) from the top of that trunk

5. **output to rhino**
- output = lines (support structure)
- connect the line output to a pipe component to visulize the structure

---

## Technical Explanation

In this assignment, i started by creating a blank (black) RGB canvas, i choose to keep the canvas in RGB from the begining because i knew i had to use the RGB color channel later on in the assignment. i created the blank canvas using `np.zeros()`. 

to create a striped pattern on the canvas i used slicing to define the stripes: `canvas[i:i+15, :]= 255`and after this creating a `for`loop to repet the pattern

---

## Design Variations

*(Include images and descriptions of your generated design variations. For each category, provide at least three variations and discuss the differences and design decisions.)*

### Parameter Tables
*(Provide the exact parameter sets and seeds used for each design. Add or remove columns to reflect your implementation.)*

| Design | amplitude | freq_u | freq_v| divU | divV | heightmap_type | seed | gen | len | angle | tessellation | 
|-------:|----------:|-------:|------:|-----:|-----:|---------------:|-----:|----:|----:|------:|-------------:|
| A      |10         |1.6     |type 1 | 15   | 15   |type 1          |-     |7    |9    |15     |quad          |
| B      |10         |1.6     |type 1 | 15   | 15   |type 1          |-     |7    |9    |15     |tri           |
| C      |-          |-       |type 0 | 15   | 15   |type 0          |29    |7    |9    |15     |quad          |
| D      |10         |1.6     |type 1 | 15   | 15   |type 1          |-     |6    |10   |31     |quad          |

> If you vary algorithms (e.g., quad vs. tri tessellation, heightmap function swap), note that explicitly in an **Algorithm Notes** column or footnote.

1. **Variation A: [Name/Description]**

   ![Variation A](images/canopy.jpg)

   *Figure 1: black empty canvas*
