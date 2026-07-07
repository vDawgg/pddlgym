(define (problem NEEDLE_TRANSFER_10)
  (:domain NEEDLE_TRANSFER)

  (:objects
        left_arm right_arm
        needle
        goal left-rest right-rest
        red_ring green_ring blue_ring yellow_ring orange_ring purple_ring pink_ring cyan_ring magenta_ring
  )

  (:init
    (robot left_arm)
    (robot right_arm)
    (initial-picker right_arm)

    (needle needle)

    (position goal)
    (position left-rest)
    (position right-rest)

    (ring red_ring)
    (ring green_ring)
    (ring blue_ring)
    (ring yellow_ring)
    (ring orange_ring)
    (ring purple_ring)
    (ring pink_ring)
    (ring cyan_ring)
    (ring magenta_ring)
    (last-ring magenta_ring)

    (goal-position goal)

    (robot-at left_arm left-rest)
    (robot-at right_arm right-rest)

    (needle-at needle needle)

    (current-ring red_ring)
    (sequence red_ring green_ring)
    (sequence green_ring blue_ring)
    (sequence blue_ring yellow_ring)
    (sequence yellow_ring orange_ring)
    (sequence orange_ring purple_ring)
    (sequence purple_ring pink_ring)
    (sequence pink_ring cyan_ring)
    (sequence cyan_ring magenta_ring)
    (sequence magenta_ring magenta_ring)
  )

  (:goal
    (and
      (needle-at needle goal)
    )
  )
)
