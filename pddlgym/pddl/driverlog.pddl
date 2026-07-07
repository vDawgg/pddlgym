; Domain taken from https://github.com/AI-Planning/classical-domains
; Simplified driving and walking constraints to not require explicit links between locations

(define (domain driverlog)
  (:requirements :strips)
  (:predicates 	(obj ?obj)
	       	(truck ?truck)
               	(location ?loc)
		(driver ?d)
		(at ?obj ?loc)
		(in ?obj1 ?obj)
		(driving ?d ?v)
		(empty ?v)
		(load-truck ?truck ?obj)
		(unload-truck ?obj ?truck)
		(board-truck ?driver ?truck)
		(disembark-truck ?driver ?truck)
		(drive-truck ?truck ?to)
		(walk ?driver ?to)
)

; (:actions load-truck unload-truck board-truck disembark-truck drive-truck walk)

(:action load-truck
  :parameters
   (?obj
    ?truck
    ?loc)
  :precondition
   (and
   (load-truck ?truck ?obj)
   (obj ?obj) (truck ?truck) (location ?loc)
   (at ?truck ?loc) (at ?obj ?loc))
  :effect
   (and (not (at ?obj ?loc)) (in ?obj ?truck)))

(:action unload-truck
  :parameters
   (?obj
    ?truck
    ?loc)
  :precondition
   (and
	(unload-truck ?obj ?truck)
   	(obj ?obj) (truck ?truck) (location ?loc)
        (at ?truck ?loc) (in ?obj ?truck))
  :effect
   (and (not (in ?obj ?truck)) (at ?obj ?loc)))

(:action board-truck
  :parameters
   (?driver
    ?truck
    ?loc)
  :precondition
   (and
   (board-truck ?driver ?truck)
   (driver ?driver) (truck ?truck) (location ?loc)
   (at ?truck ?loc) (at ?driver ?loc) (empty ?truck))
  :effect
   (and (not (at ?driver ?loc)) (driving ?driver ?truck) (not (empty ?truck))))

(:action disembark-truck
  :parameters
   (?driver
    ?truck
    ?loc)
  :precondition
   (and
	(disembark-truck ?driver ?truck)
   	(driver ?driver) (truck ?truck) (location ?loc)
        (at ?truck ?loc) (driving ?driver ?truck))
  :effect
   (and (not (driving ?driver ?truck)) (at ?driver ?loc) (empty ?truck)))

(:action drive-truck
  :parameters
   (?truck
    ?loc-from
    ?loc-to
    ?driver)
  :precondition
   (and
   (drive-truck ?truck ?loc-to)
   (truck ?truck) (location ?loc-from) (location ?loc-to) (driver ?driver)
   (at ?truck ?loc-from)
   (driving ?driver ?truck))
  :effect
   (and (not (at ?truck ?loc-from)) (at ?truck ?loc-to)))

(:action walk
  :parameters
   (?driver
    ?loc-from
    ?loc-to)
  :precondition
   (and
	(walk ?driver ?loc-to)
   	(driver ?driver) (location ?loc-from) (location ?loc-to)
	(at ?driver ?loc-from))
  :effect
   (and (not (at ?driver ?loc-from)) (at ?driver ?loc-to)))


)
