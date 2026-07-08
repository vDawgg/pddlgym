## Domain description

A robot is tasked with controlling a set of moon rovers and gathering soil and rock data together with images that are sent back to the moon-lander.

The actions available to the robot are:
- navigate
    - Navigates a rover from one point to another.
- sample_soil
    - Samples the soil at the current position. The sampled soil occupies the available storage. Sampling soil is only possible if the specific rover is equipped for this operation.
- sample_rock
    - Samples the rock at the current position. The samples rock occupies the available storage. Sampling rock is only possible if the specific rover is equipped for this operation.
- drop
    - Frees up occupied storage.
- calibrate
    - Calibrates the camera for a desired objective at the current position. Each camera can only have one calibration target which is assigned from the start.
- take_image
    - Takes an image in a specific mode of a desired objective at the current position. Taking an image in a certain mode is only possible if this mode is available on the specific rover.
- communicate_soil_data
    - Sends soil data, including the location the soil was gathered from, back to the moon-lander.
- communicate_rock_data
    - Sends rock data, including the location the rock was gathered from, back to the moon-lander.
- communicate_image_data
    - Sends image data, inclduing the captured objective and image mode, back to the moon-lander.
