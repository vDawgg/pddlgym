; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem DLOG-3-2-5)
	(:domain driverlog)
	(:objects
	driver1
	driver2
	driver3
	truck1
	truck2
	package1
	package2
	package3
	package4
	package5
	s0
	s1
	s2
	)
	(:init
	(at driver1 s1)
	(driver driver1)
	(at driver2 s0)
	(driver driver2)
	(at driver3 s0)
	(driver driver3)
	(at truck1 s1)
	(empty truck1)
	(truck truck1)
	(at truck2 s1)
	(empty truck2)
	(truck truck2)
	(at package1 s0)
	(obj package1)
	(at package2 s0)
	(obj package2)
	(at package3 s2)
	(obj package3)
	(at package4 s2)
	(obj package4)
	(at package5 s1)
	(obj package5)
	(location s0)
	(location s1)
	(location s2)

    ; action literals
    (load-truck truck1 package1)
    (load-truck truck1 package2)
    (load-truck truck1 package3)
    (load-truck truck1 package4)
    (load-truck truck1 package5)
    (load-truck truck2 package1)
    (load-truck truck2 package2)
    (load-truck truck2 package3)
    (load-truck truck2 package4)
    (load-truck truck2 package5)
    (unload-truck package1 truck1)
    (unload-truck package1 truck2)
    (unload-truck package2 truck1)
    (unload-truck package2 truck2)
    (unload-truck package3 truck1)
    (unload-truck package3 truck2)
    (unload-truck package4 truck1)
    (unload-truck package4 truck2)
    (unload-truck package5 truck1)
    (unload-truck package5 truck2)
    (board-truck driver1 truck1)
    (board-truck driver1 truck2)
    (board-truck driver2 truck1)
    (board-truck driver2 truck2)
    (board-truck driver3 truck1)
    (board-truck driver3 truck2)
    (disembark-truck driver1 truck1)
    (disembark-truck driver1 truck2)
    (disembark-truck driver2 truck1)
    (disembark-truck driver2 truck2)
    (disembark-truck driver3 truck1)
    (disembark-truck driver3 truck2)
    (drive-truck truck1 s0)
    (drive-truck truck1 s1)
    (drive-truck truck1 s2)
    (drive-truck truck2 s0)
    (drive-truck truck2 s1)
    (drive-truck truck2 s2)
    (walk driver1 s0)
    (walk driver1 s1)
    (walk driver1 s2)
    (walk driver2 s0)
    (walk driver2 s1)
    (walk driver2 s2)
    (walk driver3 s0)
    (walk driver3 s1)
    (walk driver3 s2)
    )
	(:goal (and
	(at driver2 s2)
	(at truck1 s2)
	(at truck2 s2)
	(at package1 s1)
	(at package2 s1)
	(at package3 s1)
	(at package4 s0)
	(at package5 s1)
	))


)
