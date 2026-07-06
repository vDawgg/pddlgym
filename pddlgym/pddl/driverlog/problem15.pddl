; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem DLOG-5-5-10)
	(:domain driverlog)
	(:objects
	driver1
	driver2
	driver3
	driver4
	driver5
	truck1
	truck2
	truck3
	truck4
	truck5
	package1
	package2
	package3
	package4
	package5
	package6
	package7
	package8
	package9
	package10
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
	s12
	s13
	s14
	)
	(:init
	(at driver1 s14)
	(driver driver1)
	(at driver2 s1)
	(driver driver2)
	(at driver3 s0)
	(driver driver3)
	(at driver4 s10)
	(driver driver4)
	(at driver5 s12)
	(driver driver5)
	(at truck1 s7)
	(empty truck1)
	(truck truck1)
	(at truck2 s1)
	(empty truck2)
	(truck truck2)
	(at truck3 s2)
	(empty truck3)
	(truck truck3)
	(at truck4 s13)
	(empty truck4)
	(truck truck4)
	(at truck5 s3)
	(empty truck5)
	(truck truck5)
	(at package1 s0)
	(obj package1)
	(at package2 s14)
	(obj package2)
	(at package3 s4)
	(obj package3)
	(at package4 s3)
	(obj package4)
	(at package5 s11)
	(obj package5)
	(at package6 s7)
	(obj package6)
	(at package7 s12)
	(obj package7)
	(at package8 s8)
	(obj package8)
	(at package9 s2)
	(obj package9)
	(at package10 s7)
	(obj package10)
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
	(location s12)
	(location s13)
	(location s14)
)
	(:goal (and
	(at driver1 s12)
	(at driver2 s11)
	(at driver3 s11)
	(at driver4 s12)
	(at driver5 s11)
	(at truck1 s5)
	(at truck2 s6)
	(at truck3 s8)
	(at truck4 s12)
	(at truck5 s14)
	(at package1 s13)
	(at package2 s0)
	(at package4 s11)
	(at package5 s9)
	(at package6 s2)
	(at package7 s3)
	(at package8 s6)
	(at package9 s4)
	(at package10 s8)
	))


)
