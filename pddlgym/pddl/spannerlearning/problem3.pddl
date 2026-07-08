(define (problem 3) (:domain spanner) (:objects
     bob - man
 spanner1 spanner2 spanner3 - spanner
     nut1 nut2 - nut
     location1 location2 location3 - location
     shed gate - location
    ) (:init
    (at bob shed)
    (at spanner1 location3)
    (useable spanner1)
    (at spanner2 location3)
    (useable spanner2)
    (at spanner3 location3)
    (useable spanner3)
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
    (pickup_spanner spanner3)
    (tighten_nut nut1)
    (tighten_nut nut2)
    ) (:goal
  (and
   (tightened nut1)
   (tightened nut2)
)))
