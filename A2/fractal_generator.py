"""
Assignment 2: Fractal Generator

Author: Freja Kongslev

Description:
This script generates fractal patterns using recursive functions and geometric transformations.
"""
import os
if not os.path.exists("images"):
    os.makedirs("images")

# Import necessary libraries
import math
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import random

# creating random seed for reproducibility
random.seed(100)
branch_list = []

#------creating spatial Influence: Attractor-----
# defining a fixed attractor point
attractor_point = (200, 100) 

# --- generating the fractal function ----
def generate_fractal(start_point, angle, length, depth, max_depth, angle_change, length_scaling_factor):
    """
    Parameters for the fractal generation:
    start_point: Where the branch begins.
    angle: The direction the branch is growing.
    length: How long the current branch is.
    depth: A counter that tracks how many times we have branched.
    max_depth: The limit that tells the code when to stop.
    angle_change: How much the branch tilts left or right when it splits.
    length_scaling_factor: How much shorter each new branch becomes.
    """
    
    if depth > max_depth:
        return

    # --- Attractors------
    # finding the distance and direction from the branch start to the attractor
    dx = attractor_point[0] - start_point[0]
    dy = attractor_point[1] - start_point[1]
    angle_to_attractor = math.degrees(math.atan2(dy, dx))
    
    # adding the strength towards the attractor point
    steering_strength = 0.25 #make it higher for stronger attraction
    angle = angle + (angle_to_attractor - angle) * steering_strength


    # --- New branch calculation ------
    # Calculate the point from where the next branch will start
    end_x = start_point[0] + length * math.cos(math.radians(angle))
    end_y = start_point[1] + length * math.sin(math.radians(angle))
    end_point = (end_x, end_y) # the new branch coordinates

    # --- Defining line segments ---
    branch = LineString([start_point, end_point])
    branch_list.append((branch, depth))

    # Update the length for the next recursion
    new_length = length * length_scaling_factor

    # Increment depth
    next_depth = depth + 1

    # --- control over randomness---
    random_noise = random.uniform(-5, 5)

    # Recursive calls for branches
    generate_fractal(end_point, angle + angle_change + random_noise, new_length, next_depth, max_depth, angle_change, length_scaling_factor)
    generate_fractal(end_point, angle - angle_change + random_noise, new_length, next_depth, max_depth, angle_change, length_scaling_factor)

# ---MAIN EXECUTION--------
if __name__ == "__main__":
    # Parametre
    start_point = (0, 0)
    initial_angle = 90 
    initial_length = 50 
    max_recursion_depth = 10 
    angle_change = 15
    length_scaling_factor = 0.75

    branch_list.clear()

    # Generate the fractal
    generate_fractal(start_point, initial_angle, initial_length, 0, max_recursion_depth, angle_change, length_scaling_factor)
    
    # ---Visualization-----
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # draw the attractor as a point
    ax.scatter(*attractor_point, color='red', s=200, zorder=5)

    for branch, depth in branch_list:
        x, y = branch.xy
        thickness = max(0.5, (max_recursion_depth - depth) * 0.5)
        ax.plot(x, y, color='green', linewidth=thickness, alpha=0.7)

    ax.set_aspect('equal')
    ax.legend()
    plt.axis('off') 
    plt.margins(0.1)
    plt.show()
    
    fig.savefig('images/output_1', dpi=300, bbox_inches='tight')

    