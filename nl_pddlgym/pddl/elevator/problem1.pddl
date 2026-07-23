(define (problem mixed-f6-p3-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0) (:domain miconic)
  (:objects
        f0 f1 f2 f3 f4 f5 - floor
        p0 p1 p2 - passenger
  )
  (:init
    ;; Problem-relevant predicates
    (lift-at f0)
    (origin p0 f1)
    (destin p0 f4)
    (origin p1 f3)
    (destin p1 f1)
    (origin p2 f5)
    (destin p2 f1)

    (above f0 f1)
    (above f1 f2)
    (above f2 f3)
    (above f3 f4)
    (above f4 f5)

    ;; Grounded action predicates
    (up)
    (down)
    (board p0)
    (depart p0)
    (board p1)
    (depart p1)
    (board p2)
    (depart p2)
  )
  (:goal
	(and
	(served p0)
	(served p1)
	(served p2)))
)
