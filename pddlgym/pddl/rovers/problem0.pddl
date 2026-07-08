; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem roverprob1234) (:domain Rover)
(:objects
	general - Lander
	colour high_res low_res - Mode
	rover0 - Rover
	rover0store - Store
	waypoint0 waypoint1 waypoint2 waypoint3 - Waypoint
	camera0 - Camera
	objective0 objective1 - Objective
	)
(:init
	(at_soil_sample waypoint0)
	(at_rock_sample waypoint1)
	(at_soil_sample waypoint2)
	(at_rock_sample waypoint2)
	(at_soil_sample waypoint3)
	(at_rock_sample waypoint3)
	(at_lander general waypoint0)
	(channel_free general)
	(at rover0 waypoint3)
	(store_of rover0store rover0)
	(empty rover0store)
	(equipped_for_soil_analysis rover0)
	(equipped_for_rock_analysis rover0)
	(equipped_for_imaging rover0)
	(on_board camera0 rover0)
	(calibration_target camera0 objective1)
	(supports camera0 colour)
	(supports camera0 high_res)

    ; action literals
    (navigate rover0 waypoint0)
    (navigate rover0 waypoint1)
    (navigate rover0 waypoint2)
    (navigate rover0 waypoint3)
    (sample_soil rover0)
    (sample_rock rover0)
    (drop rover0)
    (calibrate camera0 objective0)
    (calibrate camera0 objective1)
    (take_image objective0 camera0 colour)
    (take_image objective0 camera0 high_res)
    (take_image objective0 camera0 low_res)
    (take_image objective1 camera0 colour)
    (take_image objective1 camera0 high_res)
    (take_image objective1 camera0 low_res)
    (communicate_soil_data rover0 waypoint0)
    (communicate_rock_data rover0 waypoint0)
    (communicate_soil_data rover0 waypoint1)
    (communicate_rock_data rover0 waypoint1)
    (communicate_soil_data rover0 waypoint2)
    (communicate_rock_data rover0 waypoint2)
    (communicate_soil_data rover0 waypoint3)
    (communicate_rock_data rover0 waypoint3)
    (communicate_image_data rover0 objective0 colour)
    (communicate_image_data rover0 objective0 high_res)
    (communicate_image_data rover0 objective0 low_res)
    (communicate_image_data rover0 objective1 colour)
    (communicate_image_data rover0 objective1 high_res)
    (communicate_image_data rover0 objective1 low_res)
    )

(:goal (and
(communicated_soil_data waypoint2)
(communicated_rock_data waypoint3)
(communicated_image_data objective1 high_res)
	)
)
)
