;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; 4 op-blocks world
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain blocks)
    (:requirements :strips :typing)
    (:types block)
    (:predicates
        (on ?x - block ?y - block)
        (ontable ?x - block)
        (clear ?x - block)
        (handempty)
        (handfull)
        (holding ?x - block)
	(pickup ?x - block)
        (putdown ?x - block)
        (stack ?x - block ?y - block)
        (unstack ?x - block)
    )

    ; (:actions pickup putdown stack unstack)

    (:action pick-up
        :parameters (?x - block)
        :precondition (and
	    (pickup ?x)
            (clear ?x)
            (ontable ?x)
            (handempty)
        )
        :effect (and
            (not (ontable ?x))
            (not (clear ?x))
            (not (handempty))
            (handfull)
            (holding ?x)
        )
    )

    (:action put-down
        :parameters (?x - block)
        :precondition (and
	    (putdown ?x)
            (holding ?x)
            (handfull)
        )
        :effect (and
            (not (holding ?x))
            (clear ?x)
            (handempty)
            (not (handfull))
            (ontable ?x))
        )

    (:action stack
        :parameters (?x - block ?y - block)
        :precondition (and
	    (stack ?x ?y)
            (holding ?x)
            (clear ?y)
            (handfull)
        )
        :effect (and
            (not (holding ?x))
            (not (clear ?y))
            (clear ?x)
            (handempty)
            (not (handfull))
            (on ?x ?y)
        )
    )

    (:action unstack
        :parameters (?x - block ?y - block)
        :precondition (and
	    (unstack ?x)
            (on ?x ?y)
            (clear ?x)
            (handempty)
        )
        :effect (and
            (holding ?x)
            (clear ?y)
            (not (clear ?x))
            (not (handempty))
            (handfull)
            (not (on ?x ?y))
        )
    )
)
