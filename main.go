package main

import (
	"fmt"
	"math"

	// "github.com/davidkleiven/gononlin/nonlin"
)

// func ExampleNewtonKrylov() {
// 	// This example shows how one can use NewtonKrylov to solve the
// 	// system of equations
// 	// (x-1)^2*(x - y) = 0
// 	// (x-2)^3*cos(2*x/y) = 0

// 	problem := nonlin.Problem{
// 		F: func(out, x []float64) {
// 			out[0] = math.Pow(Area(x[0])-1.0, 2.0) * (x[0] - x[1])
// 			out[1] = math.Pow(x[1]-2.0, 3.0) * math.Cos(2.0*x[0]/x[1])
// 		},
// 	}

// 	solver := nonlin.NewtonKrylov{
// 		// Maximum number of Newton iterations
// 		Maxiter: 1000,

// 		// Stepsize used to appriximate jacobian with finite differences
// 		StepSize: 1e-2,

// 		// Tolerance for the solution
// 		Tol: 1e-7,
// 	}

// 	x0 := []float64{0.0, 3.0}
// 	res := solver.Solve(problem, x0)
// 	fmt.Printf("Root: (x, y) = (%.2f, %.2f)\n", res.X[0], res.X[1])
// 	fmt.Printf("Function value: (%.2f, %.2f)\n", res.F[0], res.F[1])

// 	// Output:
// 	//
// 	// Root: (x, y) = (1.00, 2.00)
// 	// Function value: (-0.00, 0.00)
// }

type Channel interface {
	CalculateDepth() float64
	Area(y float64) float64 // Y is normal depth
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

func (cp ChannelProperties) CalculateDepth() float64 {
	var NormalDepth float64

	return NormalDepth
}

func (cp ChannelProperties) Flow(Area, HydraulicRadius float64, channelProperties ChannelProperties) float64 {
	Q := Area * math.Pow(HydraulicRadius, 2/3.0) * math.Pow(cp.So, 1/2.0) / cp.N
	return Q
}

func (cp ChannelProperties) Velocity(Area float64) float64 {
	return cp.Q * Area
}

func (cp ChannelProperties) HydraulicRadius(Area, WettedPerimeter float64) float64 {
	return Area / WettedPerimeter
}

func CalculateProperties(ch Channel) (Area, WettedPerimeter, HydraulicRadius, Velocity float64) {
	// Y := ch.CalculateDepth()
	Y := 2.0
	Area = ch.Area(Y)
	WettedPerimeter = ch.WettedPerimeter(Y)
	HydraulicRadius = ch.HydraulicRadius(Area, WettedPerimeter)
	Velocity = ch.Velocity(Area)
	return Area, WettedPerimeter, HydraulicRadius, Velocity
}

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


func (rc RectangularChannel) HydraulicDepth(Y float64) float64 {
	return Y
}

func (rc RectangularChannel) SectionFactor(Y float64) float64 {
	return rc.width * math.Pow(Y, 1.5)
}

type TriangularChannel struct {
	ChannelProperties
	width float64
}

func (rc TriangularChannel) Area(Y float64) float64 {
	if rc.Yn != 0 {
		return rc.Yn * rc.width
	}
	return Y * rc.width
}



func main() {

	channel := RectangularChannel{
		width: 2,
		ChannelProperties: ChannelProperties{
			So: 0.005,
			N:  0.0013,
			Q:  3.5,
		},
	}

	Y := 2.0

	A := channel.Area(Y)
	WP := channel.WettedPerimeter(Y)
	HR := channel.HydraulicRadius(A, WP)
	Q := channel.Flow(A, HR, channel.ChannelProperties)

	fmt.Printf(" Area is %f", A)
	fmt.Printf(" WP is %f", WP)
	fmt.Printf(" HR is %f", HR)
	fmt.Printf(" Flow is %f", Q)

	// ExampleNewtonKrylov()
}
