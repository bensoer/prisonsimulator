# prisonsimulator

prisonsimulator is a simulator for solving the prisoner lightswitch problem, which is to find the fastest way
to determine if all prisoners have been inside the room.

# Prerequisites
The project is built using Python 3.6. There are no other dependencies on the project currently

# Setup
1. Clone the project
2. Execute `main.py` from terminal to execute the simulation

# Usage
You can alter the algorithm simply by adjusting the `handles_lightswitch` method within the `Prisoner` class.
This method is called everytime a prisoner enters the room, and thus has to make a specific action to the
lightswitch so as to inform or stay informed of the status of all the other prisoners.

Adjusting the `decideWhetherToAnnounce` method will change how the prisoner decides whether all other prisoners
have been in the room. This method is called everytime after `handles_lightswitch` on the same prisoner has
occurred

You can also adjust the number of prisoners by editing the `max_prisoners` variable listed in the `main.py`

# TODO
More features are coming with metrics as the simulation occurs. The intention to be able to output an
sqlite database of each days events from the simulation - which can then be graphed from for data
and debugging. Additionally features to allow others to clone the repo and easily add their own algorithms
is coming

NOTE THIS PROJECT IS IN BETA AND DOESN'T HAVE MUCH OF A SHELF LIFE.