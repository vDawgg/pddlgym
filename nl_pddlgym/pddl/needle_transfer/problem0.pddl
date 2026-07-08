(define (problem NEEDLE_TRANSFER_1)
  (:domain NEEDLE_TRANSFER)

  (:objects
    left_arm right_arm
    needle
    goal left-rest right-rest
    red_ring
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
    (last-ring red_ring)

    (goal-position goal)

    (robot-at left_arm left-rest)
    (robot-at right_arm right-rest)

    (needle-at needle needle)

    (current-ring red_ring)
    (sequence red_ring red_ring)

    ; action literals
    (move left_arm needle)
    (move left_arm goal)
    (move left_arm left-rest)
    (move left_arm right-rest)
    (move left_arm red_ring)
    (move right_arm needle)
    (move right_arm goal)
    (move right_arm left-rest)
    (move right_arm right-rest)
    (move right_arm red_ring)
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
