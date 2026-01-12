"""
Assignment 4: Agent-Based Model for Surface Panelization

Author: Freja Kongslev

Surface Generator 

Description:
This file defines the structural outline for generating or preprocessing
surfaces and geometric signal fields for Assignment 4.

Note: This script is intended to be used within Grasshopper's Python
scripting component.
"""

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import numpy as np


# ----Parameters------

# Inputs from Grasshopper:
# surface   : Rhino Surface to be sampled
# U         : Number of points in U direction
# V         : Number of points in V direction
# height    : Maximum displacement in Z direction
# freq_x    : Number of wave repetitions in X direction
# freq_y    : Number of wave repetitions in Y direction
# degree_u  : Degree of the Nurbs surface in U direction
# degree_v  : Degree of the Nurbs surface in V direction

# default numbers if no input in grasshopper
if "freq_x" not in globals(): freq_x = 2
if "freq_y" not in globals(): freq_y = 2
if "degree_u" not in globals(): degree_u = 3
if "degree_v" not in globals(): degree_v = 3


# ---Heightmap generation-------
def generate_heightmap(shape=(50,50), amplitude=1.0, freq_x=2, freq_y=2):
    rows, cols = shape
    # rows correspond to V direction, cols correspond to U direction
    
    # Normalize coordinates
    x = np.linspace(0, 1, cols)
    y = np.linspace(0, 1, rows)

    # Creates a 2D grid of X and Y coordinates
    X, Y = np.meshgrid(x, y)

    # creating a Sin/Cos wave pattern
    heightmap = np.sin(2 * np.pi * freq_y * Y) * np.cos(2 * np.pi * freq_x * X) * amplitude
    return heightmap


#------Uniform surface sampling-----
def sample_surface_uniform(surface, shape=(50,50)):
    rows, cols = shape
    u_domain = surface.Domain(0) #domain in U direction
    v_domain = surface.Domain(1) #domain in V direction

    #space out the U and V
    u_vals = np.linspace(u_domain.T0, u_domain.T1, cols)
    v_vals = np.linspace(v_domain.T0, v_domain.T1, rows)
    
    point_grid = np.empty((rows, cols), dtype=object)
    for i, v in enumerate(v_vals):
        for j, u in enumerate(u_vals):
            point_grid[i, j] = surface.PointAt(u, v)
    return point_grid


#----Apply heightmap to points-------

def manipulate_point_grid(heightmap, point_grid):
    rows, cols = heightmap.shape

    # Stores the displaced points
    manipulated_grid = np.empty((rows, cols), dtype=object)
    for i in range(rows):
        for j in range(cols):
            pt = point_grid[i, j]
            manipulated_grid[i, j] = rg.Point3d(pt.X, pt.Y, pt.Z + heightmap[i, j])
    return manipulated_grid


#------Build NURBS surface from points-----
def build_surface(point_grid, deg_u=3, deg_v=3):
    rows, cols = point_grid.shape

    # Flattens the 2D grid into a single point list
    points_flat = [point_grid[i, j] for i in range(rows) for j in range(cols)]
    srf = rg.NurbsSurface.CreateThroughPoints(
        points_flat,
        rows,
        cols,
        deg_u,
        deg_v,
        False,
        False
    )
    return srf


#-------MAIN EXECUTION--------
shape = (U, V)
heightmap = generate_heightmap(shape=shape, amplitude=height, freq_x=freq_x, freq_y=freq_y)

pt_grid = sample_surface_uniform(surface, shape=shape)

manip_pt_grid = manipulate_point_grid(heightmap, pt_grid)

srf = build_surface(manip_pt_grid, deg_u=degree_u, deg_v=degree_v)

#output: rebuild surface from displaced points 