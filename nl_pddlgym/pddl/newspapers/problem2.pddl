
(define (problem newspaper) (:domain newspapers)
  (:objects
        loc-0 - loc
	loc-1 - loc
	loc-2 - loc
	loc-3 - loc
	loc-4 - loc
	paper-0 - paper
	paper-1 - paper
	paper-2 - paper
	paper-3 - paper
	paper-4 - paper
	paper-5 - paper
	paper-6 - paper
	paper-7 - paper
	paper-8 - paper
  )
  (:init
	(at loc-0)
	(ishomebase loc-0)
	(unpacked paper-0)
	(unpacked paper-1)
	(unpacked paper-2)
	(unpacked paper-3)
	(unpacked paper-4)
	(unpacked paper-5)
	(unpacked paper-6)
	(unpacked paper-7)
	(unpacked paper-8)
	(wantspaper loc-1)
	(wantspaper loc-2)
	(wantspaper loc-3)
	(wantspaper loc-4)

    ; action literals
    (pick-up paper-0)
    (pick-up paper-1)
    (pick-up paper-2)
    (pick-up paper-3)
    (pick-up paper-4)
    (pick-up paper-5)
    (pick-up paper-6)
    (pick-up paper-7)
    (pick-up paper-8)
    (move loc-0)
    (move loc-1)
    (move loc-2)
    (move loc-3)
    (move loc-4)
    (deliver paper-0)
    (deliver paper-1)
    (deliver paper-2)
    (deliver paper-3)
    (deliver paper-4)
    (deliver paper-5)
    (deliver paper-6)
    (deliver paper-7)
    (deliver paper-8)
    )
  (:goal (and
	(satisfied loc-1)
	(satisfied loc-2)
	(satisfied loc-3)
	(satisfied loc-4)))
)
