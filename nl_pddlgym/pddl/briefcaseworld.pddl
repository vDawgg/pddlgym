; Domain taken from https://github.com/AI-Planning/classical-domains

(define (domain briefcase)
(:requirements :typing :negative-preconditions :conditional-effects)
(:types portable location)
(:predicates (at ?y - portable ?x - location)
             (in ?x - portable)
             (is-at ?x - location)
	     (move ?x - location)
	     (take-out ?x - portable)
	     (put-in ?x - portable))

; (:actions move take-out put-in)

(:action move
  :parameters (?m - location ?l - location)
  :precondition (and
		(move ?l)
  		(is-at ?m))
  :effect (and (is-at ?l) (not (is-at ?m))
		    (forall (?x - portable) (when (in ?x)
		      (and (at ?x ?l) (not (at ?x ?m)))))))

  (:action take-out
      :parameters (?x - portable)
      :precondition (and
		(take-out ?x)
      		(in ?x))
      :effect (not (in ?x)))

  (:action put-in
      :parameters (?x - portable ?l - location)
      :precondition (and
		(put-in ?x)
      		(not (in ?x)) (at ?x ?l) (is-at ?l))
      :effect (in ?x)))
