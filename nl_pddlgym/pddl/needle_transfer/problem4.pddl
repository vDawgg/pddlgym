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

    ; action literals
    (move left_arm needle)
    (move left_arm goal)
    (move left_arm left-rest)
    (move left_arm right-rest)
    (move left_arm purple_ring)
    (move left_arm pink_ring)
    (move left_arm cyan_ring)
    (move right_arm needle)
    (move right_arm goal)
    (move right_arm left-rest)
    (move right_arm right-rest)
    (move right_arm purple_ring)
    (move right_arm pink_ring)
    (move right_arm cyan_ring)
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
