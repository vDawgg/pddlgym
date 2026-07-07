(define (problem NEEDLE_TRANSFER_13)
  (:domain NEEDLE_TRANSFER)

  (:objects
        left_arm right_arm
        needle
        goal left-rest right-rest
        cyan_ring magenta_ring teal_ring brown_ring gray_ring olive_ring maroon_ring navy_ring lime_ring coral_ring gold_ring silver_ring
  )

  (:init
    (robot left_arm)
    (robot right_arm)
    (initial-picker right_arm)

    (needle needle)

    (position goal)
    (position left-rest)
    (position right-rest)

    (ring cyan_ring)
    (ring magenta_ring)
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
    (last-ring silver_ring)

    (goal-position goal)

    (robot-at left_arm left-rest)
    (robot-at right_arm right-rest)

    (needle-at needle needle)

    (current-ring cyan_ring)
    (sequence cyan_ring magenta_ring)
    (sequence magenta_ring teal_ring)
    (sequence teal_ring brown_ring)
    (sequence brown_ring gray_ring)
    (sequence gray_ring olive_ring)
    (sequence olive_ring maroon_ring)
    (sequence maroon_ring navy_ring)
    (sequence navy_ring lime_ring)
    (sequence lime_ring coral_ring)
    (sequence coral_ring gold_ring)
    (sequence gold_ring silver_ring)
    (sequence silver_ring silver_ring)

    ; action literals
    (move left_arm needle)
    (move left_arm goal)
    (move left_arm left-rest)
    (move left_arm right-rest)
    (move left_arm cyan_ring)
    (move left_arm magenta_ring)
    (move left_arm teal_ring)
    (move left_arm brown_ring)
    (move left_arm gray_ring)
    (move left_arm olive_ring)
    (move left_arm maroon_ring)
    (move left_arm navy_ring)
    (move left_arm lime_ring)
    (move left_arm coral_ring)
    (move left_arm gold_ring)
    (move left_arm silver_ring)
    (move right_arm needle)
    (move right_arm goal)
    (move right_arm left-rest)
    (move right_arm right-rest)
    (move right_arm cyan_ring)
    (move right_arm magenta_ring)
    (move right_arm teal_ring)
    (move right_arm brown_ring)
    (move right_arm gray_ring)
    (move right_arm olive_ring)
    (move right_arm maroon_ring)
    (move right_arm navy_ring)
    (move right_arm lime_ring)
    (move right_arm coral_ring)
    (move right_arm gold_ring)
    (move right_arm silver_ring)
    (pick left_arm)
    (pick right_arm)
    (place left_arm)
    (place right_arm)
    )

  (:goal
    (and
      (needle-at needle goal)
    )
  )
)
