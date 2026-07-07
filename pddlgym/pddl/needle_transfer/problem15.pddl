(define (problem NEEDLE_TRANSFER_15)
  (:domain NEEDLE_TRANSFER)

  (:objects
        left_arm right_arm
        needle
        goal left-rest right-rest
        teal_ring brown_ring gray_ring olive_ring maroon_ring navy_ring lime_ring coral_ring gold_ring silver_ring indigo_ring red_ring green_ring blue_ring
  )

  (:init
    (robot left_arm)
    (robot right_arm)
    (initial-picker right_arm)

    (needle needle)

    (position goal)
    (position left-rest)
    (position right-rest)

    (ring teal_ring)
    (ring brown_ring)
    (ring gray_ring)
    (ring olive_ring)
    (ring maroon_ring)
    (ring navy_ring)
    (ring lime_ring)
    (ring coral_ring)
    (ring gold_ring)
    (ring silver_ring)
    (ring indigo_ring)
    (ring red_ring)
    (ring green_ring)
    (ring blue_ring)
    (last-ring blue_ring)

    (goal-position goal)

    (robot-at left_arm left-rest)
    (robot-at right_arm right-rest)

    (needle-at needle needle)

    (current-ring teal_ring)
    (sequence teal_ring brown_ring)
    (sequence brown_ring gray_ring)
    (sequence gray_ring olive_ring)
    (sequence olive_ring maroon_ring)
    (sequence maroon_ring navy_ring)
    (sequence navy_ring lime_ring)
    (sequence lime_ring coral_ring)
    (sequence coral_ring gold_ring)
    (sequence gold_ring silver_ring)
    (sequence silver_ring indigo_ring)
    (sequence indigo_ring red_ring)
    (sequence red_ring green_ring)
    (sequence green_ring blue_ring)
    (sequence blue_ring blue_ring)
  )

  (:goal
    (and
      (needle-at needle goal)
    )
  )
)
