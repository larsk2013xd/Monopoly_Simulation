# Monopoly Simulation
This repo contains a project that simulates games of Monopoly and can be used to investigate game tactics and overall probabilities.

# About the simulations

The simulation is at this moment a simplified version of the original game. It works on the general idea that one player moves across the board without any opponents.
The program keeps track of ending positions of a turn. To give an example consider the following scenario:

You are now at 'Free Parking' and you throw a 10. This moves the player to the 'Go To Jail' spot. The player then gets moved to jail and his turn ends. 

In this case the 'In Jail' spot will be counted. So not the 'Go To Jail' spot. In fact, no turn ends on the 'Go To Jail' spot. Hence all simulations will return a 0 density at that spot.

For the user that is just interested in the (visual) statistics the following methods can be used.

`densityPlot(density, sname, printPilon = False, pilonSquare = 0, makeDensity = True, animate = False)`:
This function generates the density image and it takes in a few arguments.

`density`: An `np.array` of size `41` containing the frequencies of ending your turn on each square. Where index `0` corresponds to "Go". Index `39` corresponds to "Mayfair", and index `40` corresponds to "In Jail". To obtain this density please check the next section.

`sname`: Name of the file to write the infographic to. No need to put in an extension (PNG is used)

`printPilon (default: False)`: Will show a red circle on a specific square given by the `pilonSquare` argument. Can be used to show initial positions of a player.

`pilonSquare (default: 0)`: If `printPilon = True` this will be the index of the to be shown Pilon.

`makeDensity (default: True)`: If needed this will convert the given frequency array into a density (summing up to 1). All built-in functions show the pure frequencies. However if needed and custom data is used already in density format this can be set to `False`.

`animate (default: False)`: Not working at this moment.

# Obtaining densities

The user can use two functions to obtain densities:

`simulateThrowOnPos(position, nSims)` This will return a density of ending spots after a throw from a specific `position`. `nSims` can be used to increase/decrease estimation accuracy

`simulateGames(nSims, nTurns)` This will let a player move around the board for a total of `nTurns`. This will be simulated `nSims` times.

# To be added

The graphics will be completely redone and multiple seperate graphics will be available. For now the `densityPlot` is the only possible function for the graphical interpretation
