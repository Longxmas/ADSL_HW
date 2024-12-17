// 矩阵和向量定义
float A[2][3] = {{1.0, 2.0, 3.0}, {4.0, 5.0, 6.0}};   // 2x3矩阵
float x[3] = {1.0, 1.0, 1.0};                         // 3x1向量
float b[2] = {1.0, 1.0};                              // 常数向量
float y[2] = {0.0, 0.0};                              // 结果向量

void main() {
    int index[2] = {0, 1};   // 线程编号
    pipe bool ret[2];        // 用于返回数据，同时阻塞主线程
    int i;

    parallel (int i, float row[3], pipe bool r) in index, A, ret {
        mutex m {
            y[i] = row[0] * x[0] + row[1] * x[1] + row[2] * x[2];
        }
        r << true;
    }

    // 等待所有线程完成
    for i in index {
        ret[i] >>;      // 主线程阻塞，等待子线程结束
    }

    // 打印最终结果
    printf("Final result: y[0] = %f, y[1] = %f\n", y[0], y[1]);
}
