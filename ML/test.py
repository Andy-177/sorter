# test_model.py
from sorter_ml import SorterML, FeatureExtractor, sortlib
import random
import time

# 加载模型
sorter = SorterML('sort_model_fixed.json', enable_learning=False)

# 测试各种数据
test_data = [
    ([random.randint(0, 1000) for _ in range(100)], "随机"),
    (list(range(100)), "已排序"),
    (list(range(100, 0, -1)), "降序"),
    ([random.randint(0, 10) for _ in range(100)], "小范围"),
]

for data, desc in test_data:
    start = time.time()
    result = sorter.sort(data.copy())
    elapsed = time.time() - start
    correct = result == sorted(data)
    print(f"{desc}: {'✅' if correct else '❌'} {elapsed:.4f}s")