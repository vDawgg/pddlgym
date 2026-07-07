; Problem taken from https://github.com/AI-Planning/classical-domains

(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0
	instrument0
	image1
	spectrograph2
	thermograph0
	Star0
	GroundStation1
	GroundStation2
	Phenomenon3
	Phenomenon4
	Star5
	Phenomenon6
)
(:init
	(satellite satellite0)
	(instrument instrument0)
	(supports instrument0 thermograph0)
	(calibration_target instrument0 GroundStation2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Phenomenon6)
	(mode image1)
	(mode spectrograph2)
	(mode thermograph0)
	(direction Star0)
	(direction GroundStation1)
	(direction GroundStation2)
	(direction Phenomenon3)
	(direction Phenomenon4)
	(direction Star5)
	(direction Phenomenon6)

    ; action literals
    (turn_to satellite0 GroundStation1)
    (turn_to satellite0 GroundStation2)
    (turn_to satellite0 Phenomenon3)
    (turn_to satellite0 Phenomenon4)
    (turn_to satellite0 Phenomenon6)
    (turn_to satellite0 Star0)
    (turn_to satellite0 Star5)
    (switch_on instrument0)
    (switch_off instrument0)
    (calibrate instrument0 GroundStation1)
    (calibrate instrument0 GroundStation2)
    (calibrate instrument0 Phenomenon3)
    (calibrate instrument0 Phenomenon4)
    (calibrate instrument0 Phenomenon6)
    (calibrate instrument0 Star0)
    (calibrate instrument0 Star5)
    (take_image instrument0 GroundStation1 image1)
    (take_image instrument0 GroundStation1 spectrograph2)
    (take_image instrument0 GroundStation1 thermograph0)
    (take_image instrument0 GroundStation2 image1)
    (take_image instrument0 GroundStation2 spectrograph2)
    (take_image instrument0 GroundStation2 thermograph0)
    (take_image instrument0 Phenomenon3 image1)
    (take_image instrument0 Phenomenon3 spectrograph2)
    (take_image instrument0 Phenomenon3 thermograph0)
    (take_image instrument0 Phenomenon4 image1)
    (take_image instrument0 Phenomenon4 spectrograph2)
    (take_image instrument0 Phenomenon4 thermograph0)
    (take_image instrument0 Phenomenon6 image1)
    (take_image instrument0 Phenomenon6 spectrograph2)
    (take_image instrument0 Phenomenon6 thermograph0)
    (take_image instrument0 Star0 image1)
    (take_image instrument0 Star0 spectrograph2)
    (take_image instrument0 Star0 thermograph0)
    (take_image instrument0 Star5 image1)
    (take_image instrument0 Star5 spectrograph2)
    (take_image instrument0 Star5 thermograph0)
    )
(:goal (and
	(have_image Phenomenon4 thermograph0)
	(have_image Star5 thermograph0)
	(have_image Phenomenon6 thermograph0)
))

)
