; Problem for the conditional-effects test domain.
(define (problem conditional-test)
  (:domain test-conditional-domain)
  (:objects
    b1 - block
    b2 - block
    b3 - block
  )
  (:init
    (is-blue b1)
    (is-red b2)
    (is-blue b3)
    (act-conditional b1)
    (act-conditional b2)
    (act-conditional b3)
    (act-universal)
    (act-multi-var)
    (flag)
  )
  (:goal (and (is-red b1) (is-red b2) (is-red b3)))
)
