## Domain description

A robot is tasked with manufacturing a set of parts according to requirements for their shape, colour and surface condition. Once a machine is used to work on a part, the machine is occupied and can only be used again when 'do-time-step' is called at which points all busy machines complete their work and can be used again.

The actions available to the robot are:
- do-polish
    - Polishes a part. Part must be cold to allow for polishing.
- do-roll
    - Rolls a part into a cylindrical shape. This action raises the temperature of the part to 'hot' and removes all paint and surfaces conditions and additionally rolls out any holes that might have been previously drilled on the part.
- do-lathe
    - Turns a part into a cylindrical shape. Results in a rough surface condition and removes all paint.
- do-grind
    - Grinds a part to a smooth surface. Additionally removes all paint.
- do-punch
    - Punches out a hole from a part. Requires the machine to support the desired bit-width and orientation for the hole and for the part to be cold. Additionally results in a rough surface condition.
- do-drill-press
    - Drills out a hole from a part. Requires the machine to support the desired bit-width and orientation for the hole and for the part to be cold.
- do-spray-paint
    - Paints the part in a specifc color. Requires the part to be cold and removes all other surface conditions.
- do-immersion-paint
    - Paints the part in a specific color. Preserves preexisting surface conditions of the part.
- do-time-step
    - Advances the schedule, freeing machines that were previously busy and completing the current work step for a part.
