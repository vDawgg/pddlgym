; Problem taken from https://github.com/AI-Planning/classical-domains




(define (problem briefcase-o2)
(:domain briefcase)
(:objects l0 l1 l2 - location
          o0 o1 - portable)
(:init
(at o0 l2)
(at o1 l2)
(is-at l2)

    ; action literals
    (move l0)
    (move l1)
    (move l2)
    (take-out o0)
    (take-out o1)
    (put-in o0)
    (put-in o1)
    )
(:goal
(and
(at o0 l0)
(at o1 l2)
(is-at l0)
)
)
)
