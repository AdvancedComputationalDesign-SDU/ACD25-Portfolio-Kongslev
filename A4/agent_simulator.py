"""
Assignment 4: Agent-Based Model for Surface Panelization

Author: Freja Kongslev

Agent Simulator 

Description:
This file defines the structural outline for stepping and visualizing
agents within Grasshopper. No simulation logic is implemented. All behavior
(update, responding to signals, movement, etc.) must be
implemented inside your Agent class in `agent_builder.py`.

Note: This script is intended to be used within Grasshopper's Python
scripting component.
"""

import rhinoscriptsyntax as rs

#----Get the agents from the previous component----
boids = boids_component.agents

#-----update each boid/agent--------
for b in boids:
    # Apply steering forces with weights and radius provided from inputs
    b.steer(boids, rad, sep, coh, ali)
    
    # update agent position and project it onto the surface
    b.update(surface) 

# Outputs
positions = [b.position for b in boids]
vectors = [b.velocity for b in boids]