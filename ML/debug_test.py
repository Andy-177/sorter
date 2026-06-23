# test_model_debug.py
from sorter_ml import SorterML, FeatureExtractor, sortlib
import random
import time
import sys

weight_file = 'sort_model_fixed.json'

# 猴子补丁：劫持 sort 方法打印决策
original_sort = SorterML.sort

def debug_sort(self, arr):
    # 提取特征
    features = FeatureExtractor.extract_features(arr)
    
    # 预测算法
    algo, score = self.learning_engine.predict_algorithm(features)
    print(f"  🤖 AI 决策: 算法={algo}, 得分={score:.2f}")
    
    # 调用原始排序
    return original_sort(self, arr)

SorterML.sort = debug_sort

# 加载模型
sorter = SorterML(weight_file, enable_learning=False)

# 测试各种数据（缩小到10万，方便快速测试）
test_data = [
    ([random.randint(0, 1000) for _ in range(100000)], "随机"),
    (list(range(100000)), "已排序"),
    (list(range(100000, 0, -1)), "降序"),
    ([random.randint(0, 10) for _ in range(100000)], "小范围"),
]

print("=" * 60)
print(f"开始测试 {weight_file}")
print("=" * 60)

for data, desc in test_data:
    print(f"\n📊 测试: {desc}")
    start = time.time()
    result = sorter.sort(data.copy())
    elapsed = time.time() - start
    correct = result == sorted(data)
    print(f"  ✅ {desc}: {elapsed:.4f}s {'✅' if correct else '❌'}")

print("\n" + "=" * 60)
print("测试完成")