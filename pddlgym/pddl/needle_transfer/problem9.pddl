(define (problem NEEDLE_TRANSFER_09)
  (:domain NEEDLE_TRANSFER)

  (:objects
        left_arm right_arm
        needle
        goal left-rest right-rest
        orange_ring purple_ring pink_ring cyan_ring magenta_ring teal_ring brown_ring gray_ring
  )

  (:init
    (robot left_arm)
    (robot right_arm)
    (initial-picker right_arm)

    (needle needle)

    (position goal)
    (position left-rest)
    (position right-rest)

    (ring orange_ring)
    (ring purple_ring)
    (ring pink_ring)
    (ring cyan_ring)
    (ring magenta_ring)
    (ring teal_ring)
    (ring brown_ring)
    (ring gray_ring)
    (last-ring gray_ring)

    (goal-position goal)

    (robot-at left_arm left-rest)
    (robot-at right_arm right-rest)

    (needle-at needle needle)

    (current-ring orange_ring)
    (sequence orange_ring purple_ring)
    (sequence purple_ring pink_ring)
    (sequence pink_ring cyan_ring)
    (sequence cyan_ring magenta_ring)
    (sequence magenta_ring teal_ring)
    (sequence teal_ring brown_ring)
    (sequence brown_ring gray_ring)
    (sequence gray_ring gray_ring)
  )

  (:goal
    (and
      (needle-at needle goal)
    )
  )
)
