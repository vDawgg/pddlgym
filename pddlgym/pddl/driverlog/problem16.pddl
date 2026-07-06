; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem DLOG-5-5-15)
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
	package11
	package12
	package13
	package14
	package15
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
	s15
	)
	(:init
	(at driver1 s10)
	(driver driver1)
	(at driver2 s13)
	(driver driver2)
	(at driver3 s10)
	(driver driver3)
	(at driver4 s9)
	(driver driver4)
	(at driver5 s2)
	(driver driver5)
	(at truck1 s2)
	(empty truck1)
	(truck truck1)
	(at truck2 s8)
	(empty truck2)
	(truck truck2)
	(at truck3 s12)
	(empty truck3)
	(truck truck3)
	(at truck4 s3)
	(empty truck4)
	(truck truck4)
	(at truck5 s10)
	(empty truck5)
	(truck truck5)
	(at package1 s12)
	(obj package1)
	(at package2 s14)
	(obj package2)
	(at package3 s3)
	(obj package3)
	(at package4 s6)
	(obj package4)
	(at package5 s2)
	(obj package5)
	(at package6 s1)
	(obj package6)
	(at package7 s0)
	(obj package7)
	(at package8 s12)
	(obj package8)
	(at package9 s12)
	(obj package9)
	(at package10 s5)
	(obj package10)
	(at package11 s1)
	(obj package11)
	(at package12 s9)
	(obj package12)
	(at package13 s2)
	(obj package13)
	(at package14 s15)
	(obj package14)
	(at package15 s14)
	(obj package15)
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
	(location s15)
)
	(:goal (and
	(at driver2 s1)
	(at driver4 s1)
	(at driver5 s15)
	(at truck1 s14)
	(at truck2 s1)
	(at truck3 s5)
	(at truck4 s8)
	(at truck5 s6)
	(at package1 s1)
	(at package2 s15)
	(at package3 s10)
	(at package4 s3)
	(at package5 s6)
	(at package6 s8)
	(at package7 s0)
	(at package8 s13)
	(at package9 s1)
	(at package10 s11)
	(at package11 s8)
	(at package12 s6)
	(at package13 s10)
	(at package14 s1)
	(at package15 s4)
	))


)
