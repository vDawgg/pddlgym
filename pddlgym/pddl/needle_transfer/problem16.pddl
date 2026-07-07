(define (problem NEEDLE_TRANSFER_16)
  (:domain NEEDLE_TRANSFER)

  (:objects
        left_arm right_arm
        needle
        goal left-rest right-rest
        red_ring green_ring blue_ring yellow_ring orange_ring purple_ring pink_ring cyan_ring magenta_ring teal_ring brown_ring gray_ring olive_ring maroon_ring navy_ring
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
    (ring teal_ring)
    (ring brown_ring)
    (ring gray_ring)
    (ring olive_ring)
    (ring maroon_ring)
    (ring navy_ring)
    (last-ring navy_ring)

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
    (sequence magenta_ring teal_ring)
    (sequence teal_ring brown_ring)
    (sequence brown_ring gray_ring)
    (sequence gray_ring olive_ring)
    (sequence olive_ring maroon_ring)
    (sequence maroon_ring navy_ring)
    (sequence navy_ring navy_ring)
  )

  (:goal
    (and
      (needle-at needle goal)
    )
  )
)
