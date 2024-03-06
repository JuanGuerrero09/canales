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

func (rc RectangularChannel) WettedPerimeter(Y float64) float64 {
	return rc.width + (2 * Y)
}

func (rc RectangularChannel) TopWidth() float64 {
	return rc.width
}

func (rc RectangularChannel) HydraulicDepth(Y float64) float64 {
	return Y
}

func (rc RectangularChannel) SectionFactor(Y float64) float64 {
	return rc.width * math.Pow(Y, 1.5)
}
