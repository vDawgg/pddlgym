; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem DLOG-5-5-20)
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
	package16
	package17
	package18
	package19
	package20
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
	s16
	s17
	s18
	s19
	)
	(:init
	(at driver1 s11)
	(driver driver1)
	(at driver2 s6)
	(driver driver2)
	(at driver3 s1)
	(driver driver3)
	(at driver4 s2)
	(driver driver4)
	(at driver5 s4)
	(driver driver5)
	(at truck1 s12)
	(empty truck1)
	(truck truck1)
	(at truck2 s3)
	(empty truck2)
	(truck truck2)
	(at truck3 s8)
	(empty truck3)
	(truck truck3)
	(at truck4 s8)
	(empty truck4)
	(truck truck4)
	(at truck5 s2)
	(empty truck5)
	(truck truck5)
	(at package1 s3)
	(obj package1)
	(at package2 s18)
	(obj package2)
	(at package3 s0)
	(obj package3)
	(at package4 s2)
	(obj package4)
	(at package5 s3)
	(obj package5)
	(at package6 s10)
	(obj package6)
	(at package7 s7)
	(obj package7)
	(at package8 s7)
	(obj package8)
	(at package9 s18)
	(obj package9)
	(at package10 s3)
	(obj package10)
	(at package11 s16)
	(obj package11)
	(at package12 s10)
	(obj package12)
	(at package13 s13)
	(obj package13)
	(at package14 s14)
	(obj package14)
	(at package15 s3)
	(obj package15)
	(at package16 s2)
	(obj package16)
	(at package17 s18)
	(obj package17)
	(at package18 s15)
	(obj package18)
	(at package19 s16)
	(obj package19)
	(at package20 s9)
	(obj package20)
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
	(location s16)
	(location s17)
	(location s18)
	(location s19)
)
	(:goal (and
	(at driver1 s1)
	(at driver5 s9)
	(at truck1 s17)
	(at truck2 s0)
	(at truck3 s3)
	(at truck5 s9)
	(at package1 s1)
	(at package2 s7)
	(at package4 s10)
	(at package5 s15)
	(at package6 s7)
	(at package7 s10)
	(at package9 s7)
	(at package10 s10)
	(at package11 s13)
	(at package12 s12)
	(at package13 s12)
	(at package14 s15)
	(at package15 s18)
	(at package16 s8)
	(at package17 s16)
	(at package18 s3)
	(at package19 s2)
	))


)
