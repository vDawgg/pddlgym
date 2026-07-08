(define (problem NEEDLE_TRANSFER_06)
  (:domain NEEDLE_TRANSFER)

  (:objects
        left_arm right_arm
        needle
        goal left-rest right-rest
        magenta_ring teal_ring brown_ring gray_ring olive_ring
  )

  (:init
    (robot left_arm)
    (robot right_arm)
    (initial-picker right_arm)

    (needle needle)

    (position goal)
    (position left-rest)
    (position right-rest)

    (ring magenta_ring)
    (ring teal_ring)
    (ring brown_ring)
    (ring gray_ring)
    (ring olive_ring)
    (last-ring olive_ring)

    (goal-position goal)

    (robot-at left_arm left-rest)
    (robot-at right_arm right-rest)

    (needle-at needle needle)

    (current-ring magenta_ring)
    (sequence magenta_ring teal_ring)
    (sequence teal_ring brown_ring)
    (sequence brown_ring gray_ring)
    (sequence gray_ring olive_ring)
    (sequence olive_ring olive_ring)

    ; action literals
    (move left_arm needle)
    (move left_arm goal)
    (move left_arm left-rest)
    (move left_arm right-rest)
    (move left_arm magenta_ring)
    (move left_arm teal_ring)
    (move left_arm brown_ring)
    (move left_arm gray_ring)
    (move left_arm olive_ring)
    (move right_arm needle)
    (move right_arm goal)
    (move right_arm left-rest)
    (move right_arm right-rest)
    (move right_arm magenta_ring)
    (move right_arm teal_ring)
    (move right_arm brown_ring)
    (move right_arm gray_ring)
    (move right_arm olive_ring)
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
