## P-lang——支持并行语句块的编程语言

### 运行

#### 使用已有的测试文件

执行命令：

```bash
$ python main.py <test_name>
```

`<test_name>`可选值有：

- `full`：除并行外的全覆盖测试；
- `parallel`：并行测试，包括线程同步、互斥、通信；
- `msort`：并行归并排序；
- `gemv`：并行矩阵向量测试。

#### 使用其他文件

在`/testcase`下创建`xxx.p`源文件，执行命令：

```bash
$ python main.py xxx.p
```

