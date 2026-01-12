---
layout: default
title: Project Documentation
parent: "A1: NumPy Array Manipulation for 2D Pattern Generation"
nav_order: 2
nav_exclude: false
search_exclude: false
---

# Assignment 1: NumPy Array Manipulation for 2D Pattern Generation



# Documentation for Assignment 1

This is the documentation of assignment 1. where the focus was on using NumPy Array Manipulation for 2D Pattern Generation

## Table of Contents

- [Pseudo-Code](#pseudo-code)
- [Technical Explanation](#technical-explanation)
- [Results](#results)
- [References](#references)

---

## Pseudo-Code

1. **Setting up the canvas**
   - Set canvas dimensions (height and width).
   - create an empty canvas filled with zeros (working in RGB).

2. **Display empty black canvas**
   - use **Matplotlib** to show the black canvas
   - add a title to the canvas
   - turn off the axis 


3. **create a horizontal striped pattern**
   - **For** every 40 pixels down the image
         - color the next 15 pixels in white
   - use **Matplotlib** to show the striped canvas
   - add a title to the canvas
   - turn off the axis 

4. **Create a noise pattern using random**
   - Create a 2D array of random values containing either 0 (black) or 255 (white)
   - Stack the array into 3 layers representing RGB
   - use **Matplotlib** to show the striped canvas
   - add a title to the canvas
   - turn off the axis 

5. **Create a color gradient based on distance**
   - Make a new empty RGB canvas
   - Define the center point of the image (middle of width and height).
   - Calculate the maximum possible distance from the center to a corner 

6. **Aplly distance-based coloring using RGB**
   - **For** each pixel (x, y) in the canvas
      - Calculate the distance from the pixel to the center
      - Normalize this distance to a value between 0 and 1 (0 = center, 1 = corner)

   - **If** the normalized distance is between 0 and 0.5
      - blend the color from red to green 

   - **Else** (distance between 0.5 and 1)
      - blend the color from green to blue

7. **Create a distance gradient combined with a random noise pattern**
    - **Set values**
        - Set distance_weight = 0.6
        - Set noise_weight = 0.4
        - Set mid_point = 0.5
    - Create a coordinate grid with the size of the canvas
    - Calculate the distance from each pixel to the center
    - Normalize the distance to a value between 0 (center) and 1 (corner)
    - Generate a 2D random noise array with values between 0 and 1
    - Combine distance and noise:
         - combined = normalized_distance * (distance_weight + noise_weight * noise)
    - Split the combined array into two masks:
        - mask1: pixels <= mid_point (inner gradient)
        - mask2: pixels > mid_point  (outer gradient)

    - **Assign RGB colors based on masks**
        - mask1: blend red → green
        - mask2: blend green → blue

7. **Display the final gradient pattern**
   - Use Matplotlib to display the image
   - add a title to the canvas
   - turn off the axis 



8. **Save the images to a folder**
   - Save the image to the `images/` folder.

---

## Technical Explanation

In this assignment, i started by creating a blank (black) RGB canvas, i choose to keep the canvas in RGB from the begining because i knew i had to use the RGB color channel later on in the assignment. i created the blank canvas using `np.zeros()`. 

to create a striped pattern on the canvas i used slicing to define the stripes: `canvas[i:i+15, :]= 255`and after this creating a `for`loop to repet the pattern

Next, I introduced randomness by generating a black-and-white noise matrix using `np.random.choice`
because i wanted to keep working in RGB i had to convert the 2D array into an RGB canvas so i used the `np.stack`.

as the last part of the assignemnt i created a radial color gradient where i calculating the distance from each pixel to the center of the canvas. I normalized this distance to a [0, 1] to create a smooth transition between the colors, the RGB colors were definded based on the normalized distance so the pixels close to the center transitioned from red to green and the pixels farther from the center transitioned from green to blue.

as an addition, I combined a distance-based RGB gradient with random noise to create a more dynamic pattern.
The distance map controls the overall color structure from the center outward, while the noise introduces local variation.
Pixels are divided at a midpoint (0.5) so that the inner area transitions from red to green and the outer area from green to blue.
Using NumPy masks allows us to assign RGB values efficiently without looping over each pixel.

Finally, I used Matplotlib's `imshow()` to show the image and `savefig()` to save it in the correct file. 


---

## Results
The results from this assignment can be seen below with a short discribtion   



![Black empty canvas](images/black_empty_canvas.png)

*Figure 1: black empty canvas*



![Horizontal stripes](images/stripes_pattern.png)

*Figure 2: showing a black and white stiped horizontal pattern*



![Random noise pattern](images/noise_pattern.png)

*Figure 3: showing a random noise pattern*



![Distance-based RGB gradient](images/RGB_channel_pointinmid.png)

*Figure 4: showing a RGB gradient that is based on distance*



![Distance gradient combined with noise](images/distance_noise_combined.png)

*Figure 5: showing a combination of RGB gradient and noisepattern*  


---
## AI Acknowledgments
AI tools were used during this project, in particular Gemini (Google) and ChatGPT (OpenAI). These tools were primarily used to help understand code-related calculations, support the overall structure of the project, and assist with debugging when error messages occurred.

The following are examples of how AI was used during the development process:

*Describe in detail what happens in this calculation and explain it in a way that is understandable for a master’s student taking their first coding course*

*i get a error can you decribe what it means and how to fix it*

*image- why does my image look wong in the github browser, can you help me fix this*

---

## References

- NumPy Documentation: [Array Manipulation Routines](https://numpy.org/doc/stable/reference/routines.array-manipulation.html)
- Creating a loop: [python for loops](https://www.w3schools.com/python/python_for_loops.asp)
- creating array: [Numpy array slicing](https://www.w3schools.com/python/numpy/numpy_array_slicing.asp?utm_source=chatgpt.com)
- creating random pattern: [Numpy.random.choice] (https://numpy.org/doc/stable/reference/random/generated/numpy.random.choice.html)
- Theory on color gradient:(https://en.wikipedia.org/wiki/Color_gradient)
