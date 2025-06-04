import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# st.set_option('server.runOnSave', True)

# Read the CSV data
data = pd.read_csv("../watchlist.csv")

# Create visualizations
st.title("Letterboxd Watchlist Analysis")

fig, ax = plt.subplots()
st.subheader("Distribution of Movie Duration")
plt.hist(data["duration"], bins=50, color="blue", edgecolor="black")
plt.xlabel("Duration (minutes)")
plt.ylabel("Frequency")
plt.title("Distribution of Duration")
st.pyplot(fig)

fig, ax = plt.subplots()
st.subheader("Distribution of Movie Ratings")
plt.hist(data["rating"], bins=50, color="gold", edgecolor="black")
plt.xlabel("Rating")
plt.ylabel("Frequency")
plt.title("Distribution of Ratings")
st.pyplot(fig)

short_movies = data[data["duration"] < 90]
st.subheader("Movie Links (Under 90 Minutes)")
st.write(("https://letterboxd.com" + short_movies["link"]).tolist())