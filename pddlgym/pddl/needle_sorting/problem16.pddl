(define (problem NEEDLE_SORTING_16)
    (:domain NEEDLE_SORTING)
    (:objects
        blue_needle_1 blue_needle_2 blue_needle_3 yellow_needle_1 yellow_needle_2 yellow_needle_3 yellow_needle_4
        blue_goal yellow_goal
        resting_position
    )
    (:init
        (robot-at resting_position)
        (handempty)
        (needle blue_needle_1)
        (needle blue_needle_2)
        (needle blue_needle_3)
        (needle yellow_needle_1)
        (needle yellow_needle_2)
        (needle yellow_needle_3)
        (needle yellow_needle_4)
        (needle-at blue_needle_1 blue_needle_1)
        (needle-at blue_needle_2 blue_needle_2)
        (needle-at blue_needle_3 blue_needle_3)
        (needle-at yellow_needle_1 yellow_needle_1)
        (needle-at yellow_needle_2 yellow_needle_2)
        (needle-at yellow_needle_3 yellow_needle_3)
        (needle-at yellow_needle_4 yellow_needle_4)
    )
    (:goal         (and (needle-at blue_needle_1 blue_goal) (needle-at blue_needle_2 blue_goal) (needle-at blue_needle_3 blue_goal) (needle-at yellow_needle_1 yellow_goal) (needle-at yellow_needle_2 yellow_goal) (needle-at yellow_needle_3 yellow_goal) (needle-at yellow_needle_4 yellow_goal)))
)
