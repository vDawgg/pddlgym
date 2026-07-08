; Test domain exercising conditional (when) and universal (forall ... when)
; effects, including a multi-variable forall.
(define (domain test-conditional-domain)
  (:requirements :typing :conditional-effects :negative-preconditions)
  (:types block)
  (:predicates
    (is-blue ?x - block)
    (is-red ?x - block)
    (is-marked ?x - block)
    (flag)
    (act-conditional ?x - block)
    (act-universal)
    (act-multi-var))

  ; (:actions act-conditional act-universal act-multi-var)

  ; Simple conditional effect: the `when` fires only if (is-blue ?x) holds.
  ; The action also adds (is-marked ?x) unconditionally.
  (:action conditional
    :parameters (?x - block)
    :precondition (act-conditional ?x)
    :effect (and
              (when (is-blue ?x)
                (and (is-red ?x) (not (is-blue ?x))))
              (is-marked ?x)))

  ; Universal conditional effect over a single bound variable.
  (:action universal
    :parameters ()
    :precondition (and (act-universal) (flag))
    :effect (and
              (forall (?b - block)
                (when (is-blue ?b)
                  (and (is-red ?b) (not (is-blue ?b)))))
              (not (flag))))

  ; Multi-variable forall (exercises parser acceptance; behaviour is the same
  ; as the single-variable forall above because the second binding is unused).
  (:action multi_var
    :parameters ()
    :precondition (and (act-multi-var) (flag))
    :effect (and
              (forall (?b1 - block ?b2 - block)
                (when (is-blue ?b1)
                  (and (is-red ?b1) (not (is-blue ?b1)))))
              (not (flag))))
)
