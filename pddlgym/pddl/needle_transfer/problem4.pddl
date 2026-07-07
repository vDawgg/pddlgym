(define (problem NEEDLE_TRANSFER_04)
  (:domain NEEDLE_TRANSFER)

  (:objects
        left_arm right_arm
        needle
        goal left-rest right-rest
        purple_ring pink_ring cyan_ring
  )

  (:init
    (robot left_arm)
    (robot right_arm)
    (initial-picker right_arm)

    (needle needle)

    (position goal)
    (position left-rest)
    (position right-rest)

    (ring purple_ring)
    (ring pink_ring)
    (ring cyan_ring)
    (last-ring cyan_ring)

    (goal-position goal)

    (robot-at left_arm left-rest)
    (robot-at right_arm right-rest)

    (needle-at needle needle)

    (current-ring purple_ring)
    (sequence purple_ring pink_ring)
    (sequence pink_ring cyan_ring)
    (sequence cyan_ring cyan_ring)
  )

  (:goal
    (and
      (needle-at needle goal)
    )
  )
)
