; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem roverprob5146) (:domain Rover)
(:objects
	general - Lander
	colour high_res low_res - Mode
	rover0 rover1 rover2 rover3 - Rover
	rover0store rover1store rover2store rover3store - Store
	waypoint0 waypoint1 waypoint2 waypoint3 waypoint4 waypoint5 waypoint6 waypoint7 - Waypoint
	camera0 camera1 camera2 camera3 - Camera
	objective0 objective1 objective2 objective3 - Objective
	)
(:init
	(at_soil_sample waypoint0)
	(at_rock_sample waypoint0)
	(at_rock_sample waypoint2)
	(at_rock_sample waypoint3)
	(at_rock_sample waypoint5)
	(at_rock_sample waypoint6)
	(at_rock_sample waypoint7)
	(at_lander general waypoint2)
	(channel_free general)
	(at rover0 waypoint4)
	(store_of rover0store rover0)
	(empty rover0store)
	(equipped_for_imaging rover0)
	(at rover1 waypoint4)
	(store_of rover1store rover1)
	(empty rover1store)
	(equipped_for_soil_analysis rover1)
	(equipped_for_rock_analysis rover1)
	(at rover2 waypoint7)
	(store_of rover2store rover2)
	(empty rover2store)
	(equipped_for_soil_analysis rover2)
	(equipped_for_imaging rover2)
	(at rover3 waypoint7)
	(store_of rover3store rover3)
	(empty rover3store)
	(equipped_for_soil_analysis rover3)
	(equipped_for_rock_analysis rover3)
	(equipped_for_imaging rover3)
	(on_board camera0 rover3)
	(calibration_target camera0 objective2)
	(supports camera0 high_res)
	(on_board camera1 rover2)
	(calibration_target camera1 objective1)
	(supports camera1 high_res)
	(on_board camera2 rover0)
	(calibration_target camera2 objective0)
	(supports camera2 low_res)
	(on_board camera3 rover3)
	(calibration_target camera3 objective3)
	(supports camera3 colour)
	(supports camera3 high_res)
	(supports camera3 low_res)
)

(:goal (and
(communicated_soil_data waypoint0)
(communicated_rock_data waypoint3)
(communicated_rock_data waypoint6)
(communicated_image_data objective2 low_res)
(communicated_image_data objective1 high_res)
(communicated_image_data objective3 low_res)
	)
)
)
