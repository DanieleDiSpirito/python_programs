import streamlit as st
import matplotlib.pyplot as plt
from random import random
from math import log2, ceil

# Constants
LIMIT = 1e-3

# Generate random sequence #1
sequence_1 = []
last_value = 1
remainder = 1

while remainder > LIMIT:
    last_value = random() * remainder
    remainder -= last_value
    sequence_1.append(last_value)

# Streamlit app
st.title("Random Sequence Visualization")

# Display real and expected lengths
real_length = len(sequence_1)
expected_length = ceil(-log2(LIMIT))
st.write(f"Real length: {real_length}")
st.write(f"Expected length: {expected_length}")

sequence_2 = sequence_1.copy()
# shuffle the second sequence
for i in range(len(sequence_2) - 1, 0, -1):
    j = int(random() * (i + 1))
    sequence_2[i], sequence_2[j] = sequence_2[j], sequence_2[i]

# Plot the random sequence #1 and #2 separately but on the same graph
st.subheader("Random Sequence #1 and #2")
fig, ax = plt.subplots()
ax.plot(sequence_1, label="Random Sequence #1")
ax.plot(sequence_2, label="Random Sequence #2")
ax.set_xlabel("Index")
ax.set_ylabel("Value")
ax.set_title("Random Sequence #1 and #2")
ax.legend()
st.pyplot(fig)