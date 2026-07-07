; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem ZTRAVEL-3-7)
(:domain zeno-travel)
(:objects
	plane1
	plane2
	plane3
	person1
	person2
	person3
	person4
	person5
	person6
	person7
	city0
	city1
	city2
	city3
	city4
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
	(fuel-level plane1 fl5)
	(at plane2 city2)
	(aircraft plane2)
	(fuel-level plane2 fl2)
	(at plane3 city1)
	(aircraft plane3)
	(fuel-level plane3 fl0)
	(at person1 city4)
	(person person1)
	(at person2 city1)
	(person person2)
	(at person3 city2)
	(person person3)
	(at person4 city0)
	(person person4)
	(at person5 city4)
	(person person5)
	(at person6 city3)
	(person person6)
	(at person7 city3)
	(person person7)
	(city city0)
	(city city1)
	(city city2)
	(city city3)
	(city city4)
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
    (board person1 plane3)
    (debark person1 plane3)
    (board person2 plane1)
    (debark person2 plane1)
    (board person2 plane2)
    (debark person2 plane2)
    (board person2 plane3)
    (debark person2 plane3)
    (board person3 plane1)
    (debark person3 plane1)
    (board person3 plane2)
    (debark person3 plane2)
    (board person3 plane3)
    (debark person3 plane3)
    (board person4 plane1)
    (debark person4 plane1)
    (board person4 plane2)
    (debark person4 plane2)
    (board person4 plane3)
    (debark person4 plane3)
    (board person5 plane1)
    (debark person5 plane1)
    (board person5 plane2)
    (debark person5 plane2)
    (board person5 plane3)
    (debark person5 plane3)
    (board person6 plane1)
    (debark person6 plane1)
    (board person6 plane2)
    (debark person6 plane2)
    (board person6 plane3)
    (debark person6 plane3)
    (board person7 plane1)
    (debark person7 plane1)
    (board person7 plane2)
    (debark person7 plane2)
    (board person7 plane3)
    (debark person7 plane3)
    (fly plane1 city0)
    (fly plane1 city1)
    (fly plane1 city2)
    (fly plane1 city3)
    (fly plane1 city4)
    (fly plane2 city0)
    (fly plane2 city1)
    (fly plane2 city2)
    (fly plane2 city3)
    (fly plane2 city4)
    (fly plane3 city0)
    (fly plane3 city1)
    (fly plane3 city2)
    (fly plane3 city3)
    (fly plane3 city4)
    (refuel plane1)
    (refuel plane2)
    (refuel plane3)
    )
(:goal (and
	(at person1 city2)
	(at person2 city0)
	(at person3 city4)
	(at person4 city3)
	(at person5 city1)
	(at person6 city4)
	(at person7 city4)
	))

)
