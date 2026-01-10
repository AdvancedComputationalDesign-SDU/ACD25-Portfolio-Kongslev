---
layout: default
title: Project Documentation
parent: "A2: Exploring Fractals through Recursive Geometric Patterns"
nav_order: 2
nav_exclude: false
search_exclude: false
---

# Assignment 2: Exploring Fractals through Recursive Geometric Patterns

[View on GitHub]({{ site.github.repository_url }})

![Example Fractal](images/branching.png)

## Objective

In this assignment you will implement a **recursive generator** and enrich it with **geometric influences** that shape how the structure grows in space. You will work with geometric primitives (lines, polylines) using **Shapely** and render the results (e.g., with Matplotlib). The core of the assignment is to **couple formal grammar growth with spatial rules** such as attractor/repulsor points, fields, and collision constraints to produce expressive, controllable patterns.

While the branching or growth approach can be inspired by L-systems, it does not have to be strictly L-system based. You are encouraged to explore recursive generation methods influenced by spatial constraints and geometric rules that govern how the fractal develops and interacts with its environment. This opens opportunities to experiment with recursive branching logic, adaptive scaling, and spatial modulation beyond formal grammar rewriting.

---

## Repository structure

```
A2/
├── index.md                    # Do not edit front matter or content
├── README.md                   # Project documentation; Keep front matter, replace the rest with your project documentation
├── BRIEF.md                    # Assignment brief; Do not edit front matter or content
├── fractal_generator.py        # Your code implementation
└── images/                     # Add diagram, intermediary, and final images here
    ├── branching.png           # Assignment brief image; Do not delete
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
---

---

## Technical Explanation

In this assignment, i started by creating a blank (black) RGB canvas, i choose to keep the canvas in RGB from the begining because i knew i had to use the RGB color channel later on in the assignment. i created the blank canvas using `np.zeros()`. 

to create a striped pattern on the canvas i used slicing to define the stripes: `canvas[i:i+15, :]= 255`and after this creating a `for`loop to repet the pattern

---

## Design Variations

*(Include images and descriptions of your generated design variations. For each category, provide at least three variations and discuss the differences and design decisions.)*

### Parameter Tables
*(Provide the exact parameter sets and seeds used for each design. Add or remove columns to reflect your implementation.)*

| Design | attractorpoint | length | max depth| angle | scaling factor | strength | 
|-------:|---------------:|-------:|---------:|------:|---------------:|---------:|
| A      |200,100         |50      |10        |15     |0.75            |0.25      |
| B      |0,200           |40      |10        |45     |0.65            |0.05      |
| C      |100,100         |60      |9         | 90    | 0.55           |0.1       |
| D      |150,200         |30      |12        |25     |0.82            |0.15      |

> If you vary algorithms (e.g., quad vs. tri tessellation, heightmap function swap), note that explicitly in an **Algorithm Notes** column or footnote.

1. **Variation A: [Strong steering and narrow angles]**


   ![Variation A](images/output_1.png)

   *This version looks like a tree shaped by strong wind. By moving the attractor far to the right and turning up the steering strength, the branches are forced to grow in one specific direction.*


2. **Variation B: [Large branch angles and moderate scaling]**


   ![Variation A](images/output_2.png)

   *This version looks like a wide and symatric tree. I used a large angle change to make it spread out horizontally. The attractor is placed directly above to keep the growth symmetrical and upright.*

3. **Variation C: [90-degree angles]**


   ![Variation A](images/output_3.png)

   *This version is more sharp and abstract. By setting the angle to exactly 90 degrees, the tree turns into a more mathematical pattern than a natural one.*

4. **Variation D: [High depth and long branches]**


   ![Variation A](images/output_4.png)

   *this version is a very dense and more complex structure. I increased the recursion depth and kept the branches long to create a more dense branching structure that still crawls toward the attractor point.*