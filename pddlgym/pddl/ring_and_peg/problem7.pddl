(define (problem RING_AND_PEG_07)
    (:domain RING_AND_PEG)
    (:objects
        red_ring green_ring blue_ring
        red_peg green_peg blue_peg pink_peg start_position
    )
    (:init
        (ring red_ring)
        (ring green_ring)
        (ring blue_ring)
        (peg red_peg)
        (peg green_peg)
        (peg blue_peg)
        (peg pink_peg)
        (peg start_position)
        (onpeg red_ring green_peg)
        (onpeg green_ring blue_peg)
        (onpeg blue_ring red_peg)
        (pegempty pink_peg)
        (at start_position)
        (handempty)
    )
    (:goal         (and (onpeg red_ring red_peg) (onpeg green_ring green_peg) (onpeg blue_ring blue_peg)))
)
