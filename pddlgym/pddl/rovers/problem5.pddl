; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem roverprob2312) (:domain Rover)
(:objects
	general - Lander
	colour high_res low_res - Mode
	rover0 rover1 - Rover
	rover0store rover1store - Store
	waypoint0 waypoint1 waypoint2 waypoint3 waypoint4 waypoint5 - Waypoint
	camera0 camera1 camera2 - Camera
	objective0 objective1 - Objective
	)
(:init
	(at_rock_sample waypoint0)
	(at_soil_sample waypoint1)
	(at_soil_sample waypoint2)
	(at_rock_sample waypoint2)
	(at_soil_sample waypoint3)
	(at_rock_sample waypoint3)
	(at_soil_sample waypoint4)
	(at_soil_sample waypoint5)
	(at_rock_sample waypoint5)
	(at_lander general waypoint3)
	(channel_free general)
	(at rover0 waypoint1)
	(store_of rover0store rover0)
	(empty rover0store)
	(equipped_for_rock_analysis rover0)
	(equipped_for_imaging rover0)
	(at rover1 waypoint4)
	(store_of rover1store rover1)
	(empty rover1store)
	(equipped_for_soil_analysis rover1)
	(equipped_for_imaging rover1)
	(on_board camera0 rover0)
	(calibration_target camera0 objective0)
	(supports camera0 colour)
	(supports camera0 low_res)
	(on_board camera1 rover0)
	(calibration_target camera1 objective1)
	(supports camera1 colour)
	(supports camera1 low_res)
	(on_board camera2 rover1)
	(calibration_target camera2 objective0)
	(supports camera2 colour)
	(supports camera2 high_res)
)

(:goal (and
(communicated_soil_data waypoint5)
(communicated_soil_data waypoint1)
(communicated_soil_data waypoint4)
(communicated_soil_data waypoint2)
(communicated_rock_data waypoint0)
(communicated_rock_data waypoint2)
(communicated_rock_data waypoint3)
(communicated_image_data objective0 colour)
(communicated_image_data objective1 low_res)
(communicated_image_data objective0 low_res)
	)
)
)
