(define (problem NEEDLE_TRANSFER_1)
  (:domain NEEDLE_TRANSFER)

  (:objects
    left_arm right_arm
    needle
    goal left-rest right-rest
    green_ring red_ring blue_ring
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
    (last-ring blue_ring)

    (goal-position goal)

    (robot-at left_arm left-rest)
    (robot-at right_arm right-rest)

    (needle-at needle needle)

    (current-ring green_ring)
    (sequence green_ring red_ring)
    (sequence red_ring blue_ring)
    (sequence blue_ring blue_ring)
  )

  (:goal
    (and
      (needle-at needle goal)
    )
  )
)
