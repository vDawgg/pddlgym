; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem DLOG-8-6-25)
	(:domain driverlog)
	(:objects
	driver1
	driver2
	driver3
	driver4
	driver5
	driver6
	driver7
	driver8
	truck1
	truck2
	truck3
	truck4
	truck5
	truck6
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
	(at driver1 s13)
	(driver driver1)
	(at driver2 s12)
	(driver driver2)
	(at driver3 s19)
	(driver driver3)
	(at driver4 s15)
	(driver driver4)
	(at driver5 s13)
	(driver driver5)
	(at driver6 s0)
	(driver driver6)
	(at driver7 s16)
	(driver driver7)
	(at driver8 s8)
	(driver driver8)
	(at truck1 s13)
	(empty truck1)
	(truck truck1)
	(at truck2 s8)
	(empty truck2)
	(truck truck2)
	(at truck3 s5)
	(empty truck3)
	(truck truck3)
	(at truck4 s17)
	(empty truck4)
	(truck truck4)
	(at truck5 s16)
	(empty truck5)
	(truck truck5)
	(at truck6 s16)
	(empty truck6)
	(truck truck6)
	(at package1 s18)
	(obj package1)
	(at package2 s15)
	(obj package2)
	(at package3 s8)
	(obj package3)
	(at package4 s2)
	(obj package4)
	(at package5 s8)
	(obj package5)
	(at package6 s9)
	(obj package6)
	(at package7 s15)
	(obj package7)
	(at package8 s15)
	(obj package8)
	(at package9 s1)
	(obj package9)
	(at package10 s3)
	(obj package10)
	(at package11 s1)
	(obj package11)
	(at package12 s6)
	(obj package12)
	(at package13 s16)
	(obj package13)
	(at package14 s14)
	(obj package14)
	(at package15 s11)
	(obj package15)
	(at package16 s17)
	(obj package16)
	(at package17 s14)
	(obj package17)
	(at package18 s18)
	(obj package18)
	(at package19 s0)
	(obj package19)
	(at package20 s0)
	(obj package20)
	(at package21 s12)
	(obj package21)
	(at package22 s11)
	(obj package22)
	(at package23 s17)
	(obj package23)
	(at package24 s6)
	(obj package24)
	(at package25 s8)
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
	(at driver1 s13)
	(at driver2 s6)
	(at driver3 s15)
	(at driver5 s6)
	(at driver6 s5)
	(at driver7 s8)
	(at truck3 s5)
	(at truck4 s18)
	(at truck6 s12)
	(at package1 s6)
	(at package2 s7)
	(at package3 s3)
	(at package4 s11)
	(at package5 s5)
	(at package6 s14)
	(at package7 s19)
	(at package8 s16)
	(at package9 s13)
	(at package10 s9)
	(at package11 s7)
	(at package12 s3)
	(at package13 s11)
	(at package14 s14)
	(at package15 s2)
	(at package16 s12)
	(at package18 s2)
	(at package19 s4)
	(at package20 s7)
	(at package21 s8)
	(at package22 s14)
	(at package23 s10)
	(at package24 s4)
	(at package25 s16)
	))


)
