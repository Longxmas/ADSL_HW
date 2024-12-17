package main
import "fmt"
var A [5][10]float32
var x [10]float32
var y [5]float32 = [5]float32{0.0, 0.0, 0.0, 0.0, 0.0}
func main() {
var index [5]int = [5]int{0, 1, 2, 3, 4}
var ret [5]chan bool
for _i := 0; _i < 5; _i++ { ret[_i] = make(chan bool) }
var i int
var j int
for i = 0; i < 5; i = i + 1 {
for j = 0; j < 10; j = j + 1 {
fmt.Scanf("%f", &A[i][j])
}
}
for i = 0; i < 5; i = i + 1 {
for j = 0; j < 10; j = j + 1 {
fmt.Printf("A[%d][%d] = %f, ", i, j, A[i][j])
}
fmt.Printf("\n")
}
for i = 0; i < 10; i = i + 1 {
fmt.Scanf("%f", &x[i])
}
for i = 0; i < 10; i = i + 1 {
fmt.Printf("x[%d] = %f, ", i, x[i])
}
fmt.Printf("\n")
for _i := 0; _i < len(index); _i++ { go parallel_1(index[_i], A[_i], ret[_i]) }
for _, i = range index {
<- ret[i]
}
for i = 0; i < 5; i = i + 1 {
fmt.Printf("y[%d] = %f, ", i, y[i])
}
fmt.Printf("\n")
}
func parallel_1 (i int, row [10]float32, r chan bool) {
var j int
var result float32 = 0
for j = 0; j < 10; j = j + 1 {
result = result + row[j] * x[j]
}
y[i] = result
r <- true
}
