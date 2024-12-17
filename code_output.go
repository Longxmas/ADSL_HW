package main
import "fmt"
func main() {
fmt.Printf("排序前的数组: \n")
printArray(arr, arr_size)
msort(0, arr_size - 1)
fmt.Printf("排序后的数组: \n")
printArray(arr, arr_size)
}
