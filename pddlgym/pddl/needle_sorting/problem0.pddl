(define (problem NEEDLE_SORTING_3)
    (:domain NEEDLE_SORTING)
    (:objects
        red_needle_1
        green_needle_1
        blue_needle_1
        red_goal blue_goal green_goal
        resting_position
    )

    (:init
        (robot-at resting_position)
        (handempty)
        (needle red_needle_1)
        (needle green_needle_1)
        (needle blue_needle_1)
        (needle-at red_needle_1 red_needle_1)
        (needle-at green_needle_1 green_needle_1)
        (needle-at blue_needle_1 blue_needle_1)
    )
    (:goal (and
            (needle-at red_needle_1 red_goal)
            (needle-at green_needle_1 green_goal)
            (needle-at blue_needle_1 blue_goal)
        )
    )
)
