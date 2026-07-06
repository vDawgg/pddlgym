## Domain description

A robot is tasked with driving a set of goods from markets to depots. Each of the available trucks is constrained in its maximum carrying capacity, meaning multiple trucks may need to be used to best deliver all desired goods to the depots.

The actions available to the robot are:
- drive
    - Drives a truck to a specific position.
- load
    - Loads goods from a market into a truck. Reuquires the definition of the levels (i.e. amount of goods) in the market and truck before and after loading.
- unload
    - Unloads goods from a truck into a depot. Requires the definition of the levels in the truck and depot before and after unloading.
- buy
    - Buys a specific amount of goods from a market given a truck is present at the market. Requires teh definition of the levels to be loaded at the market and the levels of goods for sale available at the market before and after buying.
