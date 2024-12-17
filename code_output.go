package main
import "fmt"
var value1 int = 0
var value2 int = 0
func main() {
var index [2]int = [2]int{0, 1}
var ret [2]chan bool
for _i := 0; _i < 2; _i++ { ret[_i] = make(chan bool) }
var i int
var p12 chan float32 = make(chan float32)
var p21 chan float32 = make(chan float32)
var A [2][3]float32 = [2][3]float32{{1.0, 2.0, 3.0}, {4.0, 5.0, 6.0}}
var x [3]float32 = [3]float32{1.0, 1.0, 1.0}
var b [2]float32 = [2]float32{1.0, 1.0}
var y [2]float32 = [2]float32{0.0, 0.0}
for _i := 0; _i < len(index); _i++ { go parallel_0(index[_i], A[_i]) }
for _, i = range index {
<- ret[i - 1]
}
fmt.Printf("Final result: y[0] = %f, y[1] = %f\n", y[0], y[1])
}
func parallel_0 (x int, row int) {}
