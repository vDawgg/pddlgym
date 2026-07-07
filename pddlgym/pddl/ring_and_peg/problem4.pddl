(define (problem RING_AND_PEG_04)
    (:domain RING_AND_PEG)
    (:objects
        green_ring yellow_ring blue_ring pink_ring
        red_peg green_peg blue_peg pink_peg yellow_peg start_position
    )
    (:init
        (ring pink_ring) (ring green_ring) (ring yellow_ring) (ring blue_ring)
        (peg red_peg) (peg green_peg) (peg blue_peg) (peg pink_peg) (peg yellow_peg) (peg start_position)
        (onpeg pink_ring yellow_peg) (onpeg green_ring blue_peg) (onpeg blue_ring pink_peg) (onpeg yellow_ring green_peg)
        (pegempty red_peg)
        (at start_position)
        (handempty)
    )
    (:goal (and (onpeg pink_ring pink_peg) (onpeg green_ring green_peg) (onpeg yellow_ring yellow_peg) (onpeg blue_ring blue_peg)))
)
