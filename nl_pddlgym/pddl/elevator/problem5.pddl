(define (problem mixed-f3-p2-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0) (:domain miconic)
  (:objects
        f0 f1 f2 - floor
        p0 p1 - passenger
  )
  (:init
    ;; Problem-relevant predicates
    (lift-at f0)
    (origin p0 f0)
    (destin p0 f1)
    (origin p1 f1)
    (destin p1 f2)

    (above f0 f1)
    (above f1 f2)

    ;; Grounded action predicates
    (up)
    (down)
    (board p0)
    (depart p0)
    (board p1)
    (depart p1)
  )
  (:goal
	(and
	(served p0)
	(served p1)))
)
