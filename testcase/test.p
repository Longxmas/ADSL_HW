void main() {
    int index[3] = {1, 2, 3};
    parallel (int x) in index {
        printf("%d", x);
        ret << true;
        ret >> x;
    }
}
