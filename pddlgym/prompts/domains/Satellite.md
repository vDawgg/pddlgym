## Domain description

A robot is tasked with controlling a set of satellites to capture images. Each satellite can have different instruments with different capabilities on board.

The actions available to the robot are:
- turn_to
    - Points a satellite in a specific direction.
- switch_on
    - Turns on a specific instrument on the satellite. Once an instrument is switched on on a satellite, all power is consumed by this instrument and the power only becomes available again once the instrument is turned off.
- switch_off
    - Turns off a specific instrument on the satellite.
- calibrate
    - Calibrates an instrument for a specific target direction.
- take_image
    - Takes an image in a specific mode of the current direction of the satellite using one a calibrated instrument.
