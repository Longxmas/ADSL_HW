def int add(int x, int y) {
    if (x == y) {
        return x * 2;
    } else
        return x + y;
}
void main() {
    int a[3] = {1, 2, 3};
    int b[3] = {4, 5, 6};
    pipe int c[3];

parallel (int x, int y, pipe int z) in a, b, c {
    z << add(x, y);
}

    int i;
    for (i = 0; i < 3; i = i + 1) {
        int t;
        c[i] >> t;
        printf("%d\n", t);
    }
}