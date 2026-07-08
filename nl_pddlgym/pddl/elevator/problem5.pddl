(define (problem mixed-f3-p2-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0) (:domain miconic)
  (:objects
        f0 f1 f2 - floor
        p0 p1 - passenger
  )
  (:init
    ;; Problem-relevant predicates
    (above f0 f1)
    (above f0 f2)
    (above f1 f2)
    (lift-at f0)
    (origin p0 f0)
    (destin p0 f1)
    (origin p1 f1)
    (destin p1 f2)

    ;; Grounded action predicates
    (up f0)
    (down f0)
    (up f1)
    (down f1)
    (up f2)
    (down f2)
    (board f0 p0)
    (depart f0 p0)
    (board f0 p1)
    (depart f0 p1)
    (board f1 p0)
    (depart f1 p0)
    (board f1 p1)
    (depart f1 p1)
    (board f2 p0)
    (depart f2 p0)
    (board f2 p1)
    (depart f2 p1)
  )
  (:goal
	(and
	(served p0)
	(served p1)))
)
