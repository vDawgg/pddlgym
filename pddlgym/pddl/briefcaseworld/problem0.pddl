; Problem taken from https://github.com/AI-Planning/classical-domains




(define (problem briefcase-o1)
(:domain briefcase)
(:objects l0 l1 - location
          o0 - portable)
(:init
(at o0 l1)
(is-at l1)

    ; action literals
    (move l0)
    (move l1)
    (take-out o0)
    (put-in o0)
    )
(:goal
(and
(at o0 l1)
(is-at l0)
)
)
)
