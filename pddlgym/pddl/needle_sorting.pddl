(define (domain NEEDLE_SORTING)
    (:requirements :strips :negative-preconditions)
    (:predicates
        (needle ?n)
        (robot-at ?location)
        (needle-at ?needle ?location)
        (holding ?needle)
        (handempty)
	(move ?to)
	(pick)
	(place)
    )

    ; (:actions move pick place)

    (:action move
        :parameters (?from ?to)
        :precondition (and
	    (move ?to)
            (robot-at ?from)
            (not (robot-at ?to))
        )
        :effect (and
            (robot-at ?to)
            (not (robot-at ?from))
        )
    )

    (:action pick
        :parameters (?needle ?location)
        :precondition (and
	    (pick)
            (needle ?needle)
            (not (holding ?needle))
            (robot-at ?location)
            (needle-at ?needle ?location)
            (handempty)
        )
        :effect (and
            (holding ?needle)
            (not (needle-at ?needle ?location))
            (not (handempty))
        )
    )

    (:action place
        :parameters (?needle ?location)
        :precondition (and
	    (place)
            (needle ?needle)
            (holding ?needle)
            (robot-at ?location)
            (not (handempty))
        )
        :effect (and
            (not (holding ?needle))
            (needle-at ?needle ?location)
            (handempty)
        )
    )
)
