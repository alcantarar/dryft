# detrend_force
This function was created in an effort to correct any drift in a force-measuring treadmill signal when someone is running on it. When running, a person has only 1 foot on the ground at a time, with an aerial phase inbetween. This function assumes that the force measured by the treadmill during any given aerial phase should be zero, and uses the aerial phases before and after a given step to tare the force signal. This will effectively correct for drift in the signal step-by-step.

## Python Version
This has been tested more than the matlab version. works with the .txt file and detrends an nx3 array of [horizontal, horizontal, vertical] forces. 

## Matlab Version
Still under development. Designed to read in raw voltages from a Treadmetrix treadmill.
