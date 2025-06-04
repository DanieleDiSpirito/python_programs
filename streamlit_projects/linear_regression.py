from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Title
st.title("Linear Regression")

# Input for number of random points in the sidebar
num_points = st.sidebar.slider("Enter the number of random points:", min_value=1, max_value=100, value=10)

# Generate random points
x = np.random.rand(num_points, 1) * 100
y = 3 * x + np.random.randn(num_points, 1) * 50

# Perform linear regression
reg = LinearRegression().fit(x, y)
a = reg.coef_[0][0]
b = reg.intercept_[0]

# Calculate statistics
cov_xy = np.cov(x.flatten(), y.flatten())[0, 1]
s_x2 = np.var(x, ddof=1)
s_y2 = np.var(y, ddof=1)
s_x = np.sqrt(s_x2)
s_y = np.sqrt(s_y2)
rho = np.corrcoef(x.flatten(), y.flatten())[0, 1]
R2 = reg.score(x, y)

# Display coefficients and statistics in the sidebar
st.sidebar.latex(f"y = {a:.2f}x + {b:.2f}" if b > 0 else f"y = {a:.2f}x - {-b:.2f}")
st.sidebar.latex(f"\\text{{Covariance}}: cov_{{x,y}} = {cov_xy:.2f}")
st.sidebar.latex(f"\\text{{Variance}}: s_x^2 = {s_x2:.2f}")
st.sidebar.latex(f"\\text{{Variance}}: s_y^2 = {s_y2:.2f}")
st.sidebar.latex(f"\\text{{Standard Deviation}}: s_x = {s_x:.2f}")
st.sidebar.latex(f"\\text{{Standard Deviation}}: s_y = {s_y:.2f}")
st.sidebar.latex(f"\\text{{Correlation Index}}: \\rho = {rho:.2f}")
st.sidebar.latex(f"\\text{{Determination Index}}: R^2 = {R2:.2f}")

# Plot points and regression line in the main area
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', label='Random Points')
plt.plot(x, reg.predict(x), color='red', label='Regression Line')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Random Points and Linear Regression')
plt.legend()
st.pyplot(plt)