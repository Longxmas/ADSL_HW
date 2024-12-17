package main
import "fmt"
var a int = 4
var b int = 5
var d float32 = 3.14
var c [5]int = [5]int{1, 2, 3, 4, 5}
var name string = "Alice"
func sum(x int, y int) int {
return x + y
}
func main() {
if a > 5 {
fmt.Printf("a is greater than 5")
} else {
if a == 5 {
fmt.Printf("a is equal to 5")
} else {
fmt.Printf("a is less than 5")
}
}
var i int = 0
fmt.Printf("第一种for循环: for ;;;\n")
for i = 0; i < 10; i = i + 1 {
fmt.Printf("i:%d, ", i)
}
fmt.Printf("\n第二种for循环: for x in\n")
for _, i := range c {
fmt.Printf("i:%d, ", i)
}
var result int = sum(5, 8)
fmt.Printf("The sum is: %d\n", result)
var arr [2][3]float32 = [2][3]float32{{1.0, 2.5, 3.6}, {4.6, 5.7, 6.8}}
fmt.Printf("The first element of arr is: %f\n", arr[1][1])
var k int = 0
var j int = 0
for k = 0; k < 2; k = k + 1 {
for j = 0; j < 3; j = j + 1 {
fmt.Printf("arr[%d][%d] = %f, ", k, j, arr[k][j])
}
fmt.Printf("\n")
}
fmt.Printf("testing if for\n")
a = 10
if a > 5 {
for i = 0; i < 3; i = i + 1 {
fmt.Printf("Nested loop, i = %d, ", i)
}
fmt.Printf("\n")
} else {
fmt.Printf("Outer condition failed.\n")
}
var sum2 int = a + b
var product int = a * b
fmt.Printf("Sum: %d, Product: %d", sum2, product)
}
