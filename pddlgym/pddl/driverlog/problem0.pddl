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

    ; action literals
    (load-truck truck1 package1)
    (load-truck truck1 package2)
    (load-truck truck2 package1)
    (load-truck truck2 package2)
    (unload-truck package1 truck1)
    (unload-truck package1 truck2)
    (unload-truck package2 truck1)
    (unload-truck package2 truck2)
    (board-truck driver1 truck1)
    (board-truck driver1 truck2)
    (board-truck driver2 truck1)
    (board-truck driver2 truck2)
    (disembark-truck driver1 truck1)
    (disembark-truck driver1 truck2)
    (disembark-truck driver2 truck1)
    (disembark-truck driver2 truck2)
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
    )
	(:goal (and
	(at driver1 s1)
	(at truck1 s1)
	(at package1 s0)
	(at package2 s0)
	))


)
