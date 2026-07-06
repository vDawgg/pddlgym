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
	s7
	s8
	s9
	)
	(:init
	(at driver1 s1)
	(driver driver1)
	(at driver2 s3)
	(driver driver2)
	(at truck1 s7)
	(empty truck1)
	(truck truck1)
	(at truck2 s9)
	(empty truck2)
	(truck truck2)
	(at truck3 s2)
	(empty truck3)
	(truck truck3)
	(at package1 s3)
	(obj package1)
	(at package2 s4)
	(obj package2)
	(at package3 s9)
	(obj package3)
	(at package4 s7)
	(obj package4)
	(at package5 s4)
	(obj package5)
	(at package6 s1)
	(obj package6)
	(location s0)
	(location s1)
	(location s2)
	(location s3)
	(location s4)
	(location s5)
	(location s6)
	(location s7)
	(location s8)
	(location s9)
)
	(:goal (and
	(at driver1 s4)
	(at driver2 s9)
	(at truck2 s5)
	(at truck3 s0)
	(at package1 s2)
	(at package2 s2)
	(at package3 s9)
	(at package4 s1)
	(at package5 s0)
	(at package6 s2)
	))


)
