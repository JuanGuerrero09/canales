package main

import (
	"fmt"
	"math"
)

func roundFloat(val float64, precision uint) float64 {
	ratio := math.Pow(10, float64(precision))
	return math.Round(val*ratio) / ratio
}

type Channel interface {
	Type() string
	Depth() float64
	Flow() float64
	Area(y float64) float64 // Y is normal depth
	CalculateFlow(Area, HydraulicRadius float64) float64
	// Discharge() float64
	WettedPerimeter(y float64) float64
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

func (cp ChannelProperties) CalculateFlow(Area, HydraulicRadius float64) float64 {
	Q := Area * math.Pow(HydraulicRadius, 2/3.0) * math.Pow(cp.So, 1/2.0) / cp.N
	return Q
}

func (cp ChannelProperties) Velocity(Area float64) float64 {
	return cp.Q * Area
}

func (cp ChannelProperties) HydraulicRadius(Area, WettedPerimeter float64) float64 {
	return Area / WettedPerimeter
}

type Function func(float64) float64

type config struct {
	f         Function
	a         float64
	b         float64
	tolerance float64
}
// TODO: Add a Logger
func Bisection(cfg config) (float64, error) {
	if cfg.f(cfg.a)*cfg.f(cfg.b) > 0 {
		return 0, fmt.Errorf("root is not bracketed in [%g, %g]", cfg.a, cfg.b)
	}
	for math.Abs(cfg.b-cfg.a) > cfg.tolerance {
		c := (cfg.a + cfg.b) / 2
		if cfg.f(c) == 0 {
			return c, nil
			} else if cfg.f(cfg.a)*cfg.f(c) < 0 {
				cfg.b = c
		} else {
			cfg.a = c
		}
	}
	return (cfg.a + cfg.b) / 2, nil
}

type RectangularChannel struct {
	ChannelProperties
	width float64
}

func (rc *ChannelProperties) Depth() float64 {
	return rc.Yn
}

func (rc *ChannelProperties) Flow() float64 {
	return rc.Q
}

func CalculateDepth(rc Channel) float64 {
	channelType := rc.Type()
	y := rc.Depth()
	if y != 0 {
		return y
	}
	fmt.Println("Y here is ", y)

	Qi := rc.Flow()
	fmt.Println("Flow here is ", Qi)

	// Define the function to be solved
	f := func(y float64) float64 {
		A := rc.Area(y)
		WP := rc.WettedPerimeter(y)     // Assuming this method exists
		HR := rc.HydraulicRadius(A, WP) // Assuming this method exists
		fmt.Println("Y in this iteration", y)
		dif := rc.CalculateFlow(A, HR) - Qi
		fmt.Println(dif)
		return dif
	}


	var cfg config

	// Bisection solver
	if channelType == "Circular" {
		cfg = config{
			f: f,
			a: 0.001,
			b: 2,
			tolerance: 0.001,
		}
		
	} else {
		cfg = config{
			f: f,
			a: 0.001,
			b: 100,
			tolerance: 0.001,
		}
	}
	y, err := Bisection(cfg)
	if err != nil {
		fmt.Println("Error:", err)
		panic(err)
	}

	yfinal := roundFloat(y, 2)

	return yfinal
}

func (rc RectangularChannel) Type() string {
	return "Rectangular"
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

type TriangularChannel struct {
	ChannelProperties
	slope float64
}

func (tc TriangularChannel) Type() string {
	return "Triangular"
}

func (tc TriangularChannel) Area(Y float64) float64 {
	if tc.Yn != 0 {
		Y = tc.Yn
	}
	return math.Pow(Y, 2) * tc.slope
}

func (tc TriangularChannel) WettedPerimeter(y float64) float64 {
	return 2 * y * math.Sqrt(1+math.Pow(tc.slope, 2))
}

type TrapezoidalChannel struct {
	ChannelProperties
	slope float64
	width float64
}

func (tzc TrapezoidalChannel) Type() string {
	return "Trapezoidal"
}

func (tzc TrapezoidalChannel) Area(y float64) float64 {
	return (tzc.width * y) + (tzc.slope * math.Pow(y, 2))
}

func (tzc TrapezoidalChannel) WettedPerimeter(y float64) float64 {
	return tzc.width + (2 * y * math.Sqrt(1+math.Pow(tzc.slope, 2)))
}

type CircularChannel struct {
	ChannelProperties
	Diameter float64
}

func (tzc CircularChannel) Type() string {
	return "Circular"
}

func (cc CircularChannel) MaxFlow() float64 {
	return (math.Pi / cc.N) * math.Pow(cc.Diameter/2.0, 5/3.0) * math.Pow(cc.So, 1/2.0)
}

func (cc CircularChannel) ContactAngle(y float64) float64 {
	return 2 * math.Acos(1-(2*y/cc.Diameter))
}

func (cc CircularChannel) Area(y float64) float64 {
	CA := cc.ContactAngle(y)
	return (math.Pow(cc.Diameter, 2) / 4) * (CA/2 - (math.Sin(CA/2) * math.Cos(CA/2)))
}

func (cc CircularChannel) WettedPerimeter(y float64) float64 {
	CA := cc.ContactAngle(y)
	return ((1 / 2.0) * cc.Diameter * CA)
}

func main() {

	channel := &RectangularChannel{
		width: 2,
		ChannelProperties: ChannelProperties{
			So: 0.005,
			N:  0.0013,
			Q:  166.038,
			Yn: 0,
		},
	}

	channel2 := &TriangularChannel{
		ChannelProperties: ChannelProperties{
			So: 0.005,
			N:  0.0013,
			Q:  403.9506,
			Yn: 0,
		},
		slope: 2.0,
	}

	channel3 := &TrapezoidalChannel{
		ChannelProperties: ChannelProperties{
			So: 0.005,
			N:  0.0013,
			Q:  400,
			Yn: 0,
		},
		slope: 2.0,
		width: 2.0,
	}

	channel4 := &CircularChannel{
		ChannelProperties: ChannelProperties{
			So: 0.005,
			N:  0.0013,
			Q:  100,
			Yn: 0,
		},
		Diameter: 2.0,
	}

	fmt.Println("For Rectangular")
	channel.Yn = CalculateDepth(channel)

	A := channel.Area(channel.Yn)
	WP := channel.WettedPerimeter(channel.Yn)
	HR := channel.HydraulicRadius(A, WP)
	Q := channel.CalculateFlow(A, HR)

	fmt.Printf(" Area is %f\n", A)
	fmt.Printf(" WP is %f\n", WP)
	fmt.Printf(" HR is %f\n", HR)
	fmt.Printf(" Flow is %f\n", Q)

	fmt.Printf(" Y is %f\n", channel.Yn)

	fmt.Printf("The final channel is %+v", channel)

	channel2.Yn = CalculateDepth(channel2)
	fmt.Printf(" Y is %f\n", channel2.Yn)
	A2 := channel2.Area(channel2.Yn)
	WP2 := channel2.WettedPerimeter(channel2.Yn)
	HR2 := channel2.HydraulicRadius(A2, WP2)
	Q2 := channel2.CalculateFlow(A2, HR2)

	fmt.Println("For Rectangular")

	fmt.Printf(" Area is %f\n", A2)
	fmt.Printf(" WP is %f\n", WP2)
	fmt.Printf(" HR is %f\n", HR2)
	fmt.Printf(" Flow is %f\n", Q2)

	fmt.Printf("The final channel is %+v", channel2)

	channel3.Yn = CalculateDepth(channel3)
	fmt.Printf(" Y is %f\n", channel3.Yn)
	A3 := channel3.Area(channel3.Yn)
	WP3 := channel3.WettedPerimeter(channel3.Yn)
	HR3 := channel3.HydraulicRadius(A3, WP3)
	Q3 := channel3.CalculateFlow(A3, HR3)

	fmt.Println("For Trapezoidal")

	fmt.Printf(" Area is %f\n", A3)
	fmt.Printf(" WP is %f\n", WP3)
	fmt.Printf(" HR is %f\n", HR3)
	fmt.Printf(" Flow is %f\n", Q3)

	fmt.Printf("The final channel is %+v", channel3)

	channel4.Yn = CalculateDepth(channel4)
	fmt.Printf(" Max flow is %f\n", channel4.MaxFlow())
	A4 := channel4.Area(channel4.Yn)
	WP4 := channel4.WettedPerimeter(channel4.Yn)
	HR4 := channel4.HydraulicRadius(A4, WP4)
	Q4 := channel4.CalculateFlow(A4, HR4)

	fmt.Println("For Trapezoidal")

	fmt.Printf(" Area is %f\n", A4)
	fmt.Printf(" WP is %f\n", WP4)
	fmt.Printf(" HR is %f\n", HR4)
	fmt.Printf(" Flow is %f\n", Q4)

	fmt.Printf("The final channel is %+v", channel4)
}
