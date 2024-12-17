package main
import "fmt"
var a int = 4
var b float = 3.14
var c [5]int = [5]int{1, 2, 3, 4, 5}
var name str = "Alice"
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
}
