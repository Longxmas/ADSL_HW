package main
import "fmt"
func main() {
    var a [2]int = [...]int{1, 2}
    var c chan int
    for i := range a {
        fmt.Printf("%d", a[i])
    }
    c <- 1
    <- c
}