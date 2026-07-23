(define (problem mixed-f5-p4-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0) (:domain miconic)
  (:objects
        f0 f1 f2 f3 f4 - floor
        p0 p1 p2 p3 - passenger
  )
  (:init
    ;; Problem-relevant predicates
    (lift-at f0)
    (origin p0 f0)
    (destin p0 f1)
    (origin p1 f1)
    (destin p1 f2)
    (origin p2 f2)
    (destin p2 f3)
    (origin p3 f3)
    (destin p3 f4)

    (above f0 f1)
    (above f1 f2)
    (above f2 f3)
    (above f3 f4)

    ;; Grounded action predicates
    (up)
    (down)
    (board p0)
    (depart p0)
    (board p1)
    (depart p1)
    (board p2)
    (depart p2)
    (board p3)
    (depart p3)
  )
  (:goal
	(and
	(served p0)
	(served p1)
	(served p2)
	(served p3)))
)
