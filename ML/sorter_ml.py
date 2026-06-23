"""
sorter_ml.py - 带机器学习的智能排序系统
包含22种排序算法 + 机器学习引擎 + 智能分段
"""

import statistics
import heapq
import math
import sys
import json
import os
from collections import defaultdict
from typing import List, Tuple, Dict, Any, Optional
import random
import time


# ==================== 排序算法库 ====================

class sortlib:
    """排序算法库 - 所有方法均为静态方法，返回新数组"""
    
    # ==================== 基础排序 O(n²) ====================
    
    @staticmethod
    def bubble(arr):
        """冒泡排序 - 稳定，O(n²)，O(1)"""
        arr = arr.copy()
        n = len(arr)
        for i in range(n - 1):
            swapped = False
            for j in range(n - 1 - i):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            if not swapped:
                break
        return arr
    
    @staticmethod
    def selection(arr):
        """选择排序 - 不稳定，O(n²)，O(1)"""
        arr = arr.copy()
        n = len(arr)
        for i in range(n - 1):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr
    
    @staticmethod
    def insertion(arr):
        """插入排序 - 稳定，O(n²)，O(1)"""
        arr = arr.copy()
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr
    
    @staticmethod
    def cocktail(arr):
        """鸡尾酒排序 - 稳定，O(n²)，O(1)"""
        arr = arr.copy()
        n = len(arr)
        start, end = 0, n - 1
        swapped = True
        while swapped:
            swapped = False
            for i in range(start, end):
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    swapped = True
            if not swapped:
                break
            end -= 1
            for i in range(end - 1, start - 1, -1):
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    swapped = True
            start += 1
        return arr
    
    @staticmethod
    def odd_even(arr):
        """奇偶排序 - 稳定，O(n²)，O(1)"""
        arr = arr.copy()
        n = len(arr)
        sorted_flag = False
        while not sorted_flag:
            sorted_flag = True
            for i in range(1, n - 1, 2):
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    sorted_flag = False
            for i in range(0, n - 1, 2):
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    sorted_flag = False
        return arr
    
    @staticmethod
    def gnome(arr):
        """侏儒排序 - 稳定，O(n²)，O(1)"""
        arr = arr.copy()
        i = 0
        while i < len(arr):
            if i == 0 or arr[i] >= arr[i - 1]:
                i += 1
            else:
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
                i -= 1
        return arr
    
    # ==================== 高级排序 O(n log n) ====================
    
    @staticmethod
    def merge(arr):
        """归并排序 - 稳定，O(n log n)，O(n)"""
        arr = arr.copy()
        def _merge_sort(arr):
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = _merge_sort(arr[:mid])
            right = _merge_sort(arr[mid:])
            return _merge(left, right)
        def _merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result
        return _merge_sort(arr)
    
    @staticmethod
    def quick(arr):
        """快速排序 - 不稳定，平均O(n log n)，最坏O(n²)，O(log n)"""
        arr = arr.copy()
        n = len(arr)
        if n <= 1:
            return arr
        
        sys.setrecursionlimit(max(1000000, n * 2 + 100))
        
        def _insertion_sort(arr, low, high):
            low = int(low)
            high = int(high)
            for i in range(low + 1, high + 1):
                key = arr[i]
                j = i - 1
                while j >= low and arr[j] > key:
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = key
        
        def _partition(arr, low, high):
            low = int(low)
            high = int(high)
            # 三数取中
            mid = (low + high) // 2
            if arr[mid] < arr[low]:
                arr[low], arr[mid] = arr[mid], arr[low]
            if arr[high] < arr[low]:
                arr[low], arr[high] = arr[high], arr[low]
            if arr[high] < arr[mid]:
                arr[mid], arr[high] = arr[high], arr[mid]
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1
        
        def _quick_sort(arr, low, high):
            low = int(low)
            high = int(high)
            if low < high:
                if high - low <= 16:
                    _insertion_sort(arr, low, high)
                    return
                pi = _partition(arr, low, high)
                _quick_sort(arr, low, pi - 1)
                _quick_sort(arr, pi + 1, high)
        
        try:
            _quick_sort(arr, 0, n - 1)
        except RecursionError:
            return sortlib.heap(arr)
        return arr
    
    @staticmethod
    def heap(arr):
        """堆排序 - 不稳定，O(n log n)，O(1)"""
        arr = arr.copy()
        def _heapify(arr, n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n and arr[left] > arr[largest]:
                largest = left
            if right < n and arr[right] > arr[largest]:
                largest = right
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                _heapify(arr, n, largest)
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            _heapify(arr, n, i)
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            _heapify(arr, i, 0)
        return arr
    
    @staticmethod
    def shell(arr):
        """希尔排序 - 不稳定，O(n log n)~O(n²)，O(1)"""
        arr = arr.copy()
        n = len(arr)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2
        return arr
    
    @staticmethod
    def comb(arr):
        """梳排序 - 不稳定，平均O(n log n)，O(1)"""
        arr = arr.copy()
        n = len(arr)
        gap = n
        shrink = 1.3
        sorted_flag = False
        while not sorted_flag:
            gap = int(gap / shrink)
            if gap <= 1:
                gap = 1
                sorted_flag = True
            for i in range(n - gap):
                if arr[i] > arr[i + gap]:
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    sorted_flag = False
        return arr
    
    @staticmethod
    def intro(arr):
        """内省排序 - 不稳定，O(n log n)，O(log n)"""
        arr = arr.copy()
        n = len(arr)
        if n <= 1:
            return arr
        
        max_depth = n.bit_length() * 2
        sys.setrecursionlimit(max(1000000, n * 2 + 100))
        
        def _insertion_sort(arr, low, high):
            low = int(low)
            high = int(high)
            for i in range(low + 1, high + 1):
                key = arr[i]
                j = i - 1
                while j >= low and arr[j] > key:
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = key
        
        def _partition(arr, low, high):
            low = int(low)
            high = int(high)
            mid = (low + high) // 2
            if arr[mid] < arr[low]:
                arr[low], arr[mid] = arr[mid], arr[low]
            if arr[high] < arr[low]:
                arr[low], arr[high] = arr[high], arr[low]
            if arr[high] < arr[mid]:
                arr[mid], arr[high] = arr[high], arr[mid]
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1
        
        def _intro_sort(arr, low, high, depth_limit):
            low = int(low)
            high = int(high)
            if low < high:
                if high - low <= 16:
                    _insertion_sort(arr, low, high)
                    return
                if depth_limit == 0:
                    sub_arr = arr[low:high+1]
                    sorted_sub = sortlib.heap(sub_arr)
                    arr[low:high+1] = sorted_sub
                    return
                pivot = _partition(arr, low, high)
                _intro_sort(arr, low, pivot - 1, depth_limit - 1)
                _intro_sort(arr, pivot + 1, high, depth_limit - 1)
        
        try:
            _intro_sort(arr, 0, n - 1, max_depth)
        except RecursionError:
            return sortlib.heap(arr)
        return arr
    
    @staticmethod
    def tim(arr):
        """Timsort - 稳定，O(n log n)，O(n)"""
        return sorted(arr)
    
    # ==================== 线性时间排序 O(n) ====================
    
    @staticmethod
    def counting(arr):
        """计数排序 - 稳定，O(n+k)，O(k)，仅适用于整数"""
        if not arr:
            return []
        arr = arr.copy()
        max_val = max(arr)
        min_val = min(arr)
        range_size = max_val - min_val + 1
        count = [0] * range_size
        output = [0] * len(arr)
        for num in arr:
            count[num - min_val] += 1
        for i in range(1, len(count)):
            count[i] += count[i - 1]
        for num in reversed(arr):
            idx = num - min_val
            count[idx] -= 1
            output[count[idx]] = num
        return output
    
    @staticmethod
    def radix(arr):
        """基数排序 - 稳定，O(d*(n+k))，O(n+k)，适用于整数（包括负数）"""
        if not arr:
            return []
        arr = arr.copy()
        negatives = [x for x in arr if x < 0]
        non_negatives = [x for x in arr if x >= 0]
        def _radix_sort_positive(arr):
            if not arr:
                return arr
            max_val = max(arr)
            exp = 1
            while max_val // exp > 0:
                arr = _counting_sort_digit(arr, exp)
                exp *= 10
            return arr
        def _counting_sort_digit(arr, exp):
            n = len(arr)
            output = [0] * n
            count = [0] * 10
            for num in arr:
                idx = (num // exp) % 10
                count[idx] += 1
            for i in range(1, 10):
                count[i] += count[i - 1]
            for i in range(n - 1, -1, -1):
                idx = (arr[i] // exp) % 10
                count[idx] -= 1
                output[count[idx]] = arr[i]
            return output
        if negatives:
            neg_abs = [-x for x in negatives]
            neg_sorted_abs = _radix_sort_positive(neg_abs)
            negatives_sorted = [-x for x in reversed(neg_sorted_abs)]
        else:
            negatives_sorted = []
        non_negatives_sorted = _radix_sort_positive(non_negatives)
        return negatives_sorted + non_negatives_sorted
    
    @staticmethod
    def bucket(arr, bucket_size=5):
        """桶排序 - 稳定，平均O(n+k)，O(n+k)"""
        if not arr:
            return []
        arr = arr.copy()
        min_val = min(arr)
        max_val = max(arr)
        if min_val == max_val:
            return arr
        bucket_count = int((max_val - min_val) // bucket_size + 1)
        buckets = [[] for _ in range(bucket_count)]
        for num in arr:
            idx = int((num - min_val) // bucket_size)
            buckets[idx].append(num)
        result = []
        for bucket in buckets:
            result.extend(sorted(bucket))
        return result
    
    # ==================== 树结构排序 ====================
    
    @staticmethod
    def tree(arr):
        """二叉排序树排序 - 稳定，平均O(n log n)，最坏O(n²)，O(n)"""
        arr = arr.copy()
        class TreeNode:
            def __init__(self, val):
                self.val = val
                self.left = None
                self.right = None
                self.count = 1
        def insert(root, val):
            if root is None:
                return TreeNode(val)
            if val < root.val:
                root.left = insert(root.left, val)
            elif val > root.val:
                root.right = insert(root.right, val)
            else:
                root.count += 1
            return root
        def inorder(root, result):
            if root is None:
                return
            inorder(root.left, result)
            for _ in range(root.count):
                result.append(root.val)
            inorder(root.right, result)
        root = None
        for val in arr:
            root = insert(root, val)
        result = []
        inorder(root, result)
        return result
    
    # ==================== 特殊用途排序 ====================
    
    @staticmethod
    def pancake(arr):
        """煎饼排序 - 不稳定，O(n²)，O(1)"""
        arr = arr.copy()
        n = len(arr)
        def _flip(arr, k):
            i = 0
            while i < k:
                arr[i], arr[k] = arr[k], arr[i]
                i += 1
                k -= 1
        for i in range(n - 1, 0, -1):
            max_idx = 0
            for j in range(1, i + 1):
                if arr[j] > arr[max_idx]:
                    max_idx = j
            if max_idx != i:
                if max_idx != 0:
                    _flip(arr, max_idx)
                _flip(arr, i)
        return arr
    
    @staticmethod
    def cycle(arr):
        """循环排序 - 不稳定，O(n²)，O(1)，写入次数最少"""
        arr = arr.copy()
        n = len(arr)
        for cycle_start in range(n - 1):
            item = arr[cycle_start]
            pos = cycle_start
            for i in range(cycle_start + 1, n):
                if arr[i] < item:
                    pos += 1
            if pos == cycle_start:
                continue
            while item == arr[pos]:
                pos += 1
            if pos != cycle_start:
                arr[pos], item = item, arr[pos]
            while pos != cycle_start:
                pos = cycle_start
                for i in range(cycle_start + 1, n):
                    if arr[i] < item:
                        pos += 1
                while item == arr[pos]:
                    pos += 1
                if item != arr[pos]:
                    arr[pos], item = item, arr[pos]
        return arr
    
    @staticmethod
    def patience(arr):
        """耐心排序 - 稳定，O(n log n)，O(n)"""
        arr = arr.copy()
        piles = []
        for num in arr:
            left, right = 0, len(piles)
            while left < right:
                mid = (left + right) // 2
                if piles[mid][-1] >= num:
                    right = mid
                else:
                    left = mid + 1
            if left == len(piles):
                piles.append([num])
            else:
                piles[left].append(num)
        result = []
        while piles:
            min_idx = 0
            min_val = piles[0][-1]
            for i in range(1, len(piles)):
                if piles[i] and piles[i][-1] < min_val:
                    min_val = piles[i][-1]
                    min_idx = i
            result.append(piles[min_idx].pop())
            if not piles[min_idx]:
                piles.pop(min_idx)
        return result
    
    @staticmethod
    def bitonic(arr, direction=1):
        """双调排序 - 不稳定，O(n log² n)，O(n)"""
        arr = arr.copy()
        def _bitonic_sort(arr, low, cnt, direction):
            if cnt > 1:
                k = cnt // 2
                _bitonic_sort(arr, low, k, 1)
                _bitonic_sort(arr, low + k, k, 0)
                _bitonic_merge(arr, low, cnt, direction)
        def _bitonic_merge(arr, low, cnt, direction):
            if cnt > 1:
                k = cnt // 2
                for i in range(low, low + k):
                    if (direction == 1 and arr[i] > arr[i + k]) or \
                       (direction == 0 and arr[i] < arr[i + k]):
                        arr[i], arr[i + k] = arr[i + k], arr[i]
                _bitonic_merge(arr, low, k, direction)
                _bitonic_merge(arr, low + k, k, direction)
        n = len(arr)
        power = 1
        while power < n:
            power <<= 1
        if n < power:
            arr.extend([float('inf')] * (power - n))
        _bitonic_sort(arr, 0, power, direction)
        return [x for x in arr[:n] if x != float('inf')]
    
    @staticmethod
    def external(arr, chunk_size=10):
        """外部排序(多路归并) - 稳定，O(n log n)，O(chunk_size)"""
        if len(arr) <= chunk_size:
            return sorted(arr)
        arr = arr.copy()
        chunks = []
        for i in range(0, len(arr), chunk_size):
            chunk = sorted(arr[i:i + chunk_size])
            chunks.append(chunk)
        result = []
        heap = []
        for i, chunk in enumerate(chunks):
            if chunk:
                heapq.heappush(heap, (chunk[0], i, 0))
        while heap:
            val, chunk_idx, elem_idx = heapq.heappop(heap)
            result.append(val)
            if elem_idx + 1 < len(chunks[chunk_idx]):
                next_val = chunks[chunk_idx][elem_idx + 1]
                heapq.heappush(heap, (next_val, chunk_idx, elem_idx + 1))
        return result


# ==================== 特征提取器 ====================

class FeatureExtractor:
    """提取数据的多维特征，用于机器学习"""
    
    # 模式类型编码
    PATTERN_ENCODING = {
        'random': 0,
        'ascending': 1,
        'descending': 2,
        'uniform': 3,
        'periodic': 4,
        'oscillating': 5,
        'monotonic_asc': 6,
        'monotonic_desc': 7,
        'mixed_trend': 8,
        'single': 9,
        'small_range': 10,
        'plateau': 11
    }
    
    @staticmethod
    def extract_features(arr: List) -> Dict[str, Any]:
        """提取完整的特征向量"""
        if not arr:
            return {'empty': True, 'size': 0}
        
        n = len(arr)
        features = {
            'size': float(n),
            'empty': False,
            'is_sorted_asc': True,
            'is_sorted_desc': True,
            'is_numeric': True,
            'is_int': True,
            'is_float': True,
        }
        
        # 基础类型检查
        for x in arr[:min(n, 100)]:
            if not isinstance(x, (int, float)):
                features['is_numeric'] = False
                features['is_int'] = False
                features['is_float'] = False
                break
            if not isinstance(x, int):
                features['is_int'] = False
        
        if not features['is_numeric']:
            return features
        
        # 数值特征
        sample = arr[:min(n, 5000)]
        min_val = min(sample)
        max_val = max(sample)
        range_size = max_val - min_val
        
        features['min'] = float(min_val)
        features['max'] = float(max_val)
        features['range'] = float(range_size)
        features['range_size'] = float(range_size + 1)
        
        # 排序状态检测
        if n > 1:
            features['is_sorted_asc'] = all(arr[i] <= arr[i+1] for i in range(min(n-1, 1000)))
            features['is_sorted_desc'] = all(arr[i] >= arr[i+1] for i in range(min(n-1, 1000)))
        else:
            features['is_sorted_asc'] = True
            features['is_sorted_desc'] = True
        
        # 逆序对密度
        inv_count = 0
        sample_size = min(n, 300)
        if sample_size > 1:
            temp = arr[:sample_size]
            inv_count = FeatureExtractor._count_inversions(temp)
        
        max_inv = sample_size * (sample_size - 1) // 2
        features['inv_density'] = inv_count / max_inv if max_inv > 0 else 0.0
        features['is_almost_sorted'] = features['inv_density'] < 0.08
        
        # 数据分布特征
        if n > 1 and range_size > 0:
            try:
                mean = statistics.mean(sample)
                stdev = statistics.stdev(sample) if len(sample) > 1 else 0.0
                features['mean'] = float(mean)
                features['stdev'] = float(stdev)
                features['uniform_score'] = float(stdev / range_size) if range_size > 0 else 0.0
                
                sorted_sample = sorted(sample)
                q1 = sorted_sample[len(sorted_sample)//4]
                q2 = sorted_sample[len(sorted_sample)//2]
                q3 = sorted_sample[3*len(sorted_sample)//4]
                features['q1'] = float(q1)
                features['q2'] = float(q2)
                features['q3'] = float(q3)
                features['iqr'] = float(q3 - q1)
                
                if stdev > 0:
                    skewness = sum((x - mean)**3 for x in sample) / (n * stdev**3)
                    features['skewness'] = float(skewness)
            except:
                pass
        
        # 重复率
        unique_count = len(set(sample))
        features['unique_rate'] = unique_count / len(sample) if len(sample) > 0 else 0.0
        features['duplicate_rate'] = 1.0 - features['unique_rate']
        
        # 模式检测
        features['has_trend'] = FeatureExtractor._detect_trend(arr[:min(n, 200)])
        pattern_type = FeatureExtractor._detect_pattern_type(arr[:min(n, 200)])
        features['pattern_type'] = pattern_type
        features['pattern_type_encoded'] = float(FeatureExtractor.PATTERN_ENCODING.get(
            pattern_type, 0
        ))
        
        # 算法适合度
        features['suitable_counting'] = (
            features['is_int'] and 
            features['range_size'] <= n * 2 and 
            features['range_size'] < 1000000
        )
        features['suitable_radix'] = (
            features['is_int'] and 
            features['range_size'] > n * 2 and 
            features['range_size'] < 10**9
        )
        features['suitable_bucket'] = (
            features['is_numeric'] and 
            features.get('uniform_score', 0) > 0.25 and 
            features.get('uniform_score', 0) < 0.55 and 
            n > 50
        )
        
        return features
    
    @staticmethod
    def _count_inversions(arr: List) -> int:
        """计算逆序对数量"""
        def merge_count(arr, temp, left, right):
            if left >= right:
                return 0
            mid = (left + right) // 2
            inv_count = merge_count(arr, temp, left, mid)
            inv_count += merge_count(arr, temp, mid + 1, right)
            inv_count += merge_and_count(arr, temp, left, mid, right)
            return inv_count
        
        def merge_and_count(arr, temp, left, mid, right):
            i = left
            j = mid + 1
            k = left
            inv_count = 0
            
            while i <= mid and j <= right:
                if arr[i] <= arr[j]:
                    temp[k] = arr[i]
                    i += 1
                else:
                    temp[k] = arr[j]
                    inv_count += (mid - i + 1)
                    j += 1
                k += 1
            
            while i <= mid:
                temp[k] = arr[i]
                i += 1
                k += 1
            
            while j <= right:
                temp[k] = arr[j]
                j += 1
                k += 1
            
            for i in range(left, right + 1):
                arr[i] = temp[i]
            
            return inv_count
        
        if len(arr) <= 1:
            return 0
        temp = [0] * len(arr)
        return merge_count(arr[:], temp, 0, len(arr) - 1)
    
    @staticmethod
    def _detect_trend(arr: List) -> int:
        """检测趋势：-1降序，0随机，1升序"""
        if len(arr) < 3:
            return 0
        
        up_count = 0
        down_count = 0
        for i in range(len(arr) - 1):
            if arr[i] < arr[i+1]:
                up_count += 1
            elif arr[i] > arr[i+1]:
                down_count += 1
        
        total = up_count + down_count
        if total == 0:
            return 0
        
        ratio = up_count / total
        if ratio > 0.7:
            return 1
        elif ratio < 0.3:
            return -1
        return 0
    
    @staticmethod
    def _detect_pattern_type(arr: List) -> str:
        """检测模式类型"""
        if len(arr) < 10:
            return 'random'
        
        trends = []
        window = min(10, len(arr) // 5)
        if window < 2:
            window = 2
        for i in range(0, len(arr) - window, window):
            trend = FeatureExtractor._detect_trend(arr[i:i+window])
            trends.append(trend)
        
        if not trends:
            return 'random'
        
        changes = sum(1 for i in range(1, len(trends)) if trends[i] != trends[i-1])
        
        if changes > len(trends) * 0.5:
            return 'oscillating'
        elif all(t == 1 for t in trends):
            return 'monotonic_asc'
        elif all(t == -1 for t in trends):
            return 'monotonic_desc'
        elif trends and any(t != 0 for t in trends):
            return 'mixed_trend'
        else:
            return 'random'


# ==================== 机器学习引擎 ====================

class LearningEngine:
    """在线学习引擎 - 使用权重向量和强化学习"""
    
    def __init__(self, model_file: str = None):
        self.algorithm_weights = defaultdict(lambda: defaultdict(float))
        self.segmentation_weights = defaultdict(lambda: defaultdict(float))
        self.learning_rate = 0.01
        self.discount_factor = 0.9
        self.episode_count = 0
        self.history = []
        self.model_file = model_file
        
        # 特征列表 - 只使用数值特征
        self.algorithm_features = [
            'size', 'inv_density', 'unique_rate', 'range_size',
            'is_sorted_asc', 'is_sorted_desc', 'is_almost_sorted',
            'suitable_counting', 'suitable_radix', 'suitable_bucket',
            'uniform_score', 'has_trend', 'pattern_type_encoded'
        ]
        
        self.segmentation_features = [
            'size', 'inv_density', 'unique_rate', 'range_size',
            'pattern_type_encoded', 'has_trend'
        ]
        
        if model_file and os.path.exists(model_file):
            self.load_model(model_file)
    
    def extract_feature_vector(self, features: Dict, feature_list: List) -> List[float]:
        """提取特征向量 - 只提取数值特征"""
        vec = []
        for f in feature_list:
            if f in features:
                val = features[f]
                if isinstance(val, bool):
                    val = 1.0 if val else 0.0
                elif isinstance(val, (int, float)):
                    val = float(val)
                elif isinstance(val, str):
                    val = float(FeatureExtractor.PATTERN_ENCODING.get(val, 0))
                else:
                    val = 0.0
                vec.append(val)
            else:
                vec.append(0.0)
        return vec
    
    def predict_algorithm(self, features: Dict) -> Tuple[str, float]:
        """预测最佳算法"""
        vec = self.extract_feature_vector(features, self.algorithm_features)
        
        best_algo = None
        best_score = float('-inf')
        
        for algo in dir(sortlib):
            if callable(getattr(sortlib, algo)) and not algo.startswith('_'):
                weight_vec = self.algorithm_weights[algo]
                score = sum(weight_vec.get(i, 0.0) * vec[i] for i in range(len(vec)))
                score += self._get_prior_score(algo, features)
                
                if score > best_score:
                    best_score = score
                    best_algo = algo
        
        if best_algo is None:
            best_algo = 'quick'
        
        return best_algo, best_score
    
    def _get_prior_score(self, algo: str, features: Dict) -> float:
        """基于专家知识的先验评分"""
        prior = 0.0
        n = features.get('size', 0)
        
        # 小数据优先简单算法
        if n < 20 and algo in ['insertion', 'bubble', 'selection']:
            prior += 10
        elif n < 50 and algo in ['insertion', 'cocktail']:
            prior += 5
        
        # 已排序数据
        if features.get('is_sorted_asc', False):
            if algo in ['insertion', 'bubble']:
                prior += 20
        
        # 大数据优先高级算法
        if n > 10000:
            if algo in ['quick', 'merge', 'heap', 'intro', 'tim']:
                prior += 15
            elif algo in ['bubble', 'selection', 'insertion']:
                prior -= 30
        
        # 特殊数据类型
        if features.get('suitable_counting', False) and algo == 'counting':
            prior += 25
        if features.get('suitable_radix', False) and algo == 'radix':
            prior += 20
        if features.get('suitable_bucket', False) and algo == 'bucket':
            prior += 15
        
        # 近乎有序
        if features.get('is_almost_sorted', False):
            if algo in ['insertion', 'bubble', 'cocktail']:
                prior += 15
        
        # 高重复率
        if features.get('duplicate_rate', 0) > 0.3:
            if algo in ['counting', 'insertion']:
                prior += 10
        
        return prior
    
    def predict_segmentation(self, features: Dict) -> Dict:
        """预测最优分段策略"""
        vec = self.extract_feature_vector(features, self.segmentation_features)
        
        strategies = {
            'monolithic': 0,
            'adaptive': 0,
            'pattern_based': 0,
            'aggressive': 0
        }
        
        for strategy in strategies:
            weight_vec = self.segmentation_weights[strategy]
            strategies[strategy] = sum(weight_vec.get(i, 0.0) * vec[i] for i in range(len(vec)))
        
        # 加入先验知识
        n = features.get('size', 0)
        if n < 500:
            strategies['monolithic'] += 20
        elif n > 10000 and features.get('pattern_type') in ['oscillating', 'mixed_trend']:
            strategies['pattern_based'] += 15
            strategies['aggressive'] += 10
        
        if features.get('is_almost_sorted', False):
            strategies['monolithic'] += 10
        
        best_strategy = max(strategies, key=strategies.get)
        return {
            'strategy': best_strategy,
            'scores': strategies
        }
    
    def update_weights(self, features: Dict, algorithm: str, reward: float, 
                       segmentation_strategy: str = None):
        """更新权重（在线学习）"""
        vec = self.extract_feature_vector(features, self.algorithm_features)
        weight_vec = self.algorithm_weights[algorithm]
        
        for i, val in enumerate(vec):
            if i not in weight_vec:
                weight_vec[i] = 0.0
            weight_vec[i] += self.learning_rate * reward * val
        
        if segmentation_strategy:
            seg_vec = self.extract_feature_vector(features, self.segmentation_features)
            seg_weight_vec = self.segmentation_weights[segmentation_strategy]
            
            for i, val in enumerate(seg_vec):
                if i not in seg_weight_vec:
                    seg_weight_vec[i] = 0.0
                seg_weight_vec[i] += self.learning_rate * reward * val * 0.5
        
        self.episode_count += 1
    
    def update_weights_with_performance(self, features: Dict, algorithm: str, 
                                       reward: float, performance_ratio: float,
                                       segmentation_strategy: str = None):
        """基于性能的权重更新"""
        vec = self.extract_feature_vector(features, self.algorithm_features)
        weight_vec = self.algorithm_weights[algorithm]
        
        # 根据性能比调整学习率
        effective_lr = self.learning_rate * (0.5 + 0.5 * min(performance_ratio, 2.0))
        
        for i, val in enumerate(vec):
            if i not in weight_vec:
                weight_vec[i] = 0.0
            weight_vec[i] += effective_lr * reward * val
        
        if segmentation_strategy:
            seg_vec = self.extract_feature_vector(features, self.segmentation_features)
            seg_weight_vec = self.segmentation_weights[segmentation_strategy]
            
            for i, val in enumerate(seg_vec):
                if i not in seg_weight_vec:
                    seg_weight_vec[i] = 0.0
                seg_weight_vec[i] += effective_lr * reward * val * 0.5
        
        self.episode_count += 1
    
    def save_model(self, filename: str):
        """保存模型"""
        model = {
            'algorithm_weights': {k: dict(v) for k, v in self.algorithm_weights.items()},
            'segmentation_weights': {k: dict(v) for k, v in self.segmentation_weights.items()},
            'learning_rate': self.learning_rate,
            'discount_factor': self.discount_factor,
            'episode_count': self.episode_count
        }
        with open(filename, 'w') as f:
            json.dump(model, f, indent=2)
    
    def load_model(self, filename: str):
        """加载模型"""
        try:
            with open(filename, 'r') as f:
                model = json.load(f)
            
            for algo, weights in model['algorithm_weights'].items():
                self.algorithm_weights[algo] = defaultdict(float, weights)
            
            for strategy, weights in model['segmentation_weights'].items():
                self.segmentation_weights[strategy] = defaultdict(float, weights)
            
            self.learning_rate = model.get('learning_rate', 0.01)
            self.discount_factor = model.get('discount_factor', 0.9)
            self.episode_count = model.get('episode_count', 0)
        except Exception as e:
            print(f"加载模型失败: {e}")


# ==================== 智能分段器 ====================

class SmartSegmenter:
    """智能分段器 - 基于模式分析和机器学习"""
    
    def __init__(self, learning_engine: LearningEngine = None):
        self.learning_engine = learning_engine or LearningEngine()
        self.min_segment_size = 5
    
    def segment(self, arr: List, features: Dict) -> List[Dict]:
        """智能分段"""
        n = len(arr)
        
        if n <= self.min_segment_size * 2:
            return [{'start': 0, 'end': n, 'pattern': 'single', 'features': features}]
        
        strategy_result = self.learning_engine.predict_segmentation(features)
        strategy = strategy_result['strategy']
        
        if strategy == 'monolithic':
            return [{'start': 0, 'end': n, 'pattern': 'single', 'features': features}]
        elif strategy == 'pattern_based':
            return self._pattern_based_segment(arr)
        elif strategy == 'aggressive':
            return self._aggressive_segment(arr)
        else:
            return self._adaptive_segment(arr)
    
    def _pattern_based_segment(self, arr: List) -> List[Dict]:
        """基于模式识别的分段"""
        segments = []
        n = len(arr)
        i = 0
        
        while i < n:
            remaining = n - i
            
            # 检测升序段
            if remaining >= 3:
                j = i
                while j + 1 < n and arr[j] <= arr[j + 1]:
                    j += 1
                if j - i >= self.min_segment_size:
                    segments.append({
                        'start': i,
                        'end': j + 1,
                        'pattern': 'ascending',
                        'features': FeatureExtractor.extract_features(arr[i:j+1])
                    })
                    i = j + 1
                    continue
            
            # 检测降序段
            if remaining >= 3:
                j = i
                while j + 1 < n and arr[j] >= arr[j + 1]:
                    j += 1
                if j - i >= self.min_segment_size:
                    segments.append({
                        'start': i,
                        'end': j + 1,
                        'pattern': 'descending',
                        'features': FeatureExtractor.extract_features(arr[i:j+1])
                    })
                    i = j + 1
                    continue
            
            # 随机段
            end = i + min(self.min_segment_size * 2, remaining)
            while end < n and end - i < 100:
                if end + 2 < n:
                    if (arr[end] <= arr[end+1] <= arr[end+2]) or \
                       (arr[end] >= arr[end+1] >= arr[end+2]):
                        break
                end += 1
            
            segments.append({
                'start': i,
                'end': end,
                'pattern': 'random',
                'features': FeatureExtractor.extract_features(arr[i:end])
            })
            i = end
        
        return segments
    
    def _aggressive_segment(self, arr: List) -> List[Dict]:
        """激进分段 - 追求最大分段数量"""
        n = len(arr)
        segments = []
        window_size = max(20, n // 20)
        
        i = 0
        while i < n:
            end = min(i + window_size, n)
            segment = arr[i:end]
            segments.append({
                'start': i,
                'end': end,
                'pattern': 'random',
                'features': FeatureExtractor.extract_features(segment)
            })
            i = end
        
        return segments
    
    def _adaptive_segment(self, arr: List) -> List[Dict]:
        """自适应分段 - 平衡分段数量和段质量"""
        n = len(arr)
        change_points = self._detect_change_points(arr)
        
        segments = []
        start = 0
        
        for cp in change_points:
            if cp - start >= self.min_segment_size:
                segment = arr[start:cp]
                segments.append({
                    'start': start,
                    'end': cp,
                    'pattern': 'random',
                    'features': FeatureExtractor.extract_features(segment)
                })
                start = cp
        
        if n - start >= self.min_segment_size:
            segment = arr[start:n]
            segments.append({
                'start': start,
                'end': n,
                'pattern': 'random',
                'features': FeatureExtractor.extract_features(segment)
            })
        elif n - start > 0 and segments:
            segments[-1]['end'] = n
            segments[-1]['features'] = FeatureExtractor.extract_features(arr[segments[-1]['start']:n])
        
        return segments
    
    def _detect_change_points(self, arr: List) -> List[int]:
        """检测模式变化点"""
        if len(arr) < 20:
            return []
        
        change_points = []
        window = max(10, len(arr) // 20)
        if window < 2:
            window = 2
        
        for i in range(window, len(arr) - window, max(1, window // 2)):
            left = arr[i-window:i]
            right = arr[i:i+window]
            
            if self._is_pattern_change(left, right):
                change_points.append(i)
        
        return change_points
    
    def _is_pattern_change(self, left: List, right: List) -> bool:
        """判断是否为模式变化点"""
        if len(left) < 3 or len(right) < 3:
            return False
        
        left_trend = FeatureExtractor._detect_trend(left)
        right_trend = FeatureExtractor._detect_trend(right)
        
        if left_trend != right_trend and left_trend != 0 and right_trend != 0:
            return True
        
        if all(isinstance(x, (int, float)) for x in left + right):
            try:
                left_mean = statistics.mean(left)
                right_mean = statistics.mean(right)
                left_std = statistics.stdev(left) if len(left) > 1 else 0
                right_std = statistics.stdev(right) if len(right) > 1 else 0
                
                if abs(left_mean - right_mean) > (left_std + right_std) / 2:
                    return True
            except:
                pass
        
        return False


# ==================== 主排序类 ====================

class SorterML:
    """机器学习驱动的智能排序器"""
    
    def __init__(self, model_file: str = None, enable_learning: bool = True):
        self.learning_engine = LearningEngine(model_file)
        self.segmenter = SmartSegmenter(self.learning_engine)
        self.enable_learning = enable_learning
        self.performance_history = []
    
    def sort(self, arr: List) -> List:
        """智能排序主入口"""
        if not arr:
            return []
        
        if len(arr) <= 1:
            return arr.copy()
        
        # 检查是否已排序
        if all(arr[i] <= arr[i+1] for i in range(len(arr)-1)):
            return arr.copy()
        
        n = len(arr)
        
        # 小数据直接插入排序
        if n <= 20:
            return sortlib.insertion(arr)
        
        # 提取全局特征
        global_features = FeatureExtractor.extract_features(arr)
        
        start_time = time.time()
        
        # 决策：分段还是整体
        if n < 500:
            algo, score = self.learning_engine.predict_algorithm(global_features)
            try:
                result = getattr(sortlib, algo)(arr)
            except:
                result = sorted(arr)
            
            if self.enable_learning:
                reward = 1.0 / (time.time() - start_time + 0.001)
                self.learning_engine.update_weights(
                    global_features, algo, reward, 'monolithic'
                )
            
            return result
        
        # 智能分段
        try:
            segments = self.segmenter.segment(arr, global_features)
        except:
            algo, score = self.learning_engine.predict_algorithm(global_features)
            try:
                result = getattr(sortlib, algo)(arr)
            except:
                result = sorted(arr)
            return result
        
        if len(segments) <= 1:
            algo, score = self.learning_engine.predict_algorithm(global_features)
            try:
                result = getattr(sortlib, algo)(arr)
            except:
                result = sorted(arr)
            
            if self.enable_learning:
                reward = 1.0 / (time.time() - start_time + 0.001)
                self.learning_engine.update_weights(
                    global_features, algo, reward, 'monolithic'
                )
            
            return result
        
        # 对每个段独立排序
        sorted_segments = []
        segment_info = []
        
        for seg in segments:
            segment = arr[seg['start']:seg['end']]
            seg_features = seg['features']
            
            if seg_features.get('is_sorted_asc', False):
                sorted_segment = segment
                algo_used = 'already_sorted'
            elif seg_features.get('is_sorted_desc', False):
                sorted_segment = segment[::-1]
                algo_used = 'reverse'
            else:
                algo, _ = self.learning_engine.predict_algorithm(seg_features)
                try:
                    sorted_segment = getattr(sortlib, algo)(segment)
                except:
                    sorted_segment = sorted(segment)
                algo_used = algo
            
            sorted_segments.append(sorted_segment)
            segment_info.append({
                'start': seg['start'],
                'end': seg['end'],
                'algorithm': algo_used,
                'features': seg_features
            })
        
        # 合并所有段
        result = self._merge_segments(sorted_segments, segment_info)
        
        # 学习反馈
        if self.enable_learning:
            total_time = time.time() - start_time
            reward = 1.0 / (total_time + 0.001)
            
            for seg_info, sorted_seg in zip(segment_info, sorted_segments):
                if seg_info['algorithm'] not in ['already_sorted', 'reverse']:
                    self.learning_engine.update_weights(
                        seg_info['features'],
                        seg_info['algorithm'],
                        reward * (seg_info['end'] - seg_info['start']) / n,
                        'adaptive'
                    )
            
            self.performance_history.append({
                'size': n,
                'segments': len(segments),
                'time': total_time,
                'reward': reward
            })
        
        return result
    
    def _merge_segments(self, sorted_segments: List[List], segment_info: List[Dict]) -> List:
        """多路归并所有段"""
        if len(sorted_segments) == 1:
            return sorted_segments[0]
        
        heap = []
        result = []
        
        for i, seg in enumerate(sorted_segments):
            if seg:
                heapq.heappush(heap, (seg[0], i, 0))
        
        while heap:
            val, seg_idx, elem_idx = heapq.heappop(heap)
            result.append(val)
            
            if elem_idx + 1 < len(sorted_segments[seg_idx]):
                next_val = sorted_segments[seg_idx][elem_idx + 1]
                heapq.heappush(heap, (next_val, seg_idx, elem_idx + 1))
        
        return result


# ==================== 便捷函数 ====================

_global_sorter = SorterML()

def sort(arr: List, model_file: str = None, enable_learning: bool = True) -> List:
    """
    机器学习驱动的智能排序
    
    参数:
        arr: 待排序列表
        model_file: 模型文件路径（可选）
        enable_learning: 是否启用在线学习
    
    返回:
        list: 排序后的新列表
    
    示例:
        >>> from sorter_ml import sort
        >>> sort([3, 1, 4, 1, 5, 9, 2, 6])
        [1, 1, 2, 3, 4, 5, 6, 9]
    """
    if not arr:
        return []
    
    if model_file:
        sorter = SorterML(model_file, enable_learning)
    else:
        sorter = _global_sorter
    
    return sorter.sort(arr)