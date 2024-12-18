import os
import random

arr_size = 1000000
input_data = []
for i in range(arr_size):
    input_data.append(random.randint(0, 10000000))
input_str = " ".join(map(str, input_data)) + '\n' + " ".join(map(str, input_data)) + '\n'

print(input_str)

