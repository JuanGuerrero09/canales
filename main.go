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

// TODO: Add a Logger
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

func (rc *ChannelProperties) Depth() float64 {
	return rc.Yn
}

func (rc *ChannelProperties) Flow() float64 {
	return rc.Q
}

func CalculateDepth(rc Channel) float64 {
	y := rc.Depth()
	if y != 0 {
		return y
	}
	fmt.Println("Y here is ", y)

	Qi := rc.Flow()
	fmt.Println("Flow here is ", Qi)

	tolerance := 0.001

	// Define the function to be solved
	f := func(y float64) float64 {
		A := rc.Area(y)
		WP := rc.WettedPerimeter(y)     // Assuming this method exists
		HR := rc.HydraulicRadius(A, WP) // Assuming this method exists
		fmt.Println("Y in this iteration", y)
		fmt.Println(rc.CalculateFlow(A, HR) - Qi)
		return rc.CalculateFlow(A, HR) - Qi
	}

	// Bisection solver
	y, err := Bisection(f, 0.001, 100, tolerance)
	if err != nil {
		fmt.Println("Error:", err)
		panic(err)
	}
	fmt.Println(y)

	yfinal := roundFloat(y, 2)

	return yfinal
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
	return 2 * y * math.Sqrt(1+math.Pow(tc.slope, 2))
}

type TrapezoidalChannel struct {
	ChannelProperties
	slope float64
	width float64
}

func (tzc TrapezoidalChannel) Area(y float64) float64 {
	return (tzc.width * y) + (tzc.slope * math.Pow(y, 2))
}

func (tzc TrapezoidalChannel) WettedPerimeter(y float64) float64 {
	return tzc.width + (2 * y * math.Sqrt(1+math.Pow(tzc.slope, 2)))
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

	fmt.Println("For Rectangular")

	fmt.Printf(" Area is %f\n", A3)
	fmt.Printf(" WP is %f\n", WP3)
	fmt.Printf(" HR is %f\n", HR3)
	fmt.Printf(" Flow is %f\n", Q3)

	fmt.Printf("The final channel is %+v", channel3)
	// ExampleNewtonKrylov()
}
