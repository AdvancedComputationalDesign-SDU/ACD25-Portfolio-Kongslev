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

This project explores Agent-Based Modeling for Surface Panelization. The surface is generated as a heightmap-based surface, where agents are placed randomly. The movement of the agents is constrained to the surface geometry which forces them to adapt their trajectories to both the curvature of the terrain and the positions of their neighbors. The result is a self-organizing network that reflects the interaction between agents behavior and the surface geometry. This will be explored in more detail throughout the documentation of the project.

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
    - surface (surface): Rhino surface object
    - U (int): number of divisions along U direction
    - V (int): number of divisions along V direction
    - freq_u (float): frequency of wave in U direction
    - freq_v (float): frequency of wave in V direction
    - height (float): height of the waves
    
    Output:
    - srf: 

1. **Import Libraries**
   - import relevent libraries

2. **Generate Heightmap `generate_heightmap(shape, amplitude, freq_x, freq_y)`**
   - **Process:**
     - Create `x` and `y` linspace arrays
     - Make meshgrid `X, Y`
     - Compute `heightmap = sin(2π * freq_y * Y) * cos(2π * freq_x * X) * amplitude`
   - **Output:** 2D array of heights

3. **Sample Surface Uniformly `sample_surface_uniform(surface, shape)`**
   - **Process:**
     - Get U/V domains of surface
     - Create `u_vals` and `v_vals` linspace
     - Evaluate points at each `(u,v)` → store in `point_grid`
   - **Output:** 2D array of Point3d objects

4. **Manipulate Points with Heightmap `manipulate_point_grid(heightmap, point_grid)`**
   - **Process:**
     - For each point, add `heightmap[i,j]` to Z-coordinate
     - Store in `manipulated_grid`
   - **Output:** Updated 2D array of points

5. **Build Surface `build_surface(point_grid, deg_u, deg_v)`**
   - **Process:**
     - Flatten `point_grid` to list
     - Create NURBS surface through points using degrees `deg_u` and `deg_v`
    - **Output:** New NURBS surface

6. **Main**
   - Set `shape = (U, V)`
   - `heightmap = generate_heightmap(...)`
   - `pt_grid = sample_surface_uniform(...)`
   - `manip_pt_grid = manipulate_point_grid(...)`
   - `srf = build_surface(...)`
- **Output:** surface: final manipulated surface

   
### Agent builder

1. **Import Libraries**
   - import relevent libraries

2. **Define Boid Class**

   - **Attributes**
     - `position` → current 3D position on the surface
     - `velocity` → small random 3D vector
     - `done` → to stop movement if needed

   - **Initialize Boid `__init__(position)`**
     - Set initial `position`
     - give a `velocity`
     - Set `done = False`

3. **Distance and Neighbor Handling**
   - **Distance Function `dist(other)`**
     - Calculate the straight-line distance to another boid

   - **Sort Neighbors `sorted_neighbors(others)`**
     - Return all other boids sorted by distance

   - **Find Neighbors in Radius `_neighbors_in_radius(others, radius)`**
     - Loop through sorted neighbors
     - Collect boids within `radius`
     - Stop checking once distance exceeds radius

4. **Surface Constraint**
   - **Constrain to Surface `_constrain_to_surface(surface)`**
     - Find closest UV point on surface
     - Evaluate surface at that UV point
     - Update boid position to be exactly on surface

5. **Steering Forces**
   - **Separation Force `_separation_force(neighbors)`**
     - Push boid away from close neighbors
     - Stronger force when distance is small

6. **Combine Steering Behaviors `steer(others, radius, weights...)`**
   - Find neighbors within `radius`
   - generate:
     - Separation
   - Apply weights to each force
   - Add forces to the velocity
   - Limit velocity to `max_velocity`

7. **Update Boid Position `update(surface)`**
   - Add velocity to position
   - Project updated position back onto the surface

8. **Build Initial Agents `build_agents(n_agents, surface, seed)`**
   - random seed for reproducibility
   - Get surface U/V domains
   - For each boid/agents:
     - Pick random `(u, v)` on surface
     - Evaluate surface point
     - Create new Boid at that position
   - Return list of boids

9. **Grasshopper Script Execution**
   - **RunScript(N, reset, start_surface)**
     - If `reset` or no agents exist:
       - Create new agents on surface
     - For each agent:
       - Apply steering behavior
       - Update position on surface
     - Store agents for next iteration
- **Output:** agents


### Agent simulator

1. **Import Libraries**
   - import relevent libraries

2. **Access the agents**
   - Retrieve the list of agents from the agent component:
     - `boids = boids_component.agents`

3. **Update the Simulation**
   - **For** each boid in `boids`:
     - Apply steering behavior using current parameters:
       - Neighborhood radius
       - Separation
     - Update the boid’s position
     - Project the boid back onto the surface

4. **Collect Output Data**
   - Create a list of boid positions:
     - `positions = [b.position for b in boids]`
   - Create a list of boid velocity vectors:
     - `vectors = [b.velocity for b in boids]`

- **Output:** Positions and vectors

 



