(define (problem mixed-f2-p1-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0) (:domain miconic)
  (:objects
        f0 f1 - floor
        p0 - passenger
  )
  (:init
    ;; Problem-relevant predicates
    (lift-at f0)
    (origin p0 f1)
    (destin p0 f0)

    (above f0 f1)

    ;; Grounded action predicates
    (up)
    (down)
    (board p0)
    (depart p0)
  )
  (:goal
	(and
	(served p0)))
)
