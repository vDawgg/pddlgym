; Problem taken from https://github.com/AI-Planning/classical-domains




(define (problem briefcase-o5)
(:domain briefcase)
(:objects l0 l1 l2 l3 l4 l5 - location
          o0 o1 o2 o3 o4 - portable)
(:init
(at o0 l2)
(at o1 l0)
(at o2 l3)
(at o3 l4)
(at o4 l0)
(is-at l1)

    ; action literals
    (move l0)
    (move l1)
    (move l2)
    (move l3)
    (move l4)
    (move l5)
    (take-out o0)
    (take-out o1)
    (take-out o2)
    (take-out o3)
    (take-out o4)
    (put-in o0)
    (put-in o1)
    (put-in o2)
    (put-in o3)
    (put-in o4)
    )
(:goal
(and
(at o0 l5)
(at o1 l1)
(at o2 l1)
(at o3 l5)
(at o4 l5)
(is-at l0)
)
)
)
