package main

import "fmt"

func main() {
    s := []int{7, 2, 8, -9, 4, 0}

    //var c [2][2]chan int = [2][2]chan int{{make(chan int, 1), make(chan int, 2)}, {make(chan int, 3), make(chan int, 4)}}
    var ach [2][2]chan int
    for _i := 0; _i < 2; _i++ { for _j := 0; _j < 2; _j++ { ach[_i][_j] = make(chan int) }}
    go sum(s[:len(s)/2], ach[0][0])
    go sum(s[len(s)/2:], ach[1][0])
    var x, y int
    x, y = <-ach[0][0], <-ach[1][0] // 从通道 c 中接收

    fmt.Println(x, y, x+y)
}

func sum(s []int, c chan int) {
    sum := 0
    for _, v := range s {
        sum += v
    }
    c <- sum // 把 sum 发送到通道 c
}