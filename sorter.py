"""
sorter.py - 完整的排序算法库
包含所有经典、实用及有教育意义的排序算法

算法列表：
1. 基础排序 (O(n²)): bubble, selection, insertion, cocktail, odd_even, gnome
2. 高级排序 (O(n log n)): merge, quick, heap, shell, comb, intro, tim
3. 线性排序 (O(n)): counting, radix, bucket
4. 树结构排序: tree
5. 特殊排序: pancake, cycle, patience, bitonic
6. 外部排序: external

用法:
    from sorter import sort, sortlib
    
    # 智能排序（自动选择最优算法）
    result = sort([3, 1, 4, 1, 5])
    
    # 使用特定算法
    result = sortlib.quick([3, 1, 4, 1, 5])
"""

import statistics
import heapq
import math
import sys


class sortlib:
    """排序算法库 - 所有方法均为静态方法，返回新数组，不修改原数组"""
    
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
        
        sys.setrecursionlimit(max(1000000, len(arr) * 2))
        
        def _quick_sort(arr, low, high):
            if low < high:
                if high - low <= 16:
                    _insertion_sort(arr, low, high)
                    return
                pi = _partition(arr, low, high)
                _quick_sort(arr, low, pi - 1)
                _quick_sort(arr, pi + 1, high)
        
        def _insertion_sort(arr, low, high):
            for i in range(low + 1, high + 1):
                key = arr[i]
                j = i - 1
                while j >= low and arr[j] > key:
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = key
        
        def _partition(arr, low, high):
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
        
        try:
            _quick_sort(arr, 0, len(arr) - 1)
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
        max_depth = n.bit_length() * 2
        
        sys.setrecursionlimit(max(1000000, n * 2))
        
        def _intro_sort(arr, low, high, depth_limit):
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
        
        def _insertion_sort(arr, low, high):
            for i in range(low + 1, high + 1):
                key = arr[i]
                j = i - 1
                while j >= low and arr[j] > key:
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = key
        
        def _partition(arr, low, high):
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
    
    # ==================== 外部排序 ====================
    
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


# ==================== 智能排序引擎 ====================

class AlgorithmScorer:
    """算法评分器 - 为每个算法计算适合度分数"""
    
    def __init__(self):
        self.algorithms = {
            'bubble': sortlib.bubble,
            'selection': sortlib.selection,
            'insertion': sortlib.insertion,
            'cocktail': sortlib.cocktail,
            'odd_even': sortlib.odd_even,
            'gnome': sortlib.gnome,
            'merge': sortlib.merge,
            'quick': sortlib.quick,
            'heap': sortlib.heap,
            'shell': sortlib.shell,
            'comb': sortlib.comb,
            'intro': sortlib.intro,
            'tim': sortlib.tim,
            'counting': sortlib.counting,
            'radix': sortlib.radix,
            'bucket': sortlib.bucket,
            'tree': sortlib.tree,
            'pancake': sortlib.pancake,
            'cycle': sortlib.cycle,
            'patience': sortlib.patience,
            'bitonic': sortlib.bitonic,
        }
    
    def _score_complexity(self, name, n):
        """基于时间复杂度评分"""
        scores = {
            'bubble': n * n * 0.5,
            'selection': n * n * 0.5,
            'insertion': n * n * 0.3,
            'cocktail': n * n * 0.4,
            'odd_even': n * n * 0.5,
            'gnome': n * n * 0.6,
            'merge': n * math.log2(n) * 0.08,
            'quick': n * math.log2(n) * 0.06,
            'heap': n * math.log2(n) * 0.10,
            'shell': n * math.log2(n) * 0.12,
            'comb': n * math.log2(n) * 0.10,
            'intro': n * math.log2(n) * 0.07,
            'tim': n * math.log2(n) * 0.06,
            'counting': n * 0.05,
            'radix': n * 0.08,
            'bucket': n * 0.06,
            'tree': n * math.log2(n) * 0.15,
            'pancake': n * n * 0.8,
            'cycle': n * n * 0.7,
            'patience': n * math.log2(n) * 0.20,
            'bitonic': n * math.log2(n) * 0.25,
        }
        return scores.get(name, n * math.log2(n))
    
    def _score_stability(self, name):
        """稳定性评分（稳定算法加分）"""
        stable = {'bubble', 'insertion', 'cocktail', 'odd_even', 'gnome', 
                  'merge', 'counting', 'radix', 'bucket', 'tree', 'patience', 'tim'}
        return 0 if name in stable else 5
    
    def _score_memory(self, name):
        """内存使用评分"""
        o1 = {'bubble', 'selection', 'insertion', 'cocktail', 'odd_even', 'gnome',
              'heap', 'shell', 'comb', 'pancake', 'cycle'}
        on = {'merge', 'quick', 'intro', 'tim', 'counting', 'radix', 'bucket',
              'tree', 'patience', 'bitonic'}
        return 0 if name in o1 else 3
    
    def _score_data_fit(self, name, analysis):
        """数据特征匹配评分"""
        score = 0
        n = analysis['size']
        
        # 1. 整数数据
        if analysis['is_int']:
            if name in ['counting', 'radix']:
                score -= 10
            if name == 'bucket' and analysis.get('is_uniform', False):
                score -= 8
        
        # 2. 小范围整数 - 计数排序最优
        if analysis.get('suitable_counting', False):
            if name == 'counting':
                score -= 20
            elif name in ['radix', 'bucket']:
                score -= 5
        
        # 3. 大范围整数 - 基数排序
        if analysis.get('suitable_radix', False):
            if name == 'radix':
                score -= 15
            elif name == 'quick':
                score -= 3
        
        # 4. 近乎有序 - 插入排序最优
        if analysis.get('is_almost_sorted', False):
            if name == 'insertion':
                score -= 25
            elif name in ['bubble', 'cocktail']:
                score -= 15
        
        # 5. 已排序
        if analysis.get('is_sorted', False):
            if name in ['insertion', 'bubble']:
                score -= 10
        
        # 6. 降序
        if analysis.get('is_sorted_desc', False):
            if name in ['insertion', 'bubble']:
                score -= 8
        
        # 7. 高重复率
        if analysis.get('duplicate_rate', 0) > 0.3:
            if name == 'counting':
                score -= 15
            elif name == 'insertion':
                score -= 10
        
        # 8. 均匀分布
        if analysis.get('is_uniform', False):
            if name == 'bucket':
                score -= 15
            elif name == 'quick':
                score -= 5
        
        # 9. 数据大小
        if n > 100000:
            if name in ['counting', 'radix', 'bucket']:
                score -= 10
            elif name in ['merge', 'quick', 'intro', 'tim']:
                score -= 5
            elif name in ['bubble', 'selection', 'insertion', 'cocktail', 'odd_even', 'gnome']:
                score += 20
        elif n < 100:
            if name == 'insertion':
                score -= 15
            elif name in ['bubble', 'selection']:
                score -= 8
        
        return score
    
    def _score_parallel(self, name):
        """并行友好度评分"""
        parallel = {'odd_even', 'bitonic'}
        return 0 if name in parallel else 2
    
    def score_algorithm(self, name, analysis):
        """综合评分算法 - 分数越低越好"""
        n = analysis['size']
        
        score = self._score_complexity(name, n)
        score += self._score_stability(name)
        score += self._score_memory(name)
        score += self._score_data_fit(name, analysis)
        score += self._score_parallel(name)
        
        return score


def _analyze_segment(arr):
    """全面分析数据段特征"""
    if not arr:
        return {'empty': True, 'size': 0}
    
    n = len(arr)
    
    # 类型检测
    is_int = all(isinstance(x, int) for x in arr)
    is_float = all(isinstance(x, (int, float)) for x in arr)
    is_numeric = is_float
    
    # 排序状态
    is_sorted_asc = all(arr[i] <= arr[i+1] for i in range(n-1))
    is_sorted_desc = all(arr[i] >= arr[i+1] for i in range(n-1))
    is_sorted = is_sorted_asc or is_sorted_desc
    
    # 逆序对检测（采样）
    inversions = 0
    sample_size = min(n, 200)
    for i in range(sample_size):
        for j in range(i+1, min(n, i+100)):
            if arr[i] > arr[j]:
                inversions += 1
    max_inv = sample_size * min(n-1, 99) if n > 1 else 1
    inv_rate = inversions / max_inv if max_inv > 0 else 0
    
    # 数据范围
    range_size = 0
    min_val = None
    max_val = None
    if is_numeric:
        min_val = min(arr)
        max_val = max(arr)
        range_size = max_val - min_val + 1
    
    # 唯一值和重复率
    unique_count = len(set(arr)) if is_numeric else n
    duplicate_rate = 1 - unique_count / n if n > 0 else 0
    
    # 均匀分布检测
    is_uniform = False
    if is_numeric and n > 10 and range_size > 1:
        try:
            mean = statistics.mean(arr[:min(n, 1000)])
            stdev = statistics.stdev(arr[:min(n, 1000)]) if n > 1 else 0
            if range_size > 0 and stdev > 0:
                uniform_ratio = stdev / (max_val - min_val)
                is_uniform = 0.25 < uniform_ratio < 0.55
        except:
            pass
    
    return {
        'empty': False,
        'size': n,
        'is_int': is_int,
        'is_float': is_float,
        'is_numeric': is_numeric,
        'is_sorted': is_sorted,
        'is_sorted_asc': is_sorted_asc,
        'is_sorted_desc': is_sorted_desc,
        'inv_rate': inv_rate,
        'is_almost_sorted': inv_rate < 0.08,
        'range_size': range_size,
        'unique_count': unique_count,
        'duplicate_rate': duplicate_rate,
        'is_uniform': is_uniform,
        'min_val': min_val,
        'max_val': max_val,
        'suitable_counting': is_int and 1 <= range_size <= n * 2 and range_size < 1000000,
        'suitable_radix': is_int and range_size > n * 2 and range_size < 10**9,
        'suitable_bucket': is_numeric and is_uniform and n > 50,
    }


def _select_best_algorithm(analysis):
    """使用评分系统选择最优算法"""
    if analysis['empty'] or analysis['is_sorted']:
        return None, 'already_sorted', 0
    
    scorer = AlgorithmScorer()
    
    scores = []
    for name in scorer.algorithms:
        score = scorer.score_algorithm(name, analysis)
        scores.append((name, score))
    
    scores.sort(key=lambda x: x[1])
    
    best_name, best_score = scores[0]
    return scorer.algorithms[best_name], best_name, best_score


def _should_chunk(arr, analysis):
    """
    智能决策是否应该分块
    
    分块条件：
    1. 数据量 >= 500
    2. 多特征混合（不是单一特征）
    3. 不是完全随机（纯随机不分块，因为分块无意义）
    4. 存在明显的模式段
    """
    n = len(arr)
    
    # 数据太小不分块
    if n < 500:
        return False
    
    # 适合计数排序 - 数据特征单一，不分块
    if analysis['suitable_counting']:
        return False
    
    # 适合基数排序 - 数据特征单一，不分块
    if analysis['suitable_radix']:
        return False
    
    # 完全随机且逆序率极高 - 分块无意义
    if analysis['inv_rate'] > 0.45:
        return False
    
    # 已排序或近乎有序 - 不分块
    if analysis['is_sorted'] or analysis['is_almost_sorted']:
        return False
    
    # 检查是否有多种模式（升序段+降序段+随机段混合）
    segments = _detect_patterns(arr)
    if len(segments) <= 2:
        return False
    
    # 检查各段类型是否多样
    pattern_types = set(seg_type for _, _, seg_type, _ in segments)
    if len(pattern_types) <= 1:
        return False
    
    # 检查是否有足够大的段来值得分块
    large_segments = sum(1 for start, end, _, _ in segments if end - start > n * 0.1)
    if large_segments < 2:
        return False
    
    # 多特征且数据量大 → 分块
    return True


def _detect_patterns(arr):
    """检测列表中的模式并分块"""
    if len(arr) <= 1:
        return [(0, len(arr), 'random', _analyze_segment(arr))]
    
    n = len(arr)
    segments = []
    i = 0
    min_segment = 3
    
    while i < n:
        # 1. 检测升序段
        j = i
        while j + 1 < n and arr[j] <= arr[j + 1]:
            j += 1
        if j - i >= min_segment:
            segment = arr[i:j+1]
            segments.append((i, j+1, 'sorted_asc', _analyze_segment(segment)))
            i = j + 1
            continue
        
        # 2. 检测降序段
        j = i
        while j + 1 < n and arr[j] >= arr[j + 1]:
            j += 1
        if j - i >= min_segment:
            segment = arr[i:j+1]
            segments.append((i, j+1, 'sorted_desc', _analyze_segment(segment)))
            i = j + 1
            continue
        
        # 3. 检测小范围整数段
        if i + 5 < n:
            sub = arr[i:min(i+30, n)]
            if all(isinstance(x, int) for x in sub):
                range_size = max(sub) - min(sub) + 1
                if range_size <= len(sub) * 1.5 and range_size < 100:
                    segments.append((i, min(i+30, n), 'small_range', _analyze_segment(sub)))
                    i = min(i+30, n)
                    continue
        
        # 4. 检测均匀分布段
        if i + 10 < n:
            sub = arr[i:min(i+40, n)]
            if all(isinstance(x, (int, float)) for x in sub):
                min_val = min(sub)
                max_val = max(sub)
                if max_val > min_val:
                    try:
                        stdev = statistics.stdev(sub)
                        if stdev > 0:
                            uniform_ratio = stdev / (max_val - min_val)
                            if 0.25 < uniform_ratio < 0.55:
                                segments.append((i, min(i+40, n), 'uniform', _analyze_segment(sub)))
                                i = min(i+40, n)
                                continue
                    except:
                        pass
        
        # 5. 随机段
        end = i + 1
        while end < n:
            if end + 2 < n:
                if (arr[end] <= arr[end+1] <= arr[end+2]):
                    trend_len = 1
                    while end + trend_len + 1 < n and arr[end + trend_len] <= arr[end + trend_len + 1]:
                        trend_len += 1
                    if trend_len >= min_segment - 1:
                        break
                
                if (arr[end] >= arr[end+1] >= arr[end+2]):
                    trend_len = 1
                    while end + trend_len + 1 < n and arr[end + trend_len] >= arr[end + trend_len + 1]:
                        trend_len += 1
                    if trend_len >= min_segment - 1:
                        break
            end += 1
        
        if end <= i:
            end = i + 1
        segment = arr[i:end]
        segments.append((i, end, 'random', _analyze_segment(segment)))
        i = end
    
    return segments


def _merge_segments(sorted_segments):
    """使用多路归并合并所有排序段"""
    all_elements = []
    for sorted_data, start, end in sorted_segments:
        for idx, val in enumerate(sorted_data):
            all_elements.append((val, start + idx))
    
    all_elements.sort(key=lambda x: (x[0], x[1]))
    return [val for val, _ in all_elements]


def sort(arr):
    """
    智能排序 - 完整的自适应排序系统
    
    流程：
    1. 全面分析数据特征
    2. 使用评分系统评估所有22种算法
    3. 智能决策是否分块（多特征混合且数据量大）
    4. 检测数据中的模式并分块
    5. 每块使用评分最高的算法
    6. 多路归并合并所有块
    
    参数:
        arr: 待排序列表
    
    返回:
        list: 排序后的新列表
    
    示例:
        >>> from sorter import sort
        >>> sort([3, 1, 4, 1, 5, 9, 2, 6])
        [1, 1, 2, 3, 4, 5, 6, 9]
    """
    if not arr:
        return []
    
    # 检查是否已完全排序
    if all(arr[i] <= arr[i+1] for i in range(len(arr)-1)):
        return arr.copy()
    
    n = len(arr)
    
    # 小数据直接插入排序
    if n <= 20:
        return sortlib.insertion(arr)
    
    # 检查是否整体降序
    if all(arr[i] >= arr[i+1] for i in range(n-1)):
        return arr[::-1]
    
    # 1. 全局分析
    global_analysis = _analyze_segment(arr)
    
    # 2. 智能决策是否分块
    if not _should_chunk(arr, global_analysis):
        # 不分块，直接使用评分最高的算法
        best_func, best_name, _ = _select_best_algorithm(global_analysis)
        if best_func is None:
            return arr.copy()
        return best_func(arr)
    
    # 3. 检测模式并分块
    segments = _detect_patterns(arr)
    
    # 如果段数太少，不分块
    if len(segments) <= 1:
        best_func, best_name, _ = _select_best_algorithm(global_analysis)
        if best_func is None:
            return arr.copy()
        return best_func(arr)
    
    # 4. 对每块独立排序
    sorted_segments = []
    
    for start, end, pattern, analysis in segments:
        segment = arr[start:end]
        
        # 根据模式快速处理
        if pattern == 'sorted_asc':
            sorted_data = segment
            algo = 'already_sorted_asc'
        elif pattern == 'sorted_desc':
            sorted_data = segment[::-1]
            algo = 'reverse_desc'
        else:
            # 使用评分系统选择该块的最优算法
            block_func, block_name, _ = _select_best_algorithm(analysis)
            
            if block_func is None:
                sorted_data = segment
                algo = 'none'
            else:
                sorted_data = block_func(segment)
                algo = block_name
        
        sorted_segments.append((sorted_data, start, end))
    
    # 5. 多路归并
    result = _merge_segments(sorted_segments)
    
    return result