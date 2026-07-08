(define (problem mixed-f2-p1-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0) (:domain miconic)
  (:objects
        f0 f1 - floor
        p0 - passenger
  )
  (:init
    ;; Problem-relevant predicates
    (above f0 f1)
    (lift-at f0)
    (origin p0 f1)
    (destin p0 f0)

    ;; Grounded action predicates
    (up f0)
    (down f0)
    (up f1)
    (down f1)
    (board f0 p0)
    (depart f0 p0)
    (board f1 p0)
    (depart f1 p0)
  )
  (:goal
	(and
	(served p0)))
)
