package channels

type ChannelType string

const (
	Rectangular ChannelType = "rectangular"
	Triangular  ChannelType = "triangular"
)

type Channel interface {
	Area() float64
	Discharge() float64
	// HydraulicRadius() float64
	// Froude() float64
}

type ChannelProperties struct {
	So float64 // slope
	Q  float64 // Discharge
	Yn float64 //Critical Depth
	N  float64 //manning coef
}

type RectangularChannel struct {
	ChannelProperties
	height float64
	width  float64
}

func (rc RectangularChannel) Area() float64 {
	return 0.0
}

func (rc RectangularChannel) Discharge() float64 {
	return 0.0
}

func (rc RectangularChannel) Froude() float64 {
	return 0.0
}

func (rc RectangularChannel) HydraulicRadius() float64 {
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
}
