package main
import "fmt"
var a int = 4
var b float32 = 3.14
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
fmt.Printf("第一种for循环: for ;;;")
for i = 0; i < 10; i = i + 1 {
fmt.Printf("i:%d, ", i)
}
fmt.Printf("第二种for循环: for x in")
for _, i := range c {
fmt.Printf("i:%d, ", i)
}
var result int = sum(5, 8)
fmt.Printf("The sum is: %d", result)
var arr [2][3]int = [2][3]int{{1, 2, 3}, {4, 5, 6}}
fmt.Printf("The first element of arr is: ", arr[0][0])
for k = 0; k < 5; k = k + 1 {
fmt.Printf("arr[%d] = ", arr[k])
}
if a > 5 {
for i = 0; i < 3; i = i + 1 {
fmt.Printf("Nested loop, i = %d", i)
}
} else {
fmt.Printf("Outer condition failed.")
}
var sum2 int = a + b
var product float32 = a * b
fmt.Printf("Sum: %d, Product: %d", sum2, product)
}
