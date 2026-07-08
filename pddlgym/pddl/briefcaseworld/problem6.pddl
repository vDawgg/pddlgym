; Problem taken from https://github.com/AI-Planning/classical-domains




(define (problem briefcase-o7)
(:domain briefcase)
(:objects l0 l1 l2 l3 l4 l5 l6 l7 - location
          o0 o1 o2 o3 o4 o5 o6 - portable)
(:init
(at o0 l0)
(at o1 l6)
(at o2 l5)
(at o3 l5)
(at o4 l7)
(at o5 l6)
(at o6 l5)
(is-at l6)

    ; action literals
    (move l0)
    (move l1)
    (move l2)
    (move l3)
    (move l4)
    (move l5)
    (move l6)
    (move l7)
    (take-out o0)
    (take-out o1)
    (take-out o2)
    (take-out o3)
    (take-out o4)
    (take-out o5)
    (take-out o6)
    (put-in o0)
    (put-in o1)
    (put-in o2)
    (put-in o3)
    (put-in o4)
    (put-in o5)
    (put-in o6)
    )
(:goal
(and
(at o0 l4)
(at o1 l3)
(at o2 l1)
(at o3 l3)
(at o4 l5)
(at o5 l2)
(at o6 l6)
(is-at l7)
)
)
)
