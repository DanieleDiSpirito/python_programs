import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Title
st.title("Coin Flip")

# Input for number of coin flip
num_flip = st.sidebar.slider("Enter the number of coin flip:", min_value=1, max_value=10, value=5)

# Choose between "At least", "Precisely", "Less than"
flip_type = st.sidebar.selectbox("Choose:", ["At least", "Precisely", "Less than"])
symbol = {"At least": r"\geq", "Precisely": "=", "Less than": "<"}

# Choose the number of heads
num_heads = st.sidebar.slider("Enter the number of heads:", min_value=0, max_value=num_flip, value=5)

# Calculate statistics
prob = np.array([0.0] * (num_flip+1))
for i in range(num_flip+1):
    prob[i] = np.math.comb(num_flip, i) * 0.5**num_flip

# Calculate the probability
if flip_type == "At least":
    result = sum(prob[num_heads:])
elif flip_type == "Precisely":
    result = prob[num_heads]
else:
    result = sum(prob[:num_heads])

# Display the probability in the sidebar
st.sidebar.latex(f"P(X {symbol[flip_type]} {num_heads}) = {result:.5f}%")

for i in range(num_flip+1):
    st.sidebar.latex(f"P(X = {i}) = {prob[i]:.5f}")

# Show histogram in the main area
plt.figure(figsize=(10, 6))
plt.bar(range(num_flip+1), prob, color='blue', label='Probabilities')
# color red bar for the selected number of heads
if flip_type == "At least": # color red bar for the selected number of heads and the next
    plt.bar(range(num_heads, num_flip+1), prob[num_heads:], color='red', label='Selected Probability')
elif flip_type == "Precisely":
    plt.bar(num_heads, prob[num_heads], color='red', label='Selected Probability')
else: # color red bar for the selected number of heads (not included) and the previous
    plt.bar(range(num_heads), prob[:num_heads], color='red', label='Selected Probability')
plt.xlabel('Number of Heads')
plt.ylabel('Probability')
plt.title('Coin Flip Probability')
plt.legend()
st.pyplot(plt)