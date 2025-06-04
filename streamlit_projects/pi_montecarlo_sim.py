import streamlit as st
import random
from random import gauss
import matplotlib.pyplot as plt
from math import pi as PI, e as E
import numpy as np  # For Gaussian distribution

def distance(P, Q):
    return ((P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2) ** 0.5

def estimate_pi(points, is_gauss = False):
    in_circle = 0
    in_square = 0
    for P in points:
        if distance(P, (0, 0)) < 1:
            in_circle += 1
        in_square += 1
    if is_gauss:
        total_points = len(points)
        return 8 * in_circle / total_points
    return 4 * in_circle / in_square

def estimate_e(estimated_pi):
    p = estimated_pi / 8
    e = (1 - p)**(-2)
    return e

def plot_results(points, estimated_pi, title="Monte Carlo Simulation for Pi Estimation"):
    plt.figure(figsize=(8, 8))
    plt.scatter([point[0] for point in points], [point[1] for point in points], s=0.5, color='blue')

    circle = plt.Circle((0, 0), 1, fill=False, color='red')
    plt.gca().add_patch(circle)
    plt.axis('equal')
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")

    # Display estimated pi and absolute error
    error = 100 * abs(estimated_pi - PI) / PI
    st.write(f"Estimated $\pi$: ${estimated_pi:.4f}$ ($\epsilon$ = ${error:.4f}\%$)")
    st.write(f"True value of $\pi$: ${PI:.8f}$")
    if use_gaussian:
        error_e = 100 * abs(estimated_e - E) / E
        st.write(f"Estimated $e$: ${estimated_e:.4f}$ ($\epsilon$ = ${error_e:.4f}\%$)")
        st.write(f"True value of $e$: ${E:.8f}$")
    st.pyplot(plt)

st.title("Monte Carlo Simulation for Pi Estimation")

# User input for number of points
num_points = st.sidebar.number_input("Number of Points", min_value=100, max_value=100000, value=10000)

# Option for Gaussian distribution
use_gaussian = st.checkbox("Use Gaussian Distribution")

# Perform simulation and plot results
if st.button("Run Simulation"):
    if use_gaussian:
        points = [(gauss(0, 1), gauss(0, 1)) for _ in range(num_points)]
    else:
        points = [(2*random.random() - 1, 2*random.random() - 1) for _ in range(num_points)]

    estimated_pi = estimate_pi(points,  use_gaussian)
    if use_gaussian:
        estimated_e = estimate_e(estimated_pi)

    if use_gaussian:
        plot_results(points, estimated_pi, title="Gaussian Distribution")
    else:
        plot_results(points, estimated_pi)
