; Domain taken from https://github.com/AI-Planning/classical-domains

; IPC5 Domain: Openstacks Propositional -- strips forced sequential version
; Author: Patrik Haslum
; The problem instances for this domain were taken from the problem
; collection of the 2005 Constraint Modelling Challenge, organized by
; Barbara Smith & Ian Gent (see http://www.dcs.st-and.ac.uk/~ipg/challenge/).

(define (domain openstacks-sequencedstrips)
  (:requirements :typing :disjunctive-preconditions :negative-preconditions)
  (:types order product count)
  (:predicates (includes ?o - order ?p - product)
	       (waiting ?o - order)
	       (started ?o - order)
	       (shipped ?o - order)
	       (made ?p - product)
	       (machine-available)
	       (machine-configured ?p - product)
	       (stacks-avail ?s - count)
	       (next-count ?s - count ?ns - count)
	       (setup-machine ?product - product)
	       (make-product ?product - product)
	       (start-order ?order - order)
	       (ship-order ?order - order)
	       (open-new-stack))

  ; (:actions setup-machine make-product start-order ship-order open-new-stack)

  (:action setup-machine
    :parameters (?p - product ?avail - count)
    :precondition (and
		       (setup-machine ?p)
    		       (machine-available)
		       (not (made ?p))
		       (stacks-avail ?avail))
    :effect (and (not (machine-available)) (machine-configured ?p)))

  (:action make-product
    :parameters (?p - product ?avail - count)
    :precondition (and
		       (make-product ?p)
    		       (machine-configured ?p)
		       (forall (?o - order)
			       (imply (includes ?o ?p) (started ?o)))
		       (stacks-avail ?avail))
    :effect (and (not (machine-configured ?p))
		 (machine-available)
		 (made ?p)))

  (:action start-order
    :parameters (?o - order ?avail - count ?new-avail - count)
    :precondition (and
		       (start-order ?o)
    		       (waiting ?o)
		       (stacks-avail ?avail)
		       (next-count ?new-avail ?avail))
    :effect (and (not (waiting ?o))
		 (started ?o)
		 (not (stacks-avail ?avail))
		 (stacks-avail ?new-avail))
    )

  (:action ship-order
    :parameters (?o - order ?avail - count ?new-avail - count)
    :precondition (and
		       (ship-order ?o)
    		       (started ?o)
		       (forall (?p - product)
			       (imply (includes ?o ?p) (made ?p)))
		       (stacks-avail ?avail)
		       (next-count ?avail ?new-avail))
    :effect (and (not (started ?o))
		 (shipped ?o)
		 (not (stacks-avail ?avail))
		 (stacks-avail ?new-avail))
    )

  (:action open-new-stack
    :parameters (?open - count ?new-open - count)
    :precondition (and (open-new-stack) (stacks-avail ?open)
		       (next-count ?open ?new-open))
    :effect (and (not (stacks-avail ?open))
		 (stacks-avail ?new-open))
    )

  )
