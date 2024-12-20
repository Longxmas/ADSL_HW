void main() {
    int outer_index[3] = {1, 2, 3};   // 外层线程编号
    pipe bool ret[3];

    parallel (int x, pipe bool r) in outer_index, ret {
        int outer_index[3] = {x, x, x};     // 记录外层编号
        int inner_index[3] = {1, 2, 3};     // 内层线程编号
        pipe bool rett[3];

        parallel (int x, int y, pipe bool r) in outer_index, inner_index, rett {
            printf("我是子线程%d的子线程%d\n", x, y);
            r << true;
        }
        int i;
        for i in inner_index {
            rett[i - 1] >>;
        }
        r << true;
    }
    int i;
    for i in outer_index {
        ret[i - 1] >>;
    }
}