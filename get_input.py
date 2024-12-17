import numpy as np


# 自定义函数用于将数组元素四舍五入到指定位数的小数
def round_array(arr, decimal_places):
    return np.around(arr, decimals=decimal_places)


# 构造一个5 * 10的随机浮点矩阵
matrix_5x10 = np.random.rand(5, 10).astype(float)
# 构造一个1 * 10的随机浮点向量
vector_1x10 = np.random.rand(1, 10).astype(float)

# 将矩阵元素四舍五入到五位小数
rounded_matrix_5x10 = round_array(matrix_5x10, 6)
# 将向量元素四舍五入到五位小数
rounded_vector_1x10 = round_array(vector_1x10[0], 6)

# 进行矩阵向量乘法
result_vector = np.dot(rounded_matrix_5x10, rounded_vector_1x10.reshape(-1, 1)).flatten()
# 将结果向量元素四舍五入到五位小数
rounded_result_vector = round_array(result_vector, 6)

with open('gemv.txt', 'w') as f:
    # 先写入5 * 10的矩阵数据
    for row in rounded_matrix_5x10:
        row_str = " ".join(map(str, row))
        f.write(row_str + ' ')
    # 再写入1 * 10的向量数据
    vector_str = " ".join(map(str, rounded_vector_1x10))
    f.write(vector_str + "\n")
    # 写入矩阵向量乘法结果
    result_str = " ".join(map(str, rounded_result_vector))
    f.write(result_str + "\n")