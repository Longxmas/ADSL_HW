package main
import ("fmt"; "sync")
var m1 sync.Mutex
var value1 int = 0
var value2 int = 0
func main() {
var arr [3]int = [3]int{1, 2, 3}
var c [3]chan int
for _i := 0; _i < 3; _i++ { c[_i] = make(chan int) }
for _i := 0; _i < len(arr); _i++ { go parallel_0(arr[_i], c[_i]) }
var i int
for i = 0; i < 3; i = i + 1 {
<- c[i]
}
fmt.Printf("value1: %d\n", value1)
fmt.Printf("value2: %d\n", value2)
}
func parallel_0 (x int, z chan int) {
var i int
for i = 0; i < 10000; i = i + 1 {
value1 = value1 + 1
m1.Lock()
value2 = value2 + 1
m1.Unlock()
}
z <- 0
}
