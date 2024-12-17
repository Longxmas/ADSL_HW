int value1 = 0;
int value2 = 0;

pipe int   p12;     // 线程1向线程2发送int
pipe float p23;     // 线程2向线程3发送float
pipe bool  p31;     // 线程3向线程1发送bool

void main() {
    int index[3] = {1, 2, 3};   // 线程编号
    pipe bool ret[3];           // 用于返回数据，同时阻塞主线程
    int i;

    /************** 演示线程同步与通信 **************/
    parallel (int x, pipe bool r) in index, ret {
        if (x == 1) {
            int send = 123;
            bool receive;
            p31 >> receive;
            printf("线程1接收bool: %v\n", receive);
            p12 << send;
            printf("线程1发送int: %d\n", send);
        } else {
            if (x == 2) {
                float send = 3.14;
                int receive;
                p23 << send;
                printf("线程2发送float: %f\n", send);
                p12 >> receive;
                printf("线程2接收int: %d\n", receive);
            } else {
                bool send = true;
                float receive;
                p31 << send;
                printf("线程3发送bool: %v\n", send);
                p23 >> receive;
                printf("线程3接收float: %f\n", receive);
            }
        }
        r << true;
    }
    for i in index {
        ret[i - 1] >>;      // 主线程阻塞，等待子线程结束
    }

    /************** 演示共享变量互斥访问 **************/
    parallel (pipe bool r) in ret {
        int i;
        for (i = 0; i < 10000; i = i + 1) {
            value1 = value1 + 1;
            mutex m1 {      // 互斥访问代码块
                value2 = value2 + 1;
            }
        }
        r << true;
    }
    for i in index {
        ret[i - 1] >>;      // 主线程阻塞，等待子线程结束
    }
    printf("value1: %d\n", value1);     // value1访问没有互斥，因此小于30000
    printf("value2: %d\n", value2);     // value2等于30000
}