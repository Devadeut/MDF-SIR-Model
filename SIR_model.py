"""
    Example of ModECI MDF - SIR model
    
    An SIR model is an epidemiological model that computes the theoretical number of people infected with a contagious illness in a closed population     over time. The name of this class of models derives from the fact that they involve coupled equations relating the number of susceptible people       S(t), number of people infected I(t), and number of people who have recovered R(t).
"""


from modeci_mdf.mdf import*
import matplotlib.pyplot as plt
import os
import sys
from matplotlib.animation import FuncAnimation  
import imageio
import numpy as np

# Rest of the code remains the same

def main(total_population=1000, initial_infected=1, initial_recovered=0, beta=0.3, gamma=0.1, mode=None):
    # Initialize the Model
    sir_model = Model(id="SIR_Model")

    # Create a Graph within the Model
    sir_graph = Graph(id="SIR_Graph")
    sir_model.graphs.append(sir_graph)



    # # Parameters for the model
    # total_population = 1000
    # initial_infected = 1
    # initial_recovered = 0
    # beta = 0.3  # Infection rate
    # gamma = 0.1  # Recovery rate
    initial_susceptible = total_population - initial_infected - initial_recovered


    # SIR equation Node
    sir_node = Node(id="id")


    total_population = Parameter(id="total_population", value=total_population)
    gamma = Parameter(id="gamma", value=gamma)
    beta = Parameter(id="beta", value=beta)

    susceptible_population = Parameter(id="susceptible_population",
                                        default_initial_value=initial_susceptible,
                                        time_derivative="-beta*susceptible_population*infected_population/total_population"
                                       )
    infected_population = Parameter(id="infected_population",
                                        default_initial_value=initial_infected,
                                        time_derivative="beta*susceptible_population*infected_population/total_population - gamma*infected_population"
                                       )
    recovered_population = Parameter(id="recovered_population",
                                      default_initial_value=initial_recovered,
                                      time_derivative="gamma*infected_population"
                                     )
    infected_output1 = OutputPort(id="out_port1",value=susceptible_population.id)
    infected_output2 = OutputPort(id="out_port2",value=infected_population.id)
    infected_output3 = OutputPort(id="out_port3",value=recovered_population.id)


    sir_node.parameters.append(gamma)
    sir_node.parameters.append(beta)
    sir_node.parameters.append(total_population)
    sir_node.parameters.append(susceptible_population)
    sir_node.parameters.append(infected_population)
    sir_node.parameters.append(recovered_population)
    sir_node.output_ports.append(infected_output1)
    sir_node.output_ports.append(infected_output2)
    sir_node.output_ports.append(infected_output3)


    # Recovered Node
    recovered_node = Node(id="Recovered")
    recovered_input = InputPort(id="input_port")
    recovered_output = OutputPort(id="out_port",value=recovered_input.id)
    recovered_node.input_ports.append(recovered_input)
    recovered_node.output_ports.append(recovered_output)

    #Infected Node
    infected_node = Node(id="Infected")
    infected_input = InputPort(id="input_port")
    infected_output = OutputPort(id="out_port",value=infected_input.id)
    infected_node.input_ports.append(infected_input)
    infected_node.output_ports.append(infected_output)


    #Infected Node
    susceptible_node = Node(id="Susceptible")
    susceptible_input = InputPort(id="input_port")
    susceptible_output = OutputPort(id="out_port",value=susceptible_input.id)
    susceptible_node.input_ports.append(susceptible_input)
    susceptible_node.output_ports.append(susceptible_output)

    # Add nodes to the graph
    sir_graph.nodes.append(sir_node)
    sir_graph.nodes.append(recovered_node)
    sir_graph.nodes.append(infected_node)
    sir_graph.nodes.append(susceptible_node)


    # Infected to Recovered transition
    sir_to_rec_edge = Edge(
        id="sir_to_rec",
        sender=sir_node.id,
        sender_port="out_port3",
        receiver=recovered_node.id,
        receiver_port="input_port",
    
    )

    sir_to_inf_edge = Edge(
        id="sir_to_inf",
        sender=sir_node.id,
        sender_port="out_port2",
        receiver=infected_node.id,
        receiver_port="input_port",
    )

    sir_to_sus_edge = Edge(
        id="sir_to_sus",
        sender=sir_node.id,
        sender_port="out_port1",
        receiver=susceptible_node.id,
        receiver_port="input_port",
    )


    # Add edges to the graph
    sir_graph.edges.append(sir_to_rec_edge)
    sir_graph.edges.append(sir_to_inf_edge)
    sir_graph.edges.append(sir_to_sus_edge)

    if mode=="run":

        from modeci_mdf.execution_engine import EvaluableGraph
        eg = EvaluableGraph(sir_graph, verbose=False)
        eg.evaluate()

        dt = 1

        duration = 100
        t = 0
        times = []
        s = []
        i = []
        r = []
        while t <= duration:
            times.append(t)
            print("======   Evaluating at t = %s  ======" % (t))
            if t == 0:
                eg.evaluate()  
            else:
                eg.evaluate(time_increment=dt)

            s.append(eg.enodes["id"].evaluable_outputs["out_port1"].curr_value)
            i.append(eg.enodes["id"].evaluable_outputs["out_port2"].curr_value)
            r.append(eg.enodes["id"].evaluable_outputs["out_port3"].curr_value)

            t += dt
            print('Susceptible polution: %s'%eg.enodes["id"].evaluable_outputs["out_port1"].curr_value)
            print('Infected polution: %s'%eg.enodes["id"].evaluable_outputs["out_port2"].curr_value)
            print('Recovered polution: %s'%eg.enodes["id"].evaluable_outputs["out_port3"].curr_value)
    
        # Create subplots
        fig1, axs = plt.subplots(1, 3, figsize=(15, 5),sharey=True)
    
        # Plotting Susceptible population
        axs[0].plot(times, s, label='Susceptible', color='blue')
        axs[0].set_xlabel('Time')
        axs[0].set_ylabel('Susceptible Population')
        axs[0].set_title('Susceptible Population over Time')
        axs[0].legend()
        axs[0].grid(True)
    
        # Plotting Infected population
        axs[1].plot(times, i, label='Infected', color='orange')
        axs[1].set_xlabel('Time')
        axs[1].set_ylabel('Infected Population')
        axs[1].set_title('Infected Population over Time')
        axs[1].legend()
        axs[1].grid(True)
    
        # Plotting Recovered population
        axs[2].plot(times, r, label='Recovered', color='green')
        axs[2].set_xlabel('Time')
        axs[2].set_ylabel('Recovered Population')
        axs[2].set_title('Recovered Population over Time')
        axs[2].legend()
        axs[2].grid(True)
    
        plt.tight_layout()  # Adjust layout to prevent overlap
        plt.show()
    
        # Prepare an array to hold the rendered frames
        frames = []

        # Generate frames
        for frame in range(len(times)):
            fig, ax = plt.subplots()
            ax.plot(times[:frame+1], s[:frame+1], label='Susceptible', color='blue')
            ax.plot(times[:frame+1], i[:frame+1], label='Infected', color='orange')
            ax.plot(times[:frame+1], r[:frame+1], label='Recovered', color='green')
            ax.xaxis.set_major_locator(plt.MaxNLocator(6))
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.1f}'.format(x)))
            ax.set_xlabel('Time')
            ax.set_ylabel('Population')
            ax.set_title('Population over time')
            ax.legend()
            ax.grid(True)
    
            # Convert the Matplotlib figure to a RGB array and close the figure to free memory
            fig.canvas.draw()
            image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            frames.append(image)
            plt.close(fig)

        # Save the frames as a GIF
        imageio.mimsave('animated_plot.gif', frames, fps=20) 
        # # Create an animated line graph
        # fig2, ax = plt.subplots()
        # ax.plot(times, s, label='Susceptible', color='blue')
        # ax.plot(times, i, label='Infected', color='orange')
        # ax.plot(times, r, label='Recovered', color='green')
        # ax.xaxis.set_major_locator(plt.MaxNLocator(6))
        # ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: '{:.1f}'.format(x)))
        # ax.set_xlabel('Time')
        # ax.set_ylabel('Population')
        # ax.set_title('Population over time')
        # ax.legend()
        # ax.grid(True)
       
    
        # def animate(frame):
        #     ax.clear()
        #     ax.plot(times[:frame+1], s[:frame+1], label='Susceptible', color='blue')
        #     ax.plot(times[:frame+1], i[:frame+1], label='Infected', color='orange')  
        #     ax.plot(times[:frame+1], r[:frame+1], label='Recovered', color='green')
        #     ax.xaxis.set_major_locator(plt.MaxNLocator(6))
        #     ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: '{:.1f}'.format(x)))
        #     ax.set_xlabel('Time')
        #     ax.set_ylabel('Population')
        #     ax.set_title('Population over time')
        #     ax.legend()
        #     ax.grid(True)
        #     return[ax]
    
        # anim = FuncAnimation(fig2, animate, frames=times, interval=50, blit=True)
        # # Save the animated plot
        # anim.save('animated_plot.gif', writer='imagemagick')
        # plt.show()

        # return [fig1, anim]
        return [fig1]

    elif mode=="graph":

        sir_model.to_graph_image(
                engine="dot",
                output_format="png",
                view_on_render=False,
                level=3,
                filename_root="sir_model",
                is_horizontal=True
            )

        from IPython.display import Image
        Image(filename="sir_model.png")
        image_path = "sir_model.png"
        return image_path



    return sir_graph

if __name__ == "__main__":
    # Check if there are any command line arguments
    if len(sys.argv) > 1:
        # Assuming the second argument is the mode (e.g., '-run' or '-graph')
        mode_arg = sys.argv[1]
        if mode_arg == "-run":
            main(mode="run")
        elif mode_arg == "-graph":
            main(mode="graph")
        else:
            print("Invalid argument. Please use '-run' or '-graph'.")
    else:
        print("No arguments provided. Please specify '-run' or '-graph'.")   
    