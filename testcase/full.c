// 变量声明和赋值
int a = 4;
int b = 5;
float d = 3.14;
int c[5] = {1,2,3,4,5};
str name = "Alice";

// 函数定义与调用
/* 注释的测试 */
def int sum(int x, int y) {
    return x + y;
}

void main() {
    // 控制流：条件判断
    if (a > 5) {
        printf("a is greater than 5");
    } else {
        if (a == 5) {
            printf("a is equal to 5");
        } else {
            printf("a is less than 5");
        }
    }

    // 循环：for 循环
    int i = 0;
    printf("第一种for循环: for ;;;");
    for (i = 0; i < 10; i = i + 1) {
        printf("i:%d, ", i);
    }


    printf("第二种for循环: for x in");
    for i in c {
        printf("i:%d, ", i);
    }

    int result = sum(5, 8);
    printf("The sum is: %d", result);

    // 数组和访问
    int arr[2][3] = {{1, 2, 3}, {4, 5, 6}};
    printf("The first element of arr is: %d", arr[0][0]);

    // 数组遍历
    int k = 0;
    for (k = 0; k < 5; k = k + 1) {
        printf("arr[%d] = ", arr[k]);
    }

    // 嵌套控制流
    if (a > 5) {
        for (i = 0; i < 3; i = i + 1) {
            printf("Nested loop, i = %d", i);
        }
    } else {
        printf("Outer condition failed.");
    }

    // 运算符使用
    int sum2 = a + b;
    int product = a * b;
    printf("Sum: %d, Product: %d", sum2, product);
}