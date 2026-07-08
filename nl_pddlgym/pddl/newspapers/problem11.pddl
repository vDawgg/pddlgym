
(define (problem newspaper) (:domain newspapers)
  (:objects
        loc-0 - loc
	loc-1 - loc
	loc-10 - loc
	loc-11 - loc
	loc-12 - loc
	loc-13 - loc
	loc-2 - loc
	loc-3 - loc
	loc-4 - loc
	loc-5 - loc
	loc-6 - loc
	loc-7 - loc
	loc-8 - loc
	loc-9 - loc
	paper-0 - paper
	paper-1 - paper
	paper-10 - paper
	paper-11 - paper
	paper-12 - paper
	paper-13 - paper
	paper-14 - paper
	paper-15 - paper
	paper-16 - paper
	paper-17 - paper
	paper-18 - paper
	paper-19 - paper
	paper-2 - paper
	paper-20 - paper
	paper-3 - paper
	paper-4 - paper
	paper-5 - paper
	paper-6 - paper
	paper-7 - paper
	paper-8 - paper
	paper-9 - paper
  )
  (:init
	(at loc-0)
	(ishomebase loc-0)
	(unpacked paper-0)
	(unpacked paper-10)
	(unpacked paper-11)
	(unpacked paper-12)
	(unpacked paper-13)
	(unpacked paper-14)
	(unpacked paper-15)
	(unpacked paper-16)
	(unpacked paper-17)
	(unpacked paper-18)
	(unpacked paper-19)
	(unpacked paper-1)
	(unpacked paper-20)
	(unpacked paper-2)
	(unpacked paper-3)
	(unpacked paper-4)
	(unpacked paper-5)
	(unpacked paper-6)
	(unpacked paper-7)
	(unpacked paper-8)
	(unpacked paper-9)
	(wantspaper loc-10)
	(wantspaper loc-11)
	(wantspaper loc-12)
	(wantspaper loc-13)
	(wantspaper loc-1)
	(wantspaper loc-2)
	(wantspaper loc-3)
	(wantspaper loc-4)
	(wantspaper loc-5)
	(wantspaper loc-6)
	(wantspaper loc-7)
	(wantspaper loc-8)
	(wantspaper loc-9)

    ; action literals
    (pick-up paper-0)
    (pick-up paper-1)
    (pick-up paper-10)
    (pick-up paper-11)
    (pick-up paper-12)
    (pick-up paper-13)
    (pick-up paper-14)
    (pick-up paper-15)
    (pick-up paper-16)
    (pick-up paper-17)
    (pick-up paper-18)
    (pick-up paper-19)
    (pick-up paper-2)
    (pick-up paper-20)
    (pick-up paper-3)
    (pick-up paper-4)
    (pick-up paper-5)
    (pick-up paper-6)
    (pick-up paper-7)
    (pick-up paper-8)
    (pick-up paper-9)
    (move loc-0)
    (move loc-1)
    (move loc-10)
    (move loc-11)
    (move loc-12)
    (move loc-13)
    (move loc-2)
    (move loc-3)
    (move loc-4)
    (move loc-5)
    (move loc-6)
    (move loc-7)
    (move loc-8)
    (move loc-9)
    (deliver paper-0)
    (deliver paper-1)
    (deliver paper-10)
    (deliver paper-11)
    (deliver paper-12)
    (deliver paper-13)
    (deliver paper-14)
    (deliver paper-15)
    (deliver paper-16)
    (deliver paper-17)
    (deliver paper-18)
    (deliver paper-19)
    (deliver paper-2)
    (deliver paper-20)
    (deliver paper-3)
    (deliver paper-4)
    (deliver paper-5)
    (deliver paper-6)
    (deliver paper-7)
    (deliver paper-8)
    (deliver paper-9)
    )
  (:goal (and
	(satisfied loc-1)
	(satisfied loc-2)
	(satisfied loc-3)
	(satisfied loc-4)
	(satisfied loc-5)
	(satisfied loc-6)
	(satisfied loc-7)
	(satisfied loc-8)
	(satisfied loc-9)
	(satisfied loc-10)
	(satisfied loc-11)
	(satisfied loc-12)
	(satisfied loc-13)))
)
