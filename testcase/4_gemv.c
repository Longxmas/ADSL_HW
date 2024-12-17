// 矩阵和向量定义
float A[5][10];   // 5x10矩阵
float x[10];                         // 10x1向量
float y[5] = {0.0, 0.0, 0.0, 0.0, 0.0};                              // 结果向量

void main() {
    int index[5] = {0, 1, 2, 3, 4};   // 线程编号
    pipe bool ret[5];        // 用于返回数据，同时阻塞主线程
    int i, j;
    for (i = 0; i < 5; i = i + 1){
        for (j = 0; j < 10; j = j + 1) {
            scanf("%f", A[i][j]);
        }
    }

    for (i = 0; i < 5; i = i + 1){
        for (j = 0; j < 10; j = j + 1) {
            printf("A[%d][%d] = %f, ", i, j , A[i][j]);
        }
        printf("\n");
    }

    for (i = 0; i < 10; i = i + 1) {
        scanf("%f", x[i]);
    }

    for (i = 0; i < 10; i = i + 1) {
        printf("x[%d] = %f, ", i, x[i]);
    }
    printf("\n");

    // for (i = 0; i < 5; i = i + 1) {
    //     printf("y[%d] = %f, ", i, y[i]);
    // }
    // printf("\n");

    parallel (int i, float row[10], pipe bool r) in index, A, ret {
        int j;
        float result = 0;
        for (j = 0; j < 10; j = j + 1) {
            result = result + row[j] * x[j];
        }
        y[i] = result;
        r << true;
    }

    // 等待所有线程完成
    for i in index {
        ret[i] >>;      // 主线程阻塞，等待子线程结束
    }

    // 打印最终结果
    for (i = 0; i < 5; i = i + 1) {
        printf("y[%d] = %f, ", i, y[i]);
    }
    printf("\n");
}
