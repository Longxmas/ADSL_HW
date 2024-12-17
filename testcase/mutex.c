int value1 = 0;
int value2 = 0;

void main() {
    /* 演示线程同步与通信 */
    int index[3] = {1, 2, 3};   // 线程编号
    pipe int   p12;     // 线程1向线程2发送int
    pipe float p23;     // 线程2向线程3发送float
    pipe bool  p31;     // 线程3向线程1发送bool




    pipe int c[3];
parallel (int x, pipe int z) in arr, c {
    int i;
    for (i = 0; i < 10000; i = i + 1) {
        value1 = value1 + 1;
        mutex m1 {
            value2 = value2 + 1;
        }
    }
    z << 0;
}
    int i;
    for (i = 0; i < 3; i = i + 1) {
        c[i] >>;
    }
    printf("value1: %d\n", value1);
    printf("value2: %d\n", value2);
}