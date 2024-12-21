package main
import ("fmt"; "time")
var arr_size int = 1000000
var arr [1000000]int
var temp [1000000]int
func msort_normal(s int, t int) {
if s == t {
return
}
var mid int = (s + t) / 2
msort_normal(s, mid)
msort_normal(mid + 1, t)
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
func msort_parallel(s int, t int) {
if s == t {
return
}
var mid int = (s + t) / 2
if t - s > 100000 {
var begin [2]int = [2]int{s, mid + 1}
var end [2]int = [2]int{mid, t}
var ret [2]chan bool
for _i := 0; _i < 2; _i++ { ret[_i] = make(chan bool) }
for _i := 0; _i < len(begin); _i++ { go parallel_1(begin[_i], end[_i], ret[_i]) }
<- ret[0]
<- ret[1]
} else {
msort_normal(s, mid)
msort_normal(mid + 1, t)
}
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
func main() {
    var i int
    for i = 0; i < arr_size; i = i + 1 {
        fmt.Scanf("%d", &arr[i])
    }
    fmt.Printf("normal msort:\n")
    start_time := time.Now()
    msort_normal(0, arr_size - 1)
    run_time := time.Since(start_time)
    fmt.Printf("%v\n", run_time)
//     for i = 0; i < 10; i = i + 1 {
//         fmt.Printf("%d ", arr[i])
//     }
//     fmt.Printf("\n")

    for i = 0; i < arr_size; i = i + 1 {
        fmt.Scanf("%d", &arr[i])
    }
    fmt.Printf("parallel msort:\n")
    start_time = time.Now()
    msort_parallel(0, arr_size - 1)
    run_time = time.Since(start_time)
    fmt.Printf("%v\n", run_time)
//     for i = 0; i < 10; i = i + 1 {
//         fmt.Printf("%d ", arr[i])
//     }
}
func parallel_1 (x int, y int, r chan bool) {
msort_parallel(x, y)
r <- true
}

