import os
import sys
import streamlit as st
from SIR_model import main as run_sir_model

# Add Graphviz bin directory to PATH
graphviz_bin_dir = os.path.join(sys.prefix, "bin")
os.environ["PATH"] += os.pathsep + graphviz_bin_dir


# Streamlit app title
st.title('SIR Model Simulation')

# Introduction
st.write('This application simulates and visualizes the SIR model for infectious disease spread.')

# Buttons to control the simulation
if st.button('Run SIR Model'):
    # Call the modified run_sir_model function with "run" mode
    figures = run_sir_model(mode="run")
    for fig in figures:
        st.pyplot(fig)
    st.success('Model executed successfully.')

if st.button('Generate Graph'):
    # Call the modified run_sir_model function with "graph" mode
    image_path=run_sir_model(mode="graph")
    st.image(image_path,caption="SIR Model Graph")
    st.success('Graph generated successfully.')

# Instructions or description can be added here
st.write('The SIR model divides the population into three categories: Susceptible (S), Infected (I), and Recovered (R). The model simulates how an infectious disease spreads and is managed within a population over time.')
