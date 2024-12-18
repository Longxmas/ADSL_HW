int value1 = 0;
void main() {
    int index[3] = {1, 2, 3};   // 线程编号
    pipe bool ret[3];           // 用于返回数据，同时阻塞主线程
    int i;

    /************** 演示共享变量互斥访问 **************/
    parallel (pipe bool r) in ret {
        int index[3] = {1, 2, 3};   // 线程编号
        pipe bool rett[3];           // 用于返回数据，同时阻塞主线程
        parallel (pipe bool r) in rett {
            value1 = value1 + 1;
            printf("a");
            r << true;
        }
        int i;
        for i in index {
            rett[i - 1] >>;      // 主线程阻塞，等待子线程结束
        }
        r << true;
    }
    for i in index {
        ret[i - 1] >>;      // 主线程阻塞，等待子线程结束
    }
    printf("value1: %d\n", value1);     // value1访问没有互斥，因此小于30000
}