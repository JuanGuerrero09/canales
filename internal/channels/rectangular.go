package channels

import "math"

type RectangularChannel struct {
	ChannelProperties
	width float64
}

func (rc RectangularChannel) Area(Y float64) float64 {
	if rc.Yn != 0 {
		return rc.Yn * rc.width 
	}
	return Y * rc.width
}

func (rc RectangularChannel) WettedPerimeter() float64 {
	return rc.width + (2 * rc.Yn)
}

func (rc RectangularChannel) TopWidth() float64 {
	return rc.width
}

func (rc RectangularChannel) HydraulicDepth() float64 {
	return rc.Yn
}

func (rc RectangularChannel) SectionFactor() float64 {
	return rc.width * math.Pow(rc.Yn, 1.5)
}
