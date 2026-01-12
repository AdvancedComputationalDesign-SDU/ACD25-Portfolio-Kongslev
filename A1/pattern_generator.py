# Assignment 1: NumPy Array Manipulation for 2D Pattern Generation


import numpy as np
import matplotlib.pyplot as plt

import os
if not os.path.exists("images"):
    os.makedirs("images")


# Creating a numpy array filled with zeros to create the size of the canvas
height = 500  #height of the canvas
width = 500   #width of the canvas
canvas = np.zeros((height, width, 3), dtype=np.uint8) #3 channels for RGB
#print(canvas)

#-------creating a black empty canvas (showed as an image)------
# Save black empty canvas
plt.figure()
plt.imshow(np.zeros((height, width, 3), dtype=np.uint8))
plt.axis('off')
plt.title("Black empty canvas")
plt.savefig('images/black_empty_canvas1.png', bbox_inches='tight', pad_inches=0)
plt.close()
plt.show()


# -------Creating a pattern using array----------
# pattern with horizontal stripes:
for i in range(0, height, 40):  # jumps forward by 40 pixels
    canvas[i:i+15, :] = 255     # color 15 pixels white in height

# creating a canvas with horizontal stripes
plt.figure()
plt.imshow(canvas)
plt.axis('off')
plt.title("Horizontal stripes")
plt.savefig('images/stripes_pattern.png', bbox_inches='tight', pad_inches=0)
plt.close()


# -------Creating random noise pattern----------
canvas = np.random.choice([0, 255], size=(height, width)) #choosing the size of the canvas with random black and white pixels
canvas_noise = np.stack([canvas, canvas, canvas], axis=2) #keeping it to RGB chanel as the assignments above

# Creating a grapic canvas with random noise pattern in black and white 
plt.figure()
plt.imshow(canvas_noise)
plt.axis('off')
plt.title("Random noise pattern")
plt.savefig('images/noise_pattern.png', bbox_inches='tight', pad_inches=0)
plt.close()


#----- Working with RGB channels------

# Creating an empty RGB canvas
RGB_canvas = np.zeros((height, width, 3), dtype=float)

# placing the location of the center point acording to x and y axis
center_x = width // 2 # could also be fx 5 to make it off center
center_y = height // 2

# Maximum distance from the center to the corner
max_distance = np.sqrt(center_x**2 + center_y**2)

# Creating a loop
for y in range(height): #loop over the height of the canvas
    for x in range(width): #loop over the width of the canvas
        # these two loops ensure that we go through every pixel in the canvas

# calculating the distance from the point to the center of the canvas
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)

#normalizing the distance so it will always be between 0 and 1
        normalized_distance = distance / max_distance  

        # Assigning the color based on the normalized distance
        if normalized_distance <= 0.5:
            # From 0 to 0.5: go from red to green
            color_transition = normalized_distance / 0.5
            RGB_canvas[y, x] = [1-color_transition, color_transition, 0]  # R to G
        else:
            # From 0.5 to 1: go from green to blue
            color_transition = (normalized_distance - 0.5) / 0.5
            RGB_canvas[y, x] = [0, 1-color_transition, color_transition]  # G to B


# Creating a graphic illustration of the distance-based gradient
plt.figure()
plt.imshow(RGB_canvas)
plt.axis('off')
plt.title("Distance-based RGB gradient")
plt.savefig('images/RGB_channel_pointinmid.png', bbox_inches='tight', pad_inches=0)
plt.close()


# -------Distance map combined with noise-------

# Create coordinate grid
y, x = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')

# Center point (same logic as before)
center_x = width // 2
center_y = height // 2

# Distance from center
distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)

# Normalize distance to range 0–1
max_distance = np.sqrt(center_x**2 + center_y**2)
normalized_distance = distance / max_distance


# Create random noise (values between 0 and 1)
noise = np.random.rand(height, width)

# Combine distance and noise
#combined = normalized_distance * (distance_weight + noise_weight * noise)
combined = normalized_distance * (0.6 + 0.4 * noise)
combined = np.clip(combined, 0, 1)


# Create RGB canvas
RGB_combined = np.zeros((height, width, 3))

# Color transition masks
# 0.5 = Midpoint of the gradient: the point where the color changes from red→green to green→blue
mask1 = combined <= 0.5
mask2 = combined > 0.5

# Red → Green
RGB_combined[mask1, 0] = 1 - (combined[mask1] / 0.5)
RGB_combined[mask1, 1] = combined[mask1] / 0.5

# Green → Blue
RGB_combined[mask2, 1] = 1 - ((combined[mask2] - 0.5) / 0.5)
RGB_combined[mask2, 2] = (combined[mask2] - 0.5) / 0.5


# Display and save the combined image
plt.figure()
plt.imshow(RGB_combined)
plt.axis('off')
plt.title("Distance gradient combined with noise")
plt.savefig('images/distance_noise_combined.png', bbox_inches='tight', pad_inches=0)
plt.close()
