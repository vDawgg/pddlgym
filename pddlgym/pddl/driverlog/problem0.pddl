; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem DLOG-2-2-2)
	(:domain driverlog)
	(:objects
	driver1
	driver2
	truck1
	truck2
	package1
	package2
	s0
	s1
	s2
	)
	(:init
	(at driver1 s2)
	(driver driver1)
	(at driver2 s2)
	(driver driver2)
	(at truck1 s0)
	(empty truck1)
	(truck truck1)
	(at truck2 s0)
	(empty truck2)
	(truck truck2)
	(at package1 s0)
	(obj package1)
	(at package2 s0)
	(obj package2)
	(location s0)
	(location s1)
	(location s2)
)
	(:goal (and
	(at driver1 s1)
	(at truck1 s1)
	(at package1 s0)
	(at package2 s0)
	))


)
