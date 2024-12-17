void main() {
    int index[2] = {0, 1};   // 线程编号
    pipe bool ret[2];        // 用于返回数据，同时阻塞主线程
    int i;

    /* 演示线程同步与通信 */
    pipe float p12;     // 线程1向线程2发送float
    pipe float p21;     // 线程2向线程1发送float

    // 矩阵和向量定义
    float A[2][3] = {{1.0, 2.0, 3.0}, {4.0, 5.0, 6.0}};   // 2x3矩阵
    float x[3] = {1.0, 1.0, 1.0};                         // 3x1向量
    float b[2] = {1.0, 1.0};                              // 常数向量
    float y[2] = {0.0, 0.0};                              // 结果向量

    parallel (int x, int[3] row) in index, A {
        int c0 = row[0];
        int c1 = row[1];
        int c2 = row[2];
        y[x] = c1 * r[0] + c2 * r[1] + c3 * r[2];
    }

    // 等待所有线程完成
    for i in index {
        ret[i - 1] >>;      // 主线程阻塞，等待子线程结束
    }

    // 打印最终结果
    printf("Final result: y[0] = %f, y[1] = %f\n", y[0], y[1]);
}
