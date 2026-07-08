(define (problem 8) (:domain spanner) (:objects
     bob - man
 spanner1 spanner2 - spanner
     nut1 nut2 - nut
     location1 location2 location3 - location
     shed gate - location
    ) (:init
    (at bob shed)
    (at spanner1 location1)
    (useable spanner1)
    (at spanner2 location3)
    (useable spanner2)
    (loose nut1)
    (at nut1 gate)
    (loose nut2)
    (at nut2 gate)
    (link shed location1)
    (link location3 gate)
    (link location1 location2)
    (link location2 location3)

    ; action literals
    (walk location1)
    (walk location2)
    (walk location3)
    (walk shed)
    (walk gate)
    (pickup_spanner spanner1)
    (pickup_spanner spanner2)
    (tighten_nut nut1)
    (tighten_nut nut2)
    ) (:goal
  (and
   (tightened nut1)
   (tightened nut2)
)))
