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

# Get user inputs for model parameters
total_population = st.number_input("Total Population", min_value=1, value=1000, step=1)
initial_infected = st.number_input("Initial Infected Population", min_value=0, max_value=total_population, value=1)
initial_recovered = st.number_input("Initial Recovered Population", min_value=0, max_value=total_population - initial_infected, value=0)
beta = st.slider("Infection Rate (β)", min_value=0.0, max_value=1.0, value=0.3, step=0.01)
gamma = st.slider("Recovery Rate (γ)", min_value=0.0, max_value=1.0, value=0.1, step=0.01)


# Call the modified run_sir_model function with user input and slider values
# figures = run_sir_model(total_population, initial_infected, initial_recovered, beta, gamma, mode="run")
# for fig in figures:
#     st.pyplot(fig)
# st.success('Model executed successfully with user input and slider values.')

# Call the modified run_sir_model function with user input and slider values
figures = run_sir_model(total_population, initial_infected, initial_recovered, beta, gamma, mode="run")
for fig in figures:
    if isinstance(fig, matplotlib.animation.FuncAnimation):
        st.write("Animated Plot:")
        st.pyplot(fig)
    else:
        st.pyplot(fig)

st.success('Model executed successfully with user input and slider values.')

# Buttons to control the simulation
if st.button('Generate Graph'):
    # Call the modified run_sir_model function with "graph" mode
    image_path=run_sir_model(total_population, initial_infected, initial_recovered, beta, gamma, mode="graph")
    st.image(image_path,caption="SIR Model Graph")
    st.success('Graph generated successfully with user input and slider values.')
    
# Instructions or description can be added here
st.write('The SIR model divides the population into three categories: Susceptible (S), Infected (I), and Recovered (R). The model simulates how an infectious disease spreads and is managed within a population over time.')
