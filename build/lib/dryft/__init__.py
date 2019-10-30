"""

Removes linear or non-linear ground reaction force signal drift in a stepwise manner. It is intended
for running ground reaction force data commonly analyzed in the field of Biomechanics. The aerial phase before and after
a given stance phase are used to tare the signal instead of assuming an overall linear trend or signal offset.

Licensed under an MIT License (c) Ryan Alcantara 2019

https://alcantarar.github.io

Distributed here: https://github.com/alcantarar/dryft

"""