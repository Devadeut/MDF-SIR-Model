import os
import sys
import streamlit as st
from SIR_model import main as run_sir_model
import matplotlib
import plotly.graph_objs as go
import plotly.express as px
matplotlib.use("agg")  # Use the non-interactive Agg backend

# Add Graphviz bin directory to PATH
graphviz_bin_dir = os.path.join(sys.prefix, "bin")
os.environ["PATH"] += os.pathsep + graphviz_bin_dir


# Streamlit app title
st.title('SIR Model Simulation')

# Introduction
st.write('This application simulates and visualizes the SIR model for infectious disease spread.')


# Create a 2-column layout
col1, col2 = st.columns(2)
# Place number input and sliders in the first column
with col1:
    total_population = st.number_input("Total Population", value=1000, min_value=1)
    initial_infected = st.number_input("Initial Infected Population", value=1, min_value=0)
    initial_recovered = st.number_input("Initial Recovered Population", value=0, min_value=0)
# Place the other sliders in the second column
with col2:
    beta = st.slider("Infection Rate (β)", min_value=0.0, max_value=1.0, value=0.3)
    gamma = st.slider("Recovery Rate (γ)", min_value=0.0, max_value=1.0, value=0.1)



# Call the modified run_sir_model function with user input and slider values
# figures = run_sir_model(total_population, initial_infected, initial_recovered, beta, gamma, mode="run")
# for fig in figures:
#     st.pyplot(fig)
# st.success('Model executed successfully with user input and slider values.')

# Call the modified run_sir_model function with user input and slider values
fig,gif_path = run_sir_model(total_population, initial_infected, initial_recovered, beta, gamma, mode="run")
st.write("Static Population Model Output:")
st.pyplot(fig)
st.write("Animated Population Model Output:") # Display the GIF
st.image(gif_path, caption='SIR Model Animation')
st.success('Model executed successfully with user input and slider values.')


# Buttons to control the simulation
if st.button('Generate Graph'):
    # Call the modified run_sir_model function with "graph" mode
    image_path=run_sir_model(total_population, initial_infected, initial_recovered, beta, gamma, mode="graph")
    st.image(image_path,caption="SIR Model Graph")
    st.success('Graph generated successfully with user input and slider values.')
    
# Instructions or description can be added here
st.write('The SIR model divides the population into three categories: Susceptible (S), Infected (I), and Recovered (R). The model simulates how an infectious disease spreads and is managed within a population over time.')
