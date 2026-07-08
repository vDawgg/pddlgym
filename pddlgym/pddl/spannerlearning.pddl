(define (domain spanner)
(:requirements :typing :strips)
(:types
	location locatable - object
	man nut spanner - locatable
)

(:predicates
	(at ?m - locatable ?l - location)
	(carrying ?m - man ?s - spanner)
	(useable ?s - spanner)
	(link ?l1 - location ?l2 - location)
	(tightened ?n - nut)
	(loose ?n - nut)
	(walk ?end - location)
	(pickup_spanner ?spanner - spanner)
	(tighten_nut ?nut - nut))

; (:actions walk pickup_spanner tighten_nut)

(:action walk
        :parameters (?start - location ?end - location ?m - man)
        :precondition (and
			   (walk ?end)
			   (at ?m ?start)
                           (link ?start ?end))
        :effect (and (not (at ?m ?start)) (at ?m ?end)))

(:action pickup_spanner
        :parameters (?l - location ?s - spanner ?m - man)
        :precondition (and
			   (pickup_spanner ?s)
			   (at ?m ?l)
                           (at ?s ?l))
        :effect (and (not (at ?s ?l))
                     (carrying ?m ?s)))

(:action tighten_nut
        :parameters (?l - location ?s - spanner ?m - man ?n - nut)
        :precondition (and
			   (tighten_nut ?n)
			   (at ?m ?l)
		      	   (at ?n ?l)
			   (carrying ?m ?s)
			   (useable ?s)
			   (loose ?n))
        :effect (and (not (loose ?n))(not (useable ?s)) (tightened ?n)))
)
