import os
import sys
import streamlit as st
from SIR_model import main as run_sir_model
import matplotlib
matplotlib.use("agg")  # Use the non-interactive Agg backend

# Add Graphviz bin directory to PATH
graphviz_bin_dir = os.path.join(sys.prefix, "bin")
os.environ["PATH"] += os.pathsep + graphviz_bin_dir


# Streamlit app title
st.title('SIR Model Simulation')

# Introduction
st.write('This application simulates and visualizes the SIR model for infectious disease spread.')


# Buttons to control the simulation
# if st.button('Run SIR Model'):
#     # Call the modified run_sir_model function with "run" mode
#     figures = run_sir_model(mode="run")
#     for fig in figures:
#         st.pyplot(fig)
#     st.success('Model executed successfully.')

# if st.button('Generate Graph'):
#     # Call the modified run_sir_model function with "graph" mode
#     image_path=run_sir_model(mode="graph")
#     st.image(image_path,caption="SIR Model Graph")
#     st.success('Graph generated successfully.')

# Input fields for user input
susceptible_input = st.text_input('Initial Susceptible:', '1000')
infected_input = st.text_input('Initial Infected:', '1')
recovered_input = st.text_input('Initial Recovered:', '0')

# Slider for infection rate (beta)
beta_slider = st.slider('Infection Rate (beta):', 0, 1, 0.3)

# Slider for recovery rate (gamma)
gamma_slider = st.slider('Recovery Rate (gamma):', 0, 1, 0.1)

# Create the SIR model with user input and slider values
total_population = int(susceptible_input)
initial_infected = int(infected_input)
initial_recovered = int(recovered_input)
beta = beta_slider
gamma = gamma_slider

# Call the modified run_sir_model function with user input and slider values
figures = run_sir_model(total_population, initial_infected, initial_recovered, beta, gamma, mode="run")
for fig in figures:
    st.pyplot(fig)
st.success('Model executed successfully with user input and slider values.')

if st.button('Generate Graph'):
    # Call the modified run_sir_model function with "graph" mode
    image_path=run_sir_model(total_population, initial_infected, initial_recovered, beta, gamma, mode="graph")
    st.image(image_path,caption="SIR Model Graph")
    st.success('Graph generated successfully with user input and slider values.')
    
# Instructions or description can be added here
st.write('The SIR model divides the population into three categories: Susceptible (S), Infected (I), and Recovered (R). The model simulates how an infectious disease spreads and is managed within a population over time.')
