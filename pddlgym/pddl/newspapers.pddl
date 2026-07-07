(define (domain newspapers)
    (:requirements :strips :typing)
    (:types loc paper)
    (:predicates
        (at ?loc - loc)
        (isHomeBase ?loc - loc)
        (satisfied ?loc - loc)
        (wantsPaper ?loc - loc)
        (unpacked ?paper - paper)
        (carrying ?paper - paper)
	(pick-up ?paper)
	(move ?to)
	(deliver ?paper)
    )

    ; (:actions pick-up move deliver)

    (:action pick-up
        :parameters (?paper - paper ?loc - loc)
        :precondition (and
	    (pick-up ?paper)
            (at ?loc)
            (isHomeBase ?loc)
            (unpacked ?paper)
        )
        :effect (and
            (not (unpacked ?paper))
            (carrying ?paper)
        )
    )

    (:action move
        :parameters (?from - loc ?to - loc)
        :precondition (and
	    (move ?to)
            (at ?from)
        )
        :effect (and
            (not (at ?from))
            (at ?to)
        )
    )

    (:action deliver
        :parameters (?paper - paper ?loc - loc)
        :precondition (and
	    (deliver ?paper)
            (at ?loc)
            (wantsPaper ?loc)
            (carrying ?paper)
        )
        :effect (and
            (not (carrying ?paper))
            (not (wantsPaper ?loc))
            (satisfied ?loc)
        )
    )

)
