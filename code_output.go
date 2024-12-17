package main
import "fmt"
var arr_size int = 8
var arr [8]int = [8]int{5, 11, 9, 4, 12, 6, 7, 1}
var temp [8]int
func msort(s int, t int) {
if s == t {
return
}
var mid int = (s + t) / 2
var begin [2]int = [2]int{s, mid + 1}
var end [2]int = [2]int{mid, t}
var ret [2]chan bool
for _i := 0; _i < 2; _i++ { ret[_i] = make(chan bool) }
for _i := 0; _i < len(begin); _i++ { go parallel_1(begin[_i], end[_i], ret[_i]) }
<- ret[0]
<- ret[1]
var i int = s
var j int = mid + 1
var k int = s
for i = s; i <= mid && j <= t; {
if arr[i] <= arr[j] {
temp[k] = arr[i]
k = k + 1
i = i + 1
} else {
temp[k] = arr[j]
k = k + 1
j = j + 1
}
}
for ; i <= mid; i = i + 1 {
temp[k] = arr[i]
k = k + 1
}
for ; j <= t; j = j + 1 {
temp[k] = arr[j]
k = k + 1
}
for i = s; i <= t; i = i + 1 {
arr[i] = temp[i]
}
}
func printArray(arr [8]int, size int) {
var i int
for i = 0; i < size; i = i + 1 {
fmt.Printf("%d ", arr[i])
}
fmt.Printf("\n")
}
func main() {
fmt.Printf("排序前的数组: \n")
printArray(arr, arr_size)
msort(0, arr_size - 1)
fmt.Printf("排序后的数组: \n")
printArray(arr, arr_size)
}
func parallel_1 (x int, y int, r chan bool) {
msort(x, y)
r <- true
}
