import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import time


def random_stock_trend(starting_point, loops, max_variance):
    values = [0 for _ in range(loops)]
    values[0] = starting_point
    for idx in range(1, loops):
        new_value = (1 + (random.random() - 0.5) * max_variance * 2) * values[idx-1]
        values[idx] = new_value
    return values

def main():
    st.title("Random Stock Trend Simulation")
    starting_point = st.number_input("Starting Point", value=100, min_value=0)
    loops = st.number_input("Number of Loops", value=1000, min_value=1)
    max_variance = st.number_input("Max Variance", value=0.05, min_value=0.01, max_value=1.0, step=0.01)

    if st.button("Generate Trend"):
        with st.spinner("Generating trend..."):
            time.sleep(2)  # Simulate a long computation
            values = random_stock_trend(starting_point, loops, max_variance)
            st.success("Trend generated!")

        # put this in lateral column
        st.sidebar.header("Trend Statistics")
        st.sidebar.write(f"Starting point: {starting_point}")
        st.sidebar.write(f"Final value: {values[-1]}")
        st.sidebar.write(f"Trend: {100 * (values[-1] - starting_point) / starting_point:.2f}%")
        st.sidebar.write(f"Average value: {sum(values) / len(values):.2f}")
        st.sidebar.write(f"Max value: {max(values):.2f}")
        st.sidebar.write(f"Min value: {min(values):.2f}")
        st.sidebar.write(f"Range: {max(values) - min(values):.2f}")

        plt.plot(values)
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title('Random Stock Trend')
        st.pyplot(plt)
        plt.clf()

if __name__ == "__main__":
    main()