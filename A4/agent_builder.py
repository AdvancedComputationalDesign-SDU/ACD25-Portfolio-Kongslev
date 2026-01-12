"""
Assignment 4: Agent-Based Model for Surface Panelization

Author: Freja Kongslev

Agent Builder Template

Description:
Defines the core Agent class and factory methods for constructing an
agent-based system. Provides a high-level OOP structure for sensing,
decision-making, and movement, along with a stateful Grasshopper
GH_ScriptInstance example.

Note: This script is intended to be used within Grasshopper's Python
scripting component.
"""



# Imports 
import rhinoscriptsyntax as rs
import random
import numpy as np

import Grasshopper
import random
import rhinoscriptsyntax as rs

#---- Defining the agent (Boild class)
class Boid(object):
    def __init__(self, position):
        # Current position of the agent (stored as a list)
        self.position = position

        # Initial velocity
        self.velocity = [
            random.uniform(-0.01, 0.01),
            random.uniform(-0.01, 0.01),
            random.uniform(-0.01, 0.01)
        ]
        self.done = False

    # distance between this agent and another agent
    def dist(self, other):
        return rs.Distance(self.position, other.position)

    # all agents sorted by distance from this agent
    def sorted_neighbors(self, others):
        return sorted(others, key=self.dist)

    def _neighbors_in_radius(self, others, radius):
        neighbors = []
        sorted_others = self.sorted_neighbors(others)
        for other in sorted_others:
            if other is self:
                continue
            d = self.dist(other)
            if d < radius:
                neighbors.append(other)
            else:
                break

        #Returns nearby agents within the given radius only
        return neighbors

    #------- Surface constraint ------
    def _constrain_to_surface(self, surface):
        if not surface:
            return

        # Find the closest UV point on the surface
        uv = rs.SurfaceClosestPoint(surface, self.position)
        if uv:
            # Forces the agent position to be exactly on the surface
            self.position = rs.EvaluateSurface(surface, uv[0], uv[1])

#----- defining the agents behavior 
    def _separation_force(self, neighbors, separation_radius=0.05):
        if not neighbors:
            return [0.0, 0.0, 0.0]

        # Vector pointing away from neighbor    
        steer = [0.0, 0.0, 0.0]
        for other in neighbors:
            vec = rs.VectorCreate(self.position, other.position)
            d = rs.VectorLength(vec)
            if d == 0:
                vec = [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]
                d = rs.VectorLength(vec)
            
        # Pushes agent away from nearby neighbors
            t = max(0.0, min(d / separation_radius, 1.0))
            inv_t = 1.0 - t
            vec = rs.VectorUnitize(vec)
            vec = rs.VectorScale(vec, inv_t)
            steer = rs.VectorAdd(steer, vec)
        return steer

#----- this part is not really used in this project ---
# but the code keeps breaking when i remove it
    def _cohesion_force(self, neighbors):
        if not neighbors:
            return [0.0, 0.0, 0.0]
        center = [0.0, 0.0, 0.0]
        for other in neighbors:
            center = rs.VectorAdd(center, other.position)
        center = [c / float(len(neighbors)) for c in center]
        desired = rs.VectorCreate(center, self.position)
        if rs.VectorLength(desired) == 0:
            return [0.0, 0.0, 0.0]
        return rs.VectorUnitize(desired)

    def _alignment_force(self, neighbors):
        if not neighbors:
            return [0.0, 0.0, 0.0]
        avg_vel = [0.0, 0.0, 0.0]
        for other in neighbors:
            avg_vel = rs.VectorAdd(avg_vel, other.velocity)
        avg_vel = [v / float(len(neighbors)) for v in avg_vel]
        if rs.VectorLength(avg_vel) == 0:
            return [0.0, 0.0, 0.0]
        return rs.VectorUnitize(avg_vel)

#------------------------------------------------------------------------


#------Steering combination-------
    def steer(self, others, radius, separation_weight=1.0, cohesion_weight=1.0, alignment_weight=1.0, max_velocity=0.02):
        neighbors = self._neighbors_in_radius(others, radius)
        
        sep = self._separation_force(neighbors)
        coh = self._cohesion_force(neighbors)
        ali = self._alignment_force(neighbors)

        steer_vec = [0.0, 0.0, 0.0]
        steer_vec = rs.VectorAdd(steer_vec, rs.VectorScale(sep, separation_weight))
        steer_vec = rs.VectorAdd(steer_vec, rs.VectorScale(coh, cohesion_weight))
        steer_vec = rs.VectorAdd(steer_vec, rs.VectorScale(ali, alignment_weight))

        self.velocity = rs.VectorAdd(self.velocity, steer_vec)
        if rs.VectorLength(self.velocity) > max_velocity:
            self.velocity = rs.VectorUnitize(self.velocity)
            self.velocity = rs.VectorScale(self.velocity, max_velocity)

#--------Update the step--------
    def update(self, surface):
        if not self.done:
            # Moves the agent forward using its velocity
            self.position = rs.VectorAdd(self.position, self.velocity)
            self.position = list(self.position)

            # Projects agent back onto the surface
            self._constrain_to_surface(surface)


#------Agent initialization-----
def build_agents(n_agents, surface, seed=None):
    if seed is not None:
        random.seed(seed)
    
    agents = []
    if not surface: return agents
    
    domainU = rs.SurfaceDomain(surface, 0)
    domainV = rs.SurfaceDomain(surface, 1)
    
    for _ in range(n_agents):
        u = random.uniform(domainU[0], domainU[1])
        v = random.uniform(domainV[0], domainV[1])
        point = rs.EvaluateSurface(surface, u, v)
        if point:
            agents.append(Boid(list(point)))
    return agents


#-----grasshopper component----------
class MyComponent(Grasshopper.Kernel.GH_ScriptInstance):
    def RunScript(self, N: int, reset: bool, start_surface):

        # Initializes or resets the agent system
        if reset or not hasattr(self, "agents") or self.agents is None:
            self.agents = build_agents(N, start_surface)
        
        # Computes steering forces
        for agent in self.agents:
            agent.steer(self.agents, radius=0.1) 
        
            #Moves agent and constrains it to the surface
            agent.update(start_surface)
            
        return self