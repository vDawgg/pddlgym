; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem roverprob4123) (:domain Rover)
(:objects
	general - Lander
	colour high_res low_res - Mode
	rover0 rover1 rover2 - Rover
	rover0store rover1store rover2store - Store
	waypoint0 waypoint1 waypoint2 waypoint3 waypoint4 waypoint5 - Waypoint
	camera0 camera1 - Camera
	objective0 objective1 - Objective
	)
(:init
	(at_soil_sample waypoint1)
	(at_rock_sample waypoint2)
	(at_rock_sample waypoint3)
	(at_soil_sample waypoint4)
	(at_rock_sample waypoint4)
	(at_rock_sample waypoint5)
	(at_lander general waypoint3)
	(channel_free general)
	(at rover0 waypoint2)
	(store_of rover0store rover0)
	(empty rover0store)
	(equipped_for_soil_analysis rover0)
	(equipped_for_rock_analysis rover0)
	(equipped_for_imaging rover0)
	(at rover1 waypoint3)
	(store_of rover1store rover1)
	(empty rover1store)
	(equipped_for_rock_analysis rover1)
	(at rover2 waypoint4)
	(store_of rover2store rover2)
	(empty rover2store)
	(equipped_for_soil_analysis rover2)
	(equipped_for_rock_analysis rover2)
	(equipped_for_imaging rover2)
	(on_board camera0 rover0)
	(calibration_target camera0 objective0)
	(supports camera0 colour)
	(supports camera0 high_res)
	(on_board camera1 rover2)
	(calibration_target camera1 objective1)
	(supports camera1 high_res)
)

(:goal (and
(communicated_soil_data waypoint4)
(communicated_soil_data waypoint1)
(communicated_rock_data waypoint3)
(communicated_rock_data waypoint2)
(communicated_rock_data waypoint4)
(communicated_image_data objective0 high_res)
	)
)
)
