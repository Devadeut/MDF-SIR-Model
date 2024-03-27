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
figures = run_sir_model(total_population, initial_infected, initial_recovered, beta, gamma, mode="run")
for fig in figures:
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

dt = 1
duration = 100
t = 0
# Define the lists to store the population data over time
times = []  # List of time points
s = []  # List of susceptible population
i = []  # List of infected population
r = []  # List of recovered population

# Run the SIR model simulation and store the population data at each time step
while t <= duration:
    times.append(t)
    # Evaluate the model at each time step and store the population values
    s.append(eg.enodes["id"].evaluable_outputs["out_port1"].curr_value)
    i.append(eg.enodes["id"].evaluable_outputs["out_port2"].curr_value)
    r.append(eg.enodes["id"].evaluable_outputs["out_port3"].curr_value)
    t += dt
# Create an animated graph
fig = go.Figure(data=[
    go.Scatter(x=times, y=s, name='Susceptible', mode='lines'),
    go.Scatter(x=times, y=i, name='Infected', mode='lines'),
    go.Scatter(x=times, y=r, name='Recovered', mode='lines'),
])

# Update the graph title and layout
fig.update_layout(title='Population over time',
                  xaxis_title='Time',
                  yaxis_title='Population',
                  yaxis=dict(range=[0, 1000]))

# Display the animated graph
st.plotly_chart(fig)