(define (problem RING_AND_PEG_02)
    (:domain RING_AND_PEG)
    (:objects
        red_ring green_ring yellow_ring pink_ring
        red_peg green_peg blue_peg pink_peg yellow_peg start_position
    )
    (:init
        (ring red_ring) (ring green_ring) (ring yellow_ring) (ring pink_ring)
        (peg red_peg) (peg green_peg) (peg blue_peg) (peg pink_peg) (peg yellow_peg) (peg start_position)
        (onpeg red_ring red_peg) (onpeg green_ring yellow_peg) (onpeg yellow_ring blue_peg) (onpeg pink_ring green_peg)
        (pegempty pink_peg)
        (at start_position)
        (handempty)
    )
    (:goal (and (onpeg red_ring red_peg) (onpeg green_ring green_peg) (onpeg yellow_ring yellow_peg) (onpeg pink_ring pink_peg)))
)
