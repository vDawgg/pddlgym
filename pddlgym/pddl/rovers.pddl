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

)


(:action navigate
:parameters (?x - rover ?y - waypoint ?z - waypoint)
:precondition (and (at ?x ?y)
	    )
:effect (and (not (at ?x ?y)) (at ?x ?z)
		)
)

(:action sample_soil
:parameters (?x - rover ?s - store ?p - waypoint)
:precondition (and (at ?x ?p) (at_soil_sample ?p) (equipped_for_soil_analysis ?x) (store_of ?s ?x) (empty ?s)
		)
:effect (and (not (empty ?s)) (full ?s) (have_soil_analysis ?x ?p) (not (at_soil_sample ?p))
		)
)

(:action sample_rock
:parameters (?x - rover ?s - store ?p - waypoint)
:precondition (and (at ?x ?p) (at_rock_sample ?p) (equipped_for_rock_analysis ?x) (store_of ?s ?x)(empty ?s)
		)
:effect (and (not (empty ?s)) (full ?s) (have_rock_analysis ?x ?p) (not (at_rock_sample ?p))
		)
)

(:action drop
:parameters (?x - rover ?y - store)
:precondition (and (store_of ?y ?x) (full ?y)
		)
:effect (and (not (full ?y)) (empty ?y)
	)
)

(:action calibrate
 :parameters (?r - rover ?i - camera ?t - objective)
 :precondition (and (equipped_for_imaging ?r) (calibration_target ?i ?t) (on_board ?i ?r)
		)
 :effect (calibrated ?i ?r)
)




(:action take_image
 :parameters (?r - rover ?o - objective ?i - camera ?m - mode)
 :precondition (and (calibrated ?i ?r)
			 (on_board ?i ?r)
                      (equipped_for_imaging ?r)
                      (supports ?i ?m)
               )
 :effect (and (have_image ?r ?o ?m)(not (calibrated ?i ?r))
		)
)


(:action communicate_soil_data
 :parameters (?r - rover ?l - lander ?p - waypoint)
 :precondition (and (have_soil_analysis ?r ?p)
                   (channel_free ?l)
            )
 :effect (and (communicated_soil_data ?p)
	)
)

(:action communicate_rock_data
 :parameters (?r - rover ?l - lander ?p - waypoint)
 :precondition (and (have_rock_analysis ?r ?p)
                   (channel_free ?l)
            )
 :effect (and (communicated_rock_data ?p)
          )
)


(:action communicate_image_data
 :parameters (?r - rover ?l - lander ?o - objective ?m - mode)
 :precondition (and (have_image ?r ?o ?m)
            )
 :effect (and (communicated_image_data ?o ?m)
          )
)

)
