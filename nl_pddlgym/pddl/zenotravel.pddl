; Domain taken from https://github.com/AI-Planning/classical-domains
; Removed suboptimal zoom action in favor of cleaner instruction interface

(define (domain zeno-travel)
(:requirements :strips)
(:predicates
	 (at ?x ?c) (in ?p ?a) (fuel-level ?a ?l) (next ?l1 ?l2)(aircraft ?p) (person ?x) (city ?x) (flevel ?x)
	 (board ?person ?aircraft) (debark ?person ?aircraft) (fly ?aircraft ?city) (refuel ?aircraft))

; (:actions board debark fly refuel)

(:action board
 :parameters ( ?p ?a ?c)
 :precondition
	(and (board ?p ?a) (person ?p) (aircraft ?a) (city ?c)  (at ?p ?c) (at ?a ?c))
 :effect
	(and (in ?p ?a) (not (at ?p ?c))))

(:action debark
 :parameters ( ?p ?a ?c)
 :precondition
	(and (debark ?p ?a) (person ?p) (aircraft ?a) (city ?c)  (in ?p ?a) (at ?a ?c))
 :effect
	(and (at ?p ?c) (not (in ?p ?a))))

(:action fly
 :parameters ( ?a ?c1 ?c2 ?l1 ?l2)
 :precondition
	(and (fly ?a ?c2) (aircraft ?a) (city ?c1) (city ?c2) (flevel ?l1) (flevel ?l2)  (at ?a ?c1) (fuel-level ?a ?l1) (next ?l2 ?l1))
 :effect
	(and (at ?a ?c2) (fuel-level ?a ?l2) (not (at ?a ?c1)) (not (fuel-level ?a ?l1))))

(:action refuel
 :parameters ( ?a ?c ?l ?l1)
 :precondition
	(and (refuel ?a) (aircraft ?a) (city ?c) (flevel ?l) (flevel ?l1)  (fuel-level ?a ?l) (next ?l ?l1) (at ?a ?c))
 :effect
	(and (fuel-level ?a ?l1) (not (fuel-level ?a ?l))))

)
