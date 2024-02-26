package channels

type ChannelType string

const (
	Rectangular ChannelType = "rectangular"
	Triangular  ChannelType = "triangular"

	G float32 = 9.81
)

type Channel interface {
	Area() float64
	// Discharge() float64
	WettedPerimeter() float64
	HydraulicRadius(Area, WettedPerimeter float64) float64
	// TopWidth() float64
	Velocity(Area float64) float64
}

type ChannelProperties struct {
	So float64 // slope
	Q  float64 // Discharge
	Yn float64 //Critical Depth
	N  float64 //manning coef
}

func (cp ChannelProperties) Velocity(Area float64) float64 {
	return cp.Q * Area
}

func (cp ChannelProperties) HydraulicRadius(Area, WettedPerimeter float64) float64 {
	return Area / WettedPerimeter
}

type RectangularChannel struct {
	ChannelProperties
	height float64
	width  float64
}

func (rc RectangularChannel) Area() float64 {
	return rc.height * rc.width
}

func (rc RectangularChannel) WettedPerimeter() float64 {
	return rc.width + (2 * rc.height)
}

// func (rc RectangularChannel) Discharge() float64 {
// 	return 0.0
// }

func (rc RectangularChannel) Froude() float64 {
	return 0.0
}

// CreateChannel creates a new hydraulic channel based on the specified type.
func CreateChannel(channelType ChannelType, params map[string]float64) Channel {
	switch channelType {
	case Rectangular:
		return RectangularChannel{width: params["width"], height: params["height"]}
	// case Triangular:
	// 	return TriangularChannel{Base: params["base"], Height: params["height"]}
	default:
		// Handle unsupported channel types
		return nil
	}
	return nil
}
