"""
test_sorter.py - 排序算法库完整测试套件

测试内容：
1. 功能测试 - 验证所有算法的正确性
2. 性能测试 - 比较各算法在不同数据规模下的表现
3. 稳定性测试 - 验证稳定排序算法
4. 边界测试 - 空列表、单元素、重复元素等
5. 智能排序测试 - 验证自适应排序引擎
"""

import time
import random
import unittest
import statistics
from collections import Counter
from sorter import sort, sortlib


class TestSortingAlgorithms(unittest.TestCase):
    """测试所有排序算法的正确性"""
    
    def setUp(self):
        """准备测试数据"""
        # 基本测试用例
        self.test_cases = [
            [],  # 空列表
            [1],  # 单元素
            [1, 2, 3, 4, 5],  # 已排序
            [5, 4, 3, 2, 1],  # 逆序
            [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],  # 随机
            [1, 1, 1, 1, 1],  # 全部相同
            [1, 2, 3, 2, 1, 0, -1, -2],  # 包含负数
            [0, -1, -5, 3, 2, -10, 7],  # 随机负数
            [1.5, 2.3, 0.8, 3.2, 1.1, 2.7],  # 浮点数
            [1, 2, 3, 4, 5, 4, 3, 2, 1],  # 峰值
        ]
        
        # 大随机数组（用于性能测试）
        random.seed(42)
        self.large_random = [random.randint(-1000, 1000) for _ in range(1000)]
        
        # 几乎有序数组
        self.almost_sorted = list(range(1000))
        for _ in range(10):  # 交换10对
            i, j = random.sample(range(1000), 2)
            self.almost_sorted[i], self.almost_sorted[j] = self.almost_sorted[j], self.almost_sorted[i]
    
    def test_all_algorithms(self):
        """测试所有算法在所有测试用例上的正确性"""
        algorithms = [
            ('bubble', sortlib.bubble),
            ('selection', sortlib.selection),
            ('insertion', sortlib.insertion),
            ('cocktail', sortlib.cocktail),
            ('odd_even', sortlib.odd_even),
            ('gnome', sortlib.gnome),
            ('merge', sortlib.merge),
            ('quick', sortlib.quick),
            ('heap', sortlib.heap),
            ('shell', sortlib.shell),
            ('comb', sortlib.comb),
            ('intro', sortlib.intro),
            ('tim', sortlib.tim),
            ('counting', sortlib.counting),
            ('radix', sortlib.radix),
            ('bucket', sortlib.bucket),
            ('tree', sortlib.tree),
            ('pancake', sortlib.pancake),
            ('cycle', sortlib.cycle),
            ('patience', sortlib.patience),
            ('bitonic', sortlib.bitonic),
        ]
        
        for test_case in self.test_cases:
            # 跳过非整数测试用例（计数排序、基数排序要求整数）
            for name, algo in algorithms:
                if name in ['counting', 'radix']:
                    if not all(isinstance(x, int) for x in test_case):
                        continue
                
                try:
                    result = algo(test_case)
                    expected = sorted(test_case)
                    self.assertEqual(result, expected, 
                        f"{name} failed on {test_case}\nGot: {result}\nExpected: {expected}")
                except Exception as e:
                    self.fail(f"{name} raised {e} on {test_case}")
    
    def test_original_not_modified(self):
        """测试算法不修改原数组"""
        arr = [3, 1, 4, 1, 5, 9, 2]
        original = arr.copy()
        
        algorithms = [
            sortlib.bubble, sortlib.selection, sortlib.insertion,
            sortlib.merge, sortlib.quick, sortlib.heap,
            sortlib.shell, sortlib.comb, sortlib.intro,
            sortlib.tim, sortlib.bucket, sortlib.tree,
            sortlib.pancake, sortlib.cycle, sortlib.patience
        ]
        
        for algo in algorithms:
            _ = algo(arr)
            self.assertEqual(arr, original, f"{algo.__name__} modified original array")
    
    def test_stability(self):
        """测试稳定排序算法"""
        # 创建包含重复键的数据
        arr = [(3, 'a'), (1, 'b'), (3, 'c'), (2, 'd'), (1, 'e'), (3, 'f')]
        
        stable_algorithms = [
            ('bubble', sortlib.bubble),
            ('insertion', sortlib.insertion),
            ('cocktail', sortlib.cocktail),
            ('odd_even', sortlib.odd_even),
            ('gnome', sortlib.gnome),
            ('merge', sortlib.merge),
            ('counting', sortlib.counting),
            ('radix', sortlib.radix),
            ('bucket', sortlib.bucket),
            ('tree', sortlib.tree),
            ('patience', sortlib.patience),
            ('tim', sortlib.tim),
        ]
        
        # 将元组转为可排序的格式（使用数字键）
        num_arr = [(k, idx, v) for idx, (k, v) in enumerate(arr)]
        
        for name, algo in stable_algorithms:
            if name in ['counting', 'radix', 'bucket']:
                # 这些算法需要数值数据，跳过元组测试
                continue
            
            result = algo(num_arr)
            # 检查相同键的元素是否保持相对顺序
            key_order = {}
            for i, (key, orig_idx, val) in enumerate(result):
                if key not in key_order:
                    key_order[key] = []
                key_order[key].append(orig_idx)
            
            for key, indices in key_order.items():
                self.assertEqual(indices, sorted(indices), 
                    f"{name} is not stable for key {key}")
    
    def test_smart_sort(self):
        """测试智能排序"""
        test_cases = self.test_cases + [
            list(range(100, 0, -1)),  # 降序
            list(range(1000)),  # 大有序
            [random.randint(0, 100) for _ in range(100)],  # 小范围整数
            [random.random() for _ in range(100)],  # 浮点数
        ]
        
        for test_case in test_cases:
            result = sort(test_case)
            expected = sorted(test_case)
            self.assertEqual(result, expected, f"Smart sort failed on {test_case}")
            
            # 验证原数组未被修改
            # (这里我们不修改test_case本身，因为有些是range生成的)
    
    def test_smart_sort_performance_small(self):
        """测试智能排序在小数组上的表现"""
        # 各种小数组
        test_data = [
            [random.randint(0, 10) for _ in range(50)],
            [random.random() for _ in range(50)],
            list(range(50)) + [25, 25, 25],
            [random.randint(-100, 100) for _ in range(50)],
        ]
        
        for data in test_data:
            result = sort(data)
            self.assertEqual(result, sorted(data))
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 极大值
        arr = [10**9, -10**9, 0, 10**6, -10**6]
        self.assertEqual(sort(arr), sorted(arr))
        
        # 极大列表（但元素简单）
        arr = [0, 1] * 500
        self.assertEqual(sort(arr), sorted(arr))
        
        # 包含None（应该报错或处理）
        # 注：排序算法应该能处理可比较的类型
        arr = [3, None, 1, 2]  # Python中 None < 3
        try:
            result = sort(arr)
            self.assertEqual(result, sorted(arr))
        except TypeError:
            pass  # 某些算法可能不支持None
    
    def test_duplicate_elements(self):
        """测试重复元素"""
        arr = [5, 3, 5, 2, 5, 1, 5, 4, 5, 5]
        result = sort(arr)
        expected = sorted(arr)
        self.assertEqual(result, expected)
        
        # 高重复率
        arr = [42] * 100 + [random.randint(1, 100) for _ in range(50)]
        result = sort(arr)
        expected = sorted(arr)
        self.assertEqual(result, expected)


class TestAlgorithmScorer(unittest.TestCase):
    """测试算法评分系统"""
    
    def test_scorer_initialization(self):
        """测试评分器初始化"""
        from sorter import AlgorithmScorer
        scorer = AlgorithmScorer()
        self.assertIsNotNone(scorer.algorithms)
        self.assertGreater(len(scorer.algorithms), 20)
    
    def test_score_calculation(self):
        """测试评分计算"""
        from sorter import AlgorithmScorer, _analyze_segment
        
        scorer = AlgorithmScorer()
        
        # 测试小整数数组
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        analysis = _analyze_segment(arr)
        
        # 计数排序应该得分较低（更好）
        counting_score = scorer.score_algorithm('counting', analysis)
        bubble_score = scorer.score_algorithm('bubble', analysis)
        
        self.assertLess(counting_score, bubble_score, 
            "Counting sort should score better than bubble sort for small integers")
    
    def test_segment_analysis(self):
        """测试数据段分析"""
        from sorter import _analyze_segment
        
        # 测试整数数组
        arr = [1, 2, 3, 4, 5]
        analysis = _analyze_segment(arr)
        self.assertTrue(analysis['is_int'])
        self.assertTrue(analysis['is_sorted'])
        self.assertTrue(analysis['is_sorted_asc'])
        
        # 测试降序数组
        arr = [5, 4, 3, 2, 1]
        analysis = _analyze_segment(arr)
        self.assertTrue(analysis['is_sorted_desc'])
        
        # 测试浮点数组
        arr = [1.5, 2.3, 0.8]
        analysis = _analyze_segment(arr)
        self.assertTrue(analysis['is_float'])
        self.assertFalse(analysis['is_int'])
        
        # 测试小范围整数
        arr = [1, 2, 3, 1, 2, 3]
        analysis = _analyze_segment(arr)
        self.assertTrue(analysis['suitable_counting'])


class TestPerformance(unittest.TestCase):
    """性能测试 - 比较不同算法的运行时间"""
    
    def setUp(self):
        random.seed(42)
        self.sizes = [10, 100, 1000, 5000]
        self.test_data = {}
        
        for size in self.sizes:
            self.test_data[f'random_{size}'] = [random.randint(-1000, 1000) for _ in range(size)]
            self.test_data[f'sorted_{size}'] = list(range(size))
            self.test_data[f'reverse_{size}'] = list(range(size, 0, -1))
            self.test_data[f'almost_sorted_{size}'] = list(range(size))
            for _ in range(size // 100):
                i, j = random.sample(range(size), 2)
                self.test_data[f'almost_sorted_{size}'][i], self.test_data[f'almost_sorted_{size}'][j] = \
                    self.test_data[f'almost_sorted_{size}'][j], self.test_data[f'almost_sorted_{size}'][i]
    
    def test_performance_basic(self):
        """基本性能测试 - 只测试快速算法"""
        algorithms = [
            ('merge', sortlib.merge),
            ('quick', sortlib.quick),
            ('heap', sortlib.heap),
            ('shell', sortlib.shell),
            ('tim', sortlib.tim),
            ('smart', sort),
        ]
        
        results = {}
        for name, algo in algorithms:
            results[name] = {}
            for data_name, data in self.test_data.items():
                if len(data) > 1000 and name in ['bubble', 'selection', 'insertion']:
                    continue  # 跳过太慢的算法
                
                arr = data.copy()
                start = time.perf_counter()
                _ = algo(arr)
                elapsed = time.perf_counter() - start
                results[name][data_name] = elapsed
        
        # 简单打印性能结果
        print("\n" + "="*80)
        print("性能测试结果 (时间: 秒)")
        print("="*80)
        
        for algo_name, times in results.items():
            print(f"\n{algo_name.upper():>10}:")
            for data_name, t in times.items():
                print(f"  {data_name:>20}: {t:.6f}s")
    
    def test_smart_vs_timsort(self):
        """比较智能排序和Timsort"""
        test_cases = [
            ('random', [random.randint(-1000, 1000) for _ in range(1000)]),
            ('sorted', list(range(1000))),
            ('reverse', list(range(1000, 0, -1))),
            ('small_range', [random.randint(0, 10) for _ in range(1000)]),
            ('almost_sorted', list(range(1000))),
        ]
        
        # 添加一些交换
        for _ in range(20):
            i, j = random.sample(range(1000), 2)
            test_cases[4][1][i], test_cases[4][1][j] = test_cases[4][1][j], test_cases[4][1][i]
        
        print("\n" + "="*80)
        print("智能排序 vs Timsort 对比")
        print("="*80)
        
        for name, data in test_cases:
            # 智能排序
            arr1 = data.copy()
            start = time.perf_counter()
            _ = sort(arr1)
            smart_time = time.perf_counter() - start
            
            # Timsort
            arr2 = data.copy()
            start = time.perf_counter()
            _ = sorted(arr2)
            tim_time = time.perf_counter() - start
            
            ratio = smart_time / tim_time if tim_time > 0 else 0
            print(f"{name:>15}: Smart={smart_time:.6f}s, Tim={tim_time:.6f}s, Ratio={ratio:.2f}x")


class TestSpecialCases(unittest.TestCase):
    """特殊测试用例"""
    
    def test_large_range_integers(self):
        """测试大范围整数"""
        arr = [random.randint(-10**8, 10**8) for _ in range(100)]
        result = sort(arr)
        self.assertEqual(result, sorted(arr))
    
    def test_mixed_types(self):
        """测试混合类型（如果支持）"""
        # 注意：Python的混合类型排序可能不支持所有算法
        arr = [3, 1.5, 2, 0.5, 4]
        try:
            result = sort(arr)
            expected = sorted(arr)
            self.assertEqual(result, expected)
        except TypeError:
            pass  # 某些算法可能不支持混合类型
    
    def test_large_duplicate_rates(self):
        """测试高重复率"""
        # 90% 重复
        arr = [random.choice([1, 2, 3, 4, 5]) for _ in range(1000)]
        result = sort(arr)
        self.assertEqual(result, sorted(arr))
        
        # 只有两个值
        arr = [random.choice([0, 1]) for _ in range(1000)]
        result = sort(arr)
        self.assertEqual(result, sorted(arr))
    
    def test_pattern_detection(self):
        """测试模式检测"""
        from sorter import _detect_patterns
        
        # 升序段
        arr = [1, 2, 3, 4, 5, 3, 4, 5, 6, 7]
        segments = _detect_patterns(arr)
        self.assertGreater(len(segments), 1)
        
        # 降序段
        arr = [5, 4, 3, 2, 1, 8, 7, 6, 5, 4]
        segments = _detect_patterns(arr)
        self.assertGreater(len(segments), 1)
        
        # 全是随机
        arr = [random.randint(0, 100) for _ in range(50)]
        segments = _detect_patterns(arr)
        self.assertGreater(len(segments), 0)
    
    def test_stability_smart_sort(self):
        """测试智能排序的稳定性"""
        # 创建带索引的元组
        arr = [(3, 0), (1, 1), (3, 2), (2, 3), (1, 4), (3, 5)]
        
        # 智能排序应该保持稳定
        result = sort(arr)
        
        # 检查相同键的元素顺序
        keys = [item[0] for item in result]
        indices = [item[1] for item in result]
        
        # 对于相同的键，索引应该递增
        key_indices = {}
        for key, idx in zip(keys, indices):
            if key not in key_indices:
                key_indices[key] = []
            key_indices[key].append(idx)
        
        for key, idx_list in key_indices.items():
            self.assertEqual(idx_list, sorted(idx_list), 
                f"Smart sort is not stable for key {key}")


def run_all_tests():
    """运行所有测试"""
    print("="*80)
    print("排序算法库测试套件")
    print("="*80)
    
    # 运行单元测试
    print("\n1. 运行单元测试...")
    print("-"*80)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestSortingAlgorithms))
    suite.addTests(loader.loadTestsFromTestCase(TestAlgorithmScorer))
    suite.addTests(loader.loadTestsFromTestCase(TestSpecialCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    
    # 运行性能测试（可选）
    print("\n2. 运行性能测试...")
    print("-"*80)
    perf_test = TestPerformance()
    perf_test.setUp()
    perf_test.test_performance_basic()
    perf_test.test_smart_vs_timsort()


def quick_test():
    """快速验证测试"""
    print("快速验证测试")
    print("="*50)
    
    test_arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    print(f"原始: {test_arr}")
    print(f"排序: {sort(test_arr)}")
    
    # 测试特殊数据
    print("\n测试特殊数据:")
    print(f"空列表: {sort([])}")
    print(f"单元素: {sort([42])}")
    print(f"已排序: {sort([1,2,3,4,5])}")
    print(f"逆序: {sort([5,4,3,2,1])}")
    print(f"全部相同: {sort([7,7,7,7,7])}")
    print(f"浮点数: {sort([3.2, 1.1, 4.8, 2.3, 0.5])}")
    print(f"负数: {sort([-3, 5, -1, 0, 2, -5])}")
    
    # 测试大数组
    large = [random.randint(-100, 100) for _ in range(100)]
    result = sort(large)
    print(f"\n大数组排序: {len(large)} 个元素 -> {len(result)} 个元素")
    print(f"正确性: {'✓' if result == sorted(large) else '✗'}")
    
    # 测试稳定性
    print("\n稳定性测试:")
    arr = [(3, 'a'), (1, 'b'), (3, 'c'), (2, 'd'), (1, 'e')]
    result = sort(arr)
    print(f"原始: {arr}")
    print(f"排序: {result}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        quick_test()
    elif len(sys.argv) > 1 and sys.argv[1] == '--performance':
        print("运行性能测试...")
        perf_test = TestPerformance()
        perf_test.setUp()
        perf_test.test_performance_basic()
        perf_test.test_smart_vs_timsort()
    else:
        run_all_tests()