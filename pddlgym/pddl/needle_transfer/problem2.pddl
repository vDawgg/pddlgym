(define (problem NEEDLE_TRANSFER_02)
  (:domain NEEDLE_TRANSFER)

  (:objects
        left_arm right_arm
        needle
        goal left-rest right-rest
        teal_ring
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
    (last-ring teal_ring)

    (goal-position goal)

    (robot-at left_arm left-rest)
    (robot-at right_arm right-rest)

    (needle-at needle needle)

    (current-ring teal_ring)
    (sequence teal_ring teal_ring)
  )

  (:goal
    (and
      (needle-at needle goal)
    )
  )
)
