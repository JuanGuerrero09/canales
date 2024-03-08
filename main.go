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

func roundFloat(val float64, precision uint) float64 {
	ratio := math.Pow(10, float64(precision))
	return math.Round(val*ratio) / ratio
}

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


func (cp ChannelProperties) Flow(Area, HydraulicRadius float64) float64 {
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

func Bisection(f Function, a, b, tol float64) (float64, error) {
	if f(a)*f(b) > 0 {
		return 0, fmt.Errorf("root is not bracketed in [%g, %g]", a, b)
	}
	for math.Abs(b-a) > tol {
		c := (a + b) / 2
		if f(c) == 0 {
			return c, nil
		} else if f(a)*f(c) < 0 {
			b = c
		} else {
			a = c
		}
	}
	return (a + b) / 2, nil
}

type RectangularChannel struct {
	ChannelProperties
	width float64
}

func (rc *RectangularChannel) CalculateDepth() {
	if rc.Yn != 0 {
		return
	}

	Q := rc.Q
	tolerance := 0.001

	// Define the function to be solved
	f := func(y float64) float64 {
		A := rc.Area(y)
		WP := rc.WettedPerimeter(y)     // Assuming this method exists
		HR := rc.HydraulicRadius(A, WP) // Assuming this method exists
		return rc.Flow(A, HR) - Q
	}

	// Bisection solver
	y, err := Bisection(f, 0, rc.width*2, tolerance)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	fmt.Println(y)

	rc.Yn = roundFloat(y, 2)
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

func (tc TriangularChannel) Area(Y float64) float64 {
	if tc.Yn != 0 {
		Y = tc.Yn
	}
	return math.Pow(Y, 2) * tc.slope
}

func (tc TriangularChannel) WettedPerimeter(y float64) float64 {
	return 2 * y * math.Sqrt(1 + math.Pow(tc.slope, 2))
}

func (rc *TriangularChannel) CalculateDepth() {
	if rc.Yn != 0 {
		return
	}

	Q := rc.Q
	tolerance := 0.001

	// Define the function to be solved
	f := func(y float64) float64 {
		A := rc.Area(y)
		WP := rc.WettedPerimeter(y)     // Assuming this method exists
		HR := rc.HydraulicRadius(A, WP) // Assuming this method exists
		return rc.Flow(A, HR) - Q
	}

	// Bisection solver
	y, err := Bisection(f, 0, 2, tolerance)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	fmt.Println(y)

	rc.Yn = roundFloat(y, 2)
}



func main() {

	channel := RectangularChannel{
		width: 2,
		ChannelProperties: ChannelProperties{
			So: 0.005,
			N:  0.0013,
			Q:  166.038,
			Yn: 0,
		},
	}

	channel2 := TriangularChannel{
		ChannelProperties: ChannelProperties{
			So: 0.005,
			N:  0.0013,
			Q:  403.9506,
			Yn: 0,
		},
		slope: 2.0,
	}

	Y := 2.0

	A := channel.Area(Y)
	WP := channel.WettedPerimeter(Y)
	HR := channel.HydraulicRadius(A, WP)
	Q := channel.Flow(A, HR)

	fmt.Println("For Rectangular")
	channel.CalculateDepth()

	fmt.Printf(" Area is %f\n", A)
	fmt.Printf(" WP is %f\n", WP)
	fmt.Printf(" HR is %f\n", HR)
	fmt.Printf(" Flow is %f\n", Q)

	fmt.Printf(" Y is %f\n", channel.Yn)

	fmt.Printf("The final channel is %+v", channel)

	A2 := channel2.Area(Y)
	WP2 := channel2.WettedPerimeter(Y)
	HR2 := channel2.HydraulicRadius(A2, WP2)
	Q2 := channel2.Flow(A2, HR2)

	fmt.Println("For Rectangular")

	fmt.Printf(" Area is %f\n", A2)
	fmt.Printf(" WP is %f\n", WP2)
	fmt.Printf(" HR is %f\n", HR2)
	fmt.Printf(" Flow is %f\n", Q2)

	channel2.CalculateDepth()
	fmt.Printf(" Y is %f\n", channel2.Yn)

	fmt.Printf("The final channel is %+v", channel2)
	// ExampleNewtonKrylov()
}
