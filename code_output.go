package main
import ("fmt"; "sync")
var m1 sync.Mutex
var value1 int = 0
var value2 int = 0
func main() {
var index [3]int = [3]int{1, 2, 3}
var ret [3]chan bool
for _i := 0; _i < 3; _i++ { ret[_i] = make(chan bool) }
var i int
var p12 chan int = make(chan int)
var p23 chan float32 = make(chan float32)
var p31 chan bool = make(chan bool)
for _i := 0; _i < len(index); _i++ { go parallel_0(index[_i], ret[_i]) }
for _, i := range index {
<- ret[i - 1]
}
for _i := 0; _i < len(ret); _i++ { go parallel_1(ret[_i]) }
for _, i := range index {
<- ret[i - 1]
}
fmt.Printf("value1: %d\n", value1)
fmt.Printf("value2: %d\n", value2)
}
func parallel_0 (x int, r chan bool) {
if x == 1 {
var send int = 123
var receive bool
p12 <- send
fmt.Printf("线程1发送int: %d\n", send)
receive = <- p32
fmt.Printf("线程1接收bool: %v\n", receive)
} else {
if x == 2 {
var send float32 = 3.14
var receive int
p23 <- send
fmt.Printf("线程2发送float: %f\n", send)
receive = <- p12
fmt.Printf("线程2接收int: %d\n", receive)
} else {
var send bool = true
var receive float32
p31 <- send
fmt.Printf("线程3发送bool: %v\n", send)
receive = <- p23
fmt.Printf("线程3接收float: %f\n", receive)
}
}
r <- true
}
func parallel_1 (r chan int) {
var i int
for i = 0; i < 10000; i = i + 1 {
value1 = value1 + 1
m1.Lock()
value2 = value2 + 1
m1.Unlock()
}
r <- true
}
