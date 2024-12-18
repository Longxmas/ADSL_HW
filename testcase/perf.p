/* 用并行和非并行的归并排序来测试性能 */

int arr_size = 1000000;
int arr[1000000];
int temp[1000000];

def void msort_normal(int s, int t)
{
    if (s == t)
        return;
    int mid = (s + t) / 2;

    msort_normal(s, mid);
    msort_normal(mid + 1, t);

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
}

def void msort_parallel(int s, int t)
{
    if (s == t)
        return;
    int mid = (s + t) / 2;

    if (t - s > 10000) {
        int begin[2] = {s, mid + 1};
        int end[2] = {mid, t};
        pipe bool ret[2];
        parallel (int x, int y, pipe bool r) in begin, end, ret {
            msort_parallel(x, y);
            r << true;
        }
        ret[0] >>; ret[1] >>;
    } else {
        msort_normal(s, mid);
        msort_normal(mid + 1, t);
    }
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
}

void main()
{
    int i;
    for (i = 0; i < arr_size; i = i + 1) {
        scanf("%d", arr[i]);
    }
    printf("normal msort:\n");
    msort_normal(0, arr_size - 1);
    for (i = 0; i < 10; i = i + 1)
        printf("%d ", arr[i]);
    printf("\n");

    for (i = 0; i < arr_size; i = i + 1) {
        scanf("%d", arr[i]);
    }
    printf("parallel msort:\n");
    msort_parallel(0, arr_size - 1);
    for (i = 0; i < 10; i = i + 1)
        printf("%d ", arr[i]);
}

/*
    normal msort:
    81.7834ms
    parallel msort:
    20.0138ms
*/