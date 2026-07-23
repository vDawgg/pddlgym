
(define (problem mixed-f14-p7-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0) (:domain miconic)
  (:objects
        f0 - floor
	f1 - floor
	f10 - floor
	f11 - floor
	f12 - floor
	f13 - floor
	f2 - floor
	f3 - floor
	f4 - floor
	f5 - floor
	f6 - floor
	f7 - floor
	f8 - floor
	f9 - floor
	p0 - passenger
	p1 - passenger
	p2 - passenger
	p3 - passenger
	p4 - passenger
	p5 - passenger
	p6 - passenger
  )
  (:goal (and
	(served p0)
	(served p1)
	(served p2)
	(served p3)
	(served p4)
	(served p5)
	(served p6)))
  (:init
	(board p0)
	(board p1)
	(board p2)
	(board p3)
	(board p4)
	(board p5)
	(board p6)
	(depart p0)
	(depart p1)
	(depart p2)
	(depart p3)
	(depart p4)
	(depart p5)
	(depart p6)
	(destin p0 f4)
	(destin p1 f5)
	(destin p2 f3)
	(destin p3 f2)
	(destin p4 f3)
	(destin p5 f5)
	(destin p6 f11)
	(down)
	(lift-at f0)
	(origin p0 f1)
	(origin p1 f9)
	(origin p2 f1)
	(origin p3 f10)
	(origin p4 f1)
	(origin p5 f2)
	(origin p6 f6)

    (above f0 f1)
    (above f1 f2)
    (above f2 f3)
    (above f3 f4)
    (above f4 f5)
    (above f5 f6)
    (above f6 f7)
    (above f7 f8)
    (above f8 f9)
    (above f9 f10)
    (above f10 f11)
    (above f11 f12)
    (above f12 f13)
	(up)
))
