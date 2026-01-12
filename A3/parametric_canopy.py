"""
Assignment 3: Parametric Structural Canopy — Pseudocode Scaffold

Author: Freja Kongslev

    This file is a **high-level pseudocode**.
    It outlines the pipeline and function responsibilities. 
    Use it as a guide and fill in the bodies with your own logic.
"""

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import ghpythonlib.treehelpers as th
import math
import numpy as np


# ------Heightmap generation

def generate_heightmap(surface, U, V, amp, freq_u, freq_v, heightmap_type, seed):
    # Ensures same random result each time for same seed
    np.random.seed(seed)

    # Get surface parameter domains
    du0, du1 = rs.SurfaceDomain(surface, 0)  # U direction
    dv0, dv1 = rs.SurfaceDomain(surface, 1)  # V direction

    # Create evenly spaced values in U and V directions
    u_vals = np.linspace(du0, du1, U + 1)
    v_vals = np.linspace(dv0, dv1, V + 1)

    # Create 2D grids of U and V values
    U_grid, V_grid = np.meshgrid(u_vals, v_vals, indexing='ij')

    
    # Heightmap type 0: sinusoidal 
    # Creates a smooth wave pattern using sine functions in U and V directions
    if heightmap_type == 0:
        H = amp * np.sin(freq_u * U_grid) * np.sin(freq_v * V_grid)


    # Heightmap type 1: Radial + noise

    elif heightmap_type == 1:
        # Creates a smooth wave pattern using sine functions in U and V directions
        center_u = (du0 + du1) * 0.5
        center_v = (dv0 + dv1) * 0.5

        # Radial distance
        #Computes radial distance from the center for each grid point
        R = np.sqrt((U_grid - center_u)**2 + (V_grid - center_v)**2)

        # Normalize radial distance (0–1)
        R_norm = R / np.max(R)

        # Center fade 
        # Makes displacement strongest at the center and weaker toward the edges
        radial_falloff = 1.0 - R_norm

        # Noise between -0.5 and +0.5
        noise = np.random.rand(*R.shape) - 0.5

        # Combine radial structure + noise
        H = amp * radial_falloff * noise

    return U_grid, V_grid, H


#-------Combine surface with the heightmap-----------

def sample_surface_with_heightmap(surface, U_grid, V_grid, H):
    pts = []

    for i in range(H.shape[0]): # Loop over U direction
        row = []
        for j in range(H.shape[1]): # Loop over V direction

            # Evaluate surface point
            pt = rs.EvaluateSurface(surface, U_grid[i, j], V_grid[i, j])

            # Get surface normal at that point
            normal = rs.SurfaceNormal(surface, (U_grid[i, j], V_grid[i, j]))

            # Height from heightmap
            h = H[i, j]

            # Move point along normal
            new_pt = rg.Point3d(
                pt[0] + normal[0] * h,
                pt[1] + normal[1] * h,
                pt[2] + normal[2] * h
            )

            row.append(new_pt)

        pts.append(row)

    return pts



#------ Sample the uniform grid (no heightmap)------
def sample_uniform_grid(surface, U, V):
    
    # access to where the domain begin and ends:
    du0, du1 = rs.SurfaceDomain(surface, 0) #0 is evaluating along the U direction
    dv0, dv1 = rs.SurfaceDomain(surface, 1) # 1 is evaluating along the V direction
   
    # how to tell if we are at the start og end of the domain
    pu = [du0 + (du1 - du0)*(i/float(U)) for i in range(U+1)]
    pv = [dv0 + (dv1 - dv0)*(i/float(V)) for i in range(V+1)]

    pts = []

    for u in pu:
        row = []
        for v in pv:
            tmp_pt = rs.EvaluateSurface(surface, u, v)
            row.append(tmp_pt)
        pts.append(row)
    return pts


# ----Create quad edges------
def quad_edges_from_points(pts):
    U = len(pts)-1
    V = len(pts[0])-1

    lines = []

    for i in range(U+1):
        for j in range(V+1):
            if i < U: #vertical line
                tmp_line = rs.AddLine(pts[i][j], pts[i+1][j])
                lines.append(tmp_line)
            if j < V: # horizontal line
                tmp_line = rs.AddLine(pts[i][j], pts[i][j+1])
                lines.append(tmp_line)
    
    return lines


# ----Create quad mesh from points-----
def quad_mesh_from_points(pts):
    
    rows = len(pts)
    cols = len(pts[0])
    
    #Flattens the 2D grid into a single vertex list
    vertices = [pts[i][j] for i in range(rows) for j in range(cols)]

    faces = []
    vcols = cols

    for i in range(rows - 1):
        for j in range(cols - 1):
            a = i * vcols + j
            b = a + 1
            c = b + vcols
            d = c - 1
            faces.append([a, b, c, d]) #Each quad is defined by four vertex indices

    mesh = rs.AddMesh(vertices, faces)
    return mesh


# -----Create triangular mesh from points------
def tri_mesh_from_points(pts):
    rows = len(pts)
    cols = len(pts[0])

    # Flatten 2D point grid into vertex list
    vertices = [pts[i][j] for i in range(rows) for j in range(cols)]

    faces = []
    vcols = cols

    for i in range(rows - 1):
        for j in range(cols - 1):

            a = i * vcols + j
            b = a + 1
            c = b + vcols
            d = a + vcols

            # Split each quad into two triangles
            faces.append([a, b, c])
            faces.append([a, c, d])

    mesh = rs.AddMesh(vertices, faces)
    return mesh


# -----Move the mesh up along the normals
def move_mesh_up(mesh, offset):
    # Ensures vertex normals are available
    mesh.Normals.ComputeNormals()

    new_vertices = []
    for i in range(mesh.Vertices.Count):
        v = mesh.Vertices[i]
        normal = mesh.Normals[i]
        new_v = rg.Point3d(
            v.X + normal.X * offset,
            v.Y + normal.Y * offset,
            v.Z + normal.Z * offset
        )
        new_vertices.append(new_v)

    # Creates a new mesh instead of modifying the original
    new_mesh = rg.Mesh()
    new_mesh.Vertices.AddVertices(new_vertices)
    new_mesh.Faces.AddFaces(mesh.Faces)
    new_mesh.Normals.ComputeNormals()
    new_mesh.Compact()
    return new_mesh


###----MAIN EXECUTION----###
#print("U value: ", U, ": V value ", V)

# 1. Generate heightmap
U_grid, V_grid, H = generate_heightmap(
    srf,
    U,
    V,
    amp,
    freq_u,
    freq_v,
    heightmap_type,
    seed
)

# 2. apply heightmap to the surface
pts = sample_surface_with_heightmap(srf, U_grid, V_grid, H)

# 3. create a quad mesh
mesh_guid = quad_mesh_from_points(pts)

# 4. convert the mesh to RhinoCommon Mesh
mesh_obj = rs.coercemesh(mesh_guid)

# 5. offset the mesh along normals
mesh_obj = move_mesh_up(mesh_obj, support_height)

# 6. Output mesh
mesh = mesh_obj

# 7. convert points to a grasshopper data tree
pts_tree = th.list_to_tree(pts)

# 8. Create quad edges for visualization
edges = quad_edges_from_points(pts)

# 9. Create triangular mesh for alternative tesselation
tri_mesh = tri_mesh_from_points(pts)
