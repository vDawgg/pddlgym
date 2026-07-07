; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem ZTRAVEL-2-6)
(:domain zeno-travel)
(:objects
	plane1
	plane2
	person1
	person2
	person3
	person4
	person5
	person6
	city0
	city1
	city2
	city3
	fl0
	fl1
	fl2
	fl3
	fl4
	fl5
	fl6
	)
(:init
	(at plane1 city2)
	(aircraft plane1)
	(fuel-level plane1 fl1)
	(at plane2 city1)
	(aircraft plane2)
	(fuel-level plane2 fl1)
	(at person1 city3)
	(person person1)
	(at person2 city3)
	(person person2)
	(at person3 city3)
	(person person3)
	(at person4 city1)
	(person person4)
	(at person5 city3)
	(person person5)
	(at person6 city0)
	(person person6)
	(city city0)
	(city city1)
	(city city2)
	(city city3)
	(next fl0 fl1)
	(next fl1 fl2)
	(next fl2 fl3)
	(next fl3 fl4)
	(next fl4 fl5)
	(next fl5 fl6)
	(flevel fl0)
	(flevel fl1)
	(flevel fl2)
	(flevel fl3)
	(flevel fl4)
	(flevel fl5)
	(flevel fl6)

    ; action literals
    (board person1 plane1)
    (debark person1 plane1)
    (board person1 plane2)
    (debark person1 plane2)
    (board person2 plane1)
    (debark person2 plane1)
    (board person2 plane2)
    (debark person2 plane2)
    (board person3 plane1)
    (debark person3 plane1)
    (board person3 plane2)
    (debark person3 plane2)
    (board person4 plane1)
    (debark person4 plane1)
    (board person4 plane2)
    (debark person4 plane2)
    (board person5 plane1)
    (debark person5 plane1)
    (board person5 plane2)
    (debark person5 plane2)
    (board person6 plane1)
    (debark person6 plane1)
    (board person6 plane2)
    (debark person6 plane2)
    (fly plane1 city0)
    (fly plane1 city1)
    (fly plane1 city2)
    (fly plane1 city3)
    (fly plane2 city0)
    (fly plane2 city1)
    (fly plane2 city2)
    (fly plane2 city3)
    (refuel plane1)
    (refuel plane2)
    )
(:goal (and
	(at plane2 city1)
	(at person1 city2)
	(at person3 city3)
	(at person4 city3)
	(at person5 city2)
	(at person6 city2)
	))

)
