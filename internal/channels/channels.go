package channels

type ChannelType string

const (
	Rectangular ChannelType = "rectangular"
	Triangular  ChannelType = "triangular"

	G float32 = 9.81
)

type Channel interface {
	CalculateDepth(y float64) float64
	Area(y float64) float64 // Y is normal depth
	// Discharge() float64
	WettedPerimeter() float64
	HydraulicRadius(Area, WettedPerimeter float64) float64
	// TopWidth() float64
	Velocity(Area float64) float64
}

type ChannelProperties struct {
	So float64 // Slope
	Q  float64 // Discharge
	Yn float64 // Normal Depth
	N  float64 // Manning coef
}

func (cp ChannelProperties) CalculateDepth(initialDepth float64) float64 {
	var NormalDepth float64

	NormalDepth = 
}

func (cp ChannelProperties) Velocity(Area float64) float64 {
	return cp.Q * Area
}

func (cp ChannelProperties) HydraulicRadius(Area, WettedPerimeter float64) float64 {
	return Area / WettedPerimeter
}

func CalculateProperties(ch Channel) (Area, WettedPerimeter, HydraulicRadius, Velocity float64) {
	Y := ch.CalculateDepth()
	Area = ch.Area(Y)
	WettedPerimeter = ch.WettedPerimeter()
	HydraulicRadius = ch.HydraulicRadius(Area, WettedPerimeter)
	Velocity = ch.Velocity(Area)
	return Area, WettedPerimeter, HydraulicRadius, Velocity
}

// CreateChannel creates a new hydraulic channel based on the specified type.
func CreateChannel(channelType ChannelType, params map[string]float64) Channel {
	switch channelType {
	case Rectangular:
		return RectangularChannel{width: params["width"]}
	// case Triangular:
	// 	return TriangularChannel{Base: params["base"], Height: params["height"]}
	default:
		// Handle unsupported channel types
		return nil
	}
	return nil
}