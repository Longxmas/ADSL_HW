int arr_size = 8;
int arr[8] = {5, 11, 9, 4, 12, 6, 7, 1};
int temp[8];

// 归并排序函数
def bool msort(int s, int t)
{
    if (s == t)
        return;
    int mid = (s + t) / 2;
    int begin[2] = {s, mid};
    int end[2] = {mid + 1, t};
    pipe bool ret[2];
    parallel (int x, int y, int r) in begin, end, ret {
        msort(x, y);
        r << true;
    }
    ret[0] >>; ret[1] >>;
    int i = s, j = mid + 1, k = s;
    for (i = s; i <= mid && j <= t; )
    {
        if (arr[i] <= arr[j])
        {
            temp[k] = arr[i];
            k = k + 1;
            i = i + 1;
        }
        else
        {
            temp[k] = arr[j];
            k = k + 1;
            j = j + 1;
        }
    }
    for (; i <= mid; i = i + 1)
    {
        temp[k] = arr[i];
        k = k + 1;
    }
    for (; j <= t; j = j + 1)
    {
        temp[k] = arr[j];
        k = k + 1;
    }
    for (i = s; i <= t; i = i + 1)
        arr[i] = temp[i];
    return true;
}

// 打印数组
def bool printArray(int arr[8], int size)
{
    int i;
    for (i = 0; i < size; i = i + 1)
        printf("%d ", arr[i]);
    printf("\n");
    return true;
}

void main()
{
    printf("排序前的数组: \n");
    printArray(arr, arr_size);

    msort(0, arr_size - 1); // 调用排序函数

    printf("排序后的数组: \n");
    printArray(arr, arr_size);
}
