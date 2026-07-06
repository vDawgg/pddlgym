; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem DLOG-5-5-25)
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
	package21
	package22
	package23
	package24
	package25
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
	(at driver1 s3)
	(driver driver1)
	(at driver2 s11)
	(driver driver2)
	(at driver3 s8)
	(driver driver3)
	(at driver4 s12)
	(driver driver4)
	(at driver5 s3)
	(driver driver5)
	(at truck1 s4)
	(empty truck1)
	(truck truck1)
	(at truck2 s8)
	(empty truck2)
	(truck truck2)
	(at truck3 s19)
	(empty truck3)
	(truck truck3)
	(at truck4 s0)
	(empty truck4)
	(truck truck4)
	(at truck5 s6)
	(empty truck5)
	(truck truck5)
	(at package1 s19)
	(obj package1)
	(at package2 s17)
	(obj package2)
	(at package3 s4)
	(obj package3)
	(at package4 s10)
	(obj package4)
	(at package5 s5)
	(obj package5)
	(at package6 s18)
	(obj package6)
	(at package7 s7)
	(obj package7)
	(at package8 s17)
	(obj package8)
	(at package9 s9)
	(obj package9)
	(at package10 s2)
	(obj package10)
	(at package11 s15)
	(obj package11)
	(at package12 s5)
	(obj package12)
	(at package13 s8)
	(obj package13)
	(at package14 s5)
	(obj package14)
	(at package15 s9)
	(obj package15)
	(at package16 s19)
	(obj package16)
	(at package17 s12)
	(obj package17)
	(at package18 s16)
	(obj package18)
	(at package19 s11)
	(obj package19)
	(at package20 s9)
	(obj package20)
	(at package21 s4)
	(obj package21)
	(at package22 s18)
	(obj package22)
	(at package23 s2)
	(obj package23)
	(at package24 s6)
	(obj package24)
	(at package25 s1)
	(obj package25)
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
	(at driver1 s16)
	(at driver2 s13)
	(at driver4 s7)
	(at driver5 s5)
	(at truck1 s2)
	(at truck2 s11)
	(at truck3 s10)
	(at truck4 s3)
	(at truck5 s16)
	(at package1 s19)
	(at package2 s10)
	(at package3 s19)
	(at package4 s11)
	(at package5 s14)
	(at package6 s18)
	(at package7 s7)
	(at package8 s6)
	(at package9 s7)
	(at package10 s14)
	(at package11 s13)
	(at package12 s11)
	(at package13 s15)
	(at package14 s6)
	(at package15 s11)
	(at package16 s10)
	(at package17 s17)
	(at package18 s15)
	(at package19 s4)
	(at package20 s7)
	(at package21 s3)
	(at package22 s8)
	(at package23 s17)
	(at package24 s2)
	(at package25 s12)
	))


)
