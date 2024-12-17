// 变量声明和赋值
int a = 4;
int b = 5;
float d = 3.14;
bool x = false;
float c[3] = {1.2, 1.3, 1.4};
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
    printf("\n测试第一种for循环: for ;;;\n");
    for (i = 0; i < 10; i = i + 1) {
        printf("i:%d, ", i);
    }


    printf("\n测试第二种for循环: for x in\n");
    for i in c {
        printf("i:%f, ", i);
    }

    int result = sum(5, 8);
    printf("The sum is: %d\n", result);

    // 数组和访问
    float arr[2][3] = {{1.0, 2.5, 3.6}, {4.6, 5.7, 6.8}};
    printf("The first element of arr is: %f\n", arr[1][1]);

    // 数组遍历
    int k = 0;
    int j = 0;
    for (k = 0; k < 2; k = k + 1) {
        for (j = 0; j < 3; j = j + 1) {
            printf("arr[%d][%d] = %f, ", k, j, arr[k][j]);
        }
        printf("\n");
    }

    printf("testing if for\n");
    a = 10;
    // 嵌套控制流
    if (a > 5) {
        for (i = 0; i < 3; i = i + 1) {
            printf("Nested loop, i = %d, ", i);
        }
        printf("\n");
    } else {
        printf("Outer condition failed.\n");
    }

    // 运算符使用
    int sum2 = a + b;
    int product = a * b;
    printf("Sum: %d, Product: %d", sum2, product);
}