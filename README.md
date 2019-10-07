# Dryft
#### Created by Ryan Alcantara 
##### ryan.alcantara@colorado.edu
This library was created in an effort to correct any drift in a force-measuring 
treadmill or force plate signal when someone is running on it. When running, a 
person has only 1 foot on the ground at a time, with an aerial phase inbetween each step. 
Here, I assume that the force measured by the treadmill during any given aerial phase should be zero, 
and use the aerial phases before and after a given step to tare the force signal. This will 
effectively correct for drift in the signal step-wise manner. 

The python library was developed first and has been tested . A MATLAB version was
created afterwards as it is a common language used in the field of biomechanics.

``