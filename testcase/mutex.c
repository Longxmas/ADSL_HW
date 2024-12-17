int value1 = 0;
int value2 = 0;

void main() {
    /* 演示线程同步与通信 */
    int index[3] = {1, 2, 3};   // 线程编号
    pipe int   p12;     // 线程1向线程2发送int
    pipe float p23;     // 线程2向线程3发送float
    pipe bool  p31;     // 线程3向线程1发送bool
    pipe bool  ret[3];  // 用于返回数据，同时阻塞主线程

    parallel (int x, pipe r) in index, ret {
        if (x == 1) {
            int send = 123;
            bool receive;
            p12 << send;
            printf("线程1发送int: %d", send)
            p32 >> receive;
            printf("线程1接收bool: %v", receive)
        } else {
            if (x == 2) {
                float send = 3.14;
                int receive;
                p23 << send;
                printf("线程2发送float: %f", send)
                p12 >> receive;
                printf("线程2接收int: %d", receive)
            } else {
                bool send = true;
                float receive;
                p31 << send;
                printf("线程3发送bool: %v", send)
                p23 >> receive;
                printf("线程3接收float: %f", receive)
            }
        }
    }


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