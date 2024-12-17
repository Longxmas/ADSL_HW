package main
import "fmt"
func add(x int, y int) int {
if x == y {
return x * 2
} else {
return x + y
}
}
func main() {
var a [3]int = [3]int{1, 2, 3}
var b [3]int = [3]int{4, 5, 6}
var c [3]chan int
for _i := 0; _i < 3; _i++ { c[_i] = make(chan int) }
for _i := 0; _i < len(a); _i++ { go parallel_0(a[_i], b[_i], c[_i]) }
var i int
for i = 0; i < 3; i = i + 1 {
var t int
t = <- c[i]
fmt.Printf("%d\n", t)
}
}
func parallel_0 (x int, y int, z chan int) {
z <- add(x, y)
}