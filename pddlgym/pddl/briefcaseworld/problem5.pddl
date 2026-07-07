; Problem taken from https://github.com/AI-Planning/classical-domains




(define (problem briefcase-o6)
(:domain briefcase)
(:objects l0 l1 l2 l3 l4 l5 l6 - location
          o0 o1 o2 o3 o4 o5 - portable)
(:init
(at o0 l0)
(at o1 l0)
(at o2 l2)
(at o3 l4)
(at o4 l5)
(at o5 l3)
(is-at l3)

    ; action literals
    (move l0)
    (move l1)
    (move l2)
    (move l3)
    (move l4)
    (move l5)
    (move l6)
    (take-out o0)
    (take-out o1)
    (take-out o2)
    (take-out o3)
    (take-out o4)
    (take-out o5)
    (put-in o0)
    (put-in o1)
    (put-in o2)
    (put-in o3)
    (put-in o4)
    (put-in o5)
    )
(:goal
(and
(at o0 l1)
(at o1 l4)
(at o2 l6)
(at o3 l4)
(at o4 l5)
(at o5 l0)
(is-at l3)
)
)
)
