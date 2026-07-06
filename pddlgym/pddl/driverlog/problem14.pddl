; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem DLOG-4-4-8)
	(:domain driverlog)
	(:objects
	driver1
	driver2
	driver3
	driver4
	truck1
	truck2
	truck3
	truck4
	package1
	package2
	package3
	package4
	package5
	package6
	package7
	package8
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
	s10
	s11
	)
	(:init
	(at driver1 s8)
	(driver driver1)
	(at driver2 s5)
	(driver driver2)
	(at driver3 s5)
	(driver driver3)
	(at driver4 s10)
	(driver driver4)
	(at truck1 s3)
	(empty truck1)
	(truck truck1)
	(at truck2 s9)
	(empty truck2)
	(truck truck2)
	(at truck3 s3)
	(empty truck3)
	(truck truck3)
	(at truck4 s6)
	(empty truck4)
	(truck truck4)
	(at package1 s3)
	(obj package1)
	(at package2 s2)
	(obj package2)
	(at package3 s8)
	(obj package3)
	(at package4 s11)
	(obj package4)
	(at package5 s1)
	(obj package5)
	(at package6 s8)
	(obj package6)
	(at package7 s9)
	(obj package7)
	(at package8 s10)
	(obj package8)
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
	(location s10)
	(location s11)
)
	(:goal (and
	(at driver3 s8)
	(at truck3 s8)
	(at package1 s2)
	(at package2 s5)
	(at package3 s1)
	(at package4 s7)
	(at package5 s0)
	(at package6 s11)
	(at package7 s2)
	(at package8 s0)
	))


)
