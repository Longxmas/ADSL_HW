int value1 = 0;
int value2 = 0;

void main() {
    int arr[3] = {1, 2, 3};
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