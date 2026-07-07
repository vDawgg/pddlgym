; Domain taken from https://github.com/AI-Planning/classical-domains
; Removed navigation and visibility constraints to avoid having to model reachability in NL descriptions.

(define (domain Rover)
(:requirements :typing :strips)
(:types rover waypoint store camera mode lander objective)

(:predicates (at ?x - rover ?y - waypoint)
             (at_lander ?x - lander ?y - waypoint)
	     (equipped_for_soil_analysis ?r - rover)
             (equipped_for_rock_analysis ?r - rover)
             (equipped_for_imaging ?r - rover)
             (empty ?s - store)
             (have_rock_analysis ?r - rover ?w - waypoint)
             (have_soil_analysis ?r - rover ?w - waypoint)
             (full ?s - store)
	     (calibrated ?c - camera ?r - rover)
	     (supports ?c - camera ?m - mode)
             (have_image ?r - rover ?o - objective ?m - mode)
             (communicated_soil_data ?w - waypoint)
             (communicated_rock_data ?w - waypoint)
             (communicated_image_data ?o - objective ?m - mode)
	     (at_soil_sample ?w - waypoint)
	     (at_rock_sample ?w - waypoint)
	     (store_of ?s - store ?r - rover)
	     (calibration_target ?i - camera ?o - objective)
	     (on_board ?i - camera ?r - rover)
	     (channel_free ?l - lander)
	     (navigate ?rover ?to)
	     (sample_soil ?rover)
	     (sample_rock ?rover)
	     (drop ?rover)
	     (calibrate ?camera ?objective)
	     (take_image ?objective ?camera ?mode)
	     (communicate_soil_data ?rover ?position)
	     (communicate_rock_data ?rover ?position)
	     (communicate_image_data ?rover ?objective ?mode)
)

; (:actions navigate sample_soil sample_rock drop calibrate take_image communicate_soil_data communicate_rock_data communicate_image_data)

(:action navigate
:parameters (?x - rover ?y - waypoint ?z - waypoint)
:precondition (and
	(navigate ?x ?z)
	(at ?x ?y)
	    )
:effect (and (not (at ?x ?y)) (at ?x ?z)
		)
)

(:action sample_soil
:parameters (?x - rover ?s - store ?p - waypoint)
:precondition (and
	(sample_soil ?x)
	(at ?x ?p) (at_soil_sample ?p) (equipped_for_soil_analysis ?x) (store_of ?s ?x) (empty ?s)
		)
:effect (and (not (empty ?s)) (full ?s) (have_soil_analysis ?x ?p) (not (at_soil_sample ?p))
		)
)

(:action sample_rock
:parameters (?x - rover ?s - store ?p - waypoint)
:precondition (and
	(sample_rock ?x)
	(at ?x ?p) (at_rock_sample ?p) (equipped_for_rock_analysis ?x) (store_of ?s ?x)(empty ?s)
		)
:effect (and (not (empty ?s)) (full ?s) (have_rock_analysis ?x ?p) (not (at_rock_sample ?p))
		)
)

(:action drop
:parameters (?x - rover ?y - store)
:precondition (and
	(drop ?x)
	(store_of ?y ?x) (full ?y)
		)
:effect (and (not (full ?y)) (empty ?y)
	)
)

(:action calibrate
 :parameters (?r - rover ?i - camera ?t - objective)
 :precondition (and
	(calibrate ?i ?t)
 	(equipped_for_imaging ?r) (calibration_target ?i ?t) (on_board ?i ?r)
		)
 :effect (calibrated ?i ?r)
)




(:action take_image
 :parameters (?r - rover ?o - objective ?i - camera ?m - mode)
 :precondition (and
			(take_image ?o ?i ?m)
 			(calibrated ?i ?r)
			 (on_board ?i ?r)
                      (equipped_for_imaging ?r)
                      (supports ?i ?m)
               )
 :effect (and (have_image ?r ?o ?m)(not (calibrated ?i ?r))
		)
)


(:action communicate_soil_data
 :parameters (?r - rover ?l - lander ?p - waypoint)
 :precondition (and
		(communicate_soil_data ?r ?p)
 		(have_soil_analysis ?r ?p)
                   (channel_free ?l)
            )
 :effect (and (communicated_soil_data ?p)
	)
)

(:action communicate_rock_data
 :parameters (?r - rover ?l - lander ?p - waypoint)
 :precondition (and
		(communicate_rock_data ?r ?p)
 		(have_rock_analysis ?r ?p)
                   (channel_free ?l)
            )
 :effect (and (communicated_rock_data ?p)
          )
)


(:action communicate_image_data
 :parameters (?r - rover ?l - lander ?o - objective ?m - mode)
 :precondition (and
		(communicate_image_data ?r ?o ?m)
 		(have_image ?r ?o ?m)
            )
 :effect (and (communicated_image_data ?o ?m)
          )
)

)
