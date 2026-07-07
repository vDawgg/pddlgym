(define (problem NEEDLE_SORTING_04)
    (:domain NEEDLE_SORTING)
    (:objects
        red_needle_1 red_needle_2 green_needle_1 green_needle_2
        red_goal green_goal
        resting_position
    )
    (:init
        (robot-at resting_position)
        (handempty)
        (needle red_needle_1)
        (needle red_needle_2)
        (needle green_needle_1)
        (needle green_needle_2)
        (needle-at red_needle_1 red_needle_1)
        (needle-at red_needle_2 red_needle_2)
        (needle-at green_needle_1 green_needle_1)
        (needle-at green_needle_2 green_needle_2)
    )
    (:goal         (and (needle-at red_needle_1 red_goal) (needle-at red_needle_2 red_goal) (needle-at green_needle_1 green_goal) (needle-at green_needle_2 green_goal)))
)
