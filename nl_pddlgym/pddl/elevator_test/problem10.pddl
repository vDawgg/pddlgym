
(define (problem mixed-f20-p10-u0-v0-g0-a0-n0-a0-b0-n0-f0-r0) (:domain miconic)
  (:objects
        f0 - floor
	f1 - floor
	f10 - floor
	f11 - floor
	f12 - floor
	f13 - floor
	f14 - floor
	f15 - floor
	f16 - floor
	f17 - floor
	f18 - floor
	f19 - floor
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
	p7 - passenger
	p8 - passenger
	p9 - passenger
  )
  (:goal (and
	(served p0)
	(served p1)
	(served p2)
	(served p3)
	(served p4)
	(served p5)
	(served p6)
	(served p7)
	(served p8)
	(served p9)))
  (:init
	(board p0)
	(board p1)
	(board p2)
	(board p3)
	(board p4)
	(board p5)
	(board p6)
	(board p7)
	(board p8)
	(board p9)
	(depart p0)
	(depart p1)
	(depart p2)
	(depart p3)
	(depart p4)
	(depart p5)
	(depart p6)
	(depart p7)
	(depart p8)
	(depart p9)
	(destin p0 f6)
	(destin p1 f15)
	(destin p2 f15)
	(destin p3 f12)
	(destin p4 f1)
	(destin p5 f7)
	(destin p6 f19)
	(destin p7 f6)
	(destin p8 f6)
	(destin p9 f16)
	(down)
	(lift-at f0)
	(origin p0 f3)
	(origin p1 f17)
	(origin p2 f13)
	(origin p3 f6)
	(origin p4 f9)
	(origin p5 f2)
	(origin p6 f10)
	(origin p7 f3)
	(origin p8 f0)
	(origin p9 f12)

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
    (above f13 f14)
    (above f14 f15)
    (above f15 f16)
    (above f16 f17)
    (above f17 f18)
    (above f18 f19)
	(up)
))
