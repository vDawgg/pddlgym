; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem DLOG-2-3-6)
	(:domain driverlog)
	(:objects
	driver1
	driver2
	truck1
	truck2
	truck3
	package1
	package2
	package3
	package4
	package5
	package6
	s0
	s1
	s2
	s3
	s4
	s5
	s6
	)
	(:init
	(at driver1 s6)
	(driver driver1)
	(at driver2 s0)
	(driver driver2)
	(at truck1 s0)
	(empty truck1)
	(truck truck1)
	(at truck2 s2)
	(empty truck2)
	(truck truck2)
	(at truck3 s2)
	(empty truck3)
	(truck truck3)
	(at package1 s6)
	(obj package1)
	(at package2 s2)
	(obj package2)
	(at package3 s3)
	(obj package3)
	(at package4 s0)
	(obj package4)
	(at package5 s5)
	(obj package5)
	(at package6 s5)
	(obj package6)
	(location s0)
	(location s1)
	(location s2)
	(location s3)
	(location s4)
	(location s5)
	(location s6)
)
	(:goal (and
	(at driver2 s4)
	(at truck2 s4)
	(at package1 s6)
	(at package2 s3)
	(at package3 s4)
	(at package4 s6)
	(at package5 s1)
	))


)
