"""
trainer_fixed.py - 修复版训练器
"""

import json
import os
import random
import time
import math
from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict
import statistics
import argparse

from sorter_ml import sortlib, FeatureExtractor, LearningEngine, SorterML, sort


class FixedTrainer:
    """修复版训练器"""
    
    def __init__(self, model_file: str = 'sort_model_fixed.json'):
        self.model_file = model_file
        self.sorter = SorterML(model_file, enable_learning=True)
        self.training_history = []
        self.best_performance_ratio = 0.0
        self.total_samples = 0
        
        # 所有算法列表
        self.all_algorithms = self._get_all_algorithms()
        
    def _get_all_algorithms(self) -> List[str]:
        """获取所有算法"""
        return [name for name in dir(sortlib) 
                if not name.startswith('_') and callable(getattr(sortlib, name))]
    
    # ==================== 数据生成器 ====================
    
    def generate_data(self, size: int) -> Tuple[List, str]:
        """生成各种类型的数据"""
        generators = [
            ('random', lambda: [random.randint(0, 1000) for _ in range(size)]),
            ('sorted', lambda: list(range(size))),
            ('almost_sorted', lambda: self._almost_sorted(size, 0.05)),
            ('descending', lambda: list(range(size, 0, -1))),
            ('with_duplicates', lambda: self._with_duplicates(size, 0.3)),
            ('small_range', lambda: [random.randint(0, 10) for _ in range(size)]),
        ]
        
        name, generator = random.choice(generators)
        return generator(), name
    
    def _almost_sorted(self, size: int, disorder: float) -> List:
        data = list(range(size))
        num_swaps = max(1, int(size * disorder))
        for _ in range(min(num_swaps, size)):
            i = random.randint(0, size - 2)
            j = random.randint(i + 1, min(i + 10, size - 1))
            data[i], data[j] = data[j], data[i]
        return data
    
    def _with_duplicates(self, size: int, unique_ratio: float) -> List:
        unique_count = max(1, int(size * unique_ratio))
        base = list(range(unique_count))
        data = [random.choice(base) for _ in range(size)]
        random.shuffle(data)
        return data
    
    # ==================== 完整基准测试 ====================
    
    def benchmark_all(self, data: List, iterations: int = 2) -> Dict[str, float]:
        """测试所有算法，找到真正的最优"""
        sorted_data = sorted(data)
        results = {}
        
        for algo_name in self.all_algorithms:
            try:
                func = getattr(sortlib, algo_name)
                times = []
                
                for _ in range(iterations):
                    test_data = data.copy()
                    start = time.perf_counter()
                    result = func(test_data)
                    elapsed = time.perf_counter() - start
                    
                    if result == sorted_data:
                        times.append(elapsed)
                
                if times:
                    results[algo_name] = min(times)  # 取最快的一次
                else:
                    results[algo_name] = float('inf')
                    
            except Exception as e:
                results[algo_name] = float('inf')
        
        return results
    
    # ==================== 训练 ====================
    
    def train_on_sample(self, data: List) -> Dict:
        """在单个样本上训练 - 修复版"""
        if not data or len(data) < 2:
            return None
        
        features = FeatureExtractor.extract_features(data)
        
        # 1. 完整基准测试 - 找到真正最优
        baseline = self.benchmark_all(data, iterations=2)
        
        # 过滤有效结果
        valid_results = {k: v for k, v in baseline.items() if v < float('inf')}
        if not valid_results:
            return None
        
        # 找到真正最优的算法
        best_algo = min(valid_results, key=valid_results.get)
        best_time = valid_results[best_algo]
        
        # 2. 模型预测
        predicted_algo, _ = self.sorter.learning_engine.predict_algorithm(features)
        predicted_time = baseline.get(predicted_algo, float('inf'))
        
        # 3. 计算性能比（相对最优算法）
        if predicted_time < float('inf') and best_time > 0:
            performance_ratio = best_time / predicted_time
        else:
            performance_ratio = 0.0
        
        # ===== 修复: 新的奖励函数 =====
        # 不再要求完全匹配，而是基于性能比给予奖励
        
        if performance_ratio >= 0.95:
            # 非常接近最优（在5%以内）
            reward = 1.0
        elif performance_ratio >= 0.8:
            # 接近最优（在20%以内）
            reward = 0.7
        elif performance_ratio >= 0.6:
            # 还可以
            reward = 0.4
        elif performance_ratio >= 0.4:
            # 勉强可以
            reward = 0.1
        else:
            # 太慢了，给予小负奖励
            reward = -0.2
        
        # 额外奖励：如果算法是正确的（能排序）
        if predicted_time < float('inf'):
            reward += 0.1  # 能正确排序的基础奖励
        
        # ===== 更新权重 =====
        self.sorter.learning_engine.update_weights(
            features, predicted_algo, reward, 'monolithic'
        )
        
        # ===== 统计 =====
        self.total_samples += 1
        is_correct = predicted_algo == best_algo
        
        return {
            'size': len(data),
            'best_algo': best_algo,
            'predicted_algo': predicted_algo,
            'is_correct': is_correct,
            'performance_ratio': performance_ratio,
            'reward': reward
        }
    
    def train_epoch(self, batch_size: int = 20) -> Dict:
        """训练一个轮次"""
        correct = 0
        total = 0
        perf_ratios = []
        rewards = []
        
        for _ in range(batch_size):
            # 随机选择数据大小
            size = random.choice([10, 20, 50, 100, 200, 500, 1000])
            
            # 生成数据
            data, data_type = self.generate_data(size)
            
            # 训练
            result = self.train_on_sample(data)
            
            if result:
                total += 1
                if result['is_correct']:
                    correct += 1
                perf_ratios.append(result['performance_ratio'])
                rewards.append(result['reward'])
        
        return {
            'accuracy': correct / total if total > 0 else 0,
            'avg_performance_ratio': statistics.mean(perf_ratios) if perf_ratios else 0,
            'avg_reward': statistics.mean(rewards) if rewards else 0,
            'samples': total
        }
    
    def train(self, epochs: int = 50, batch_size: int = 30):
        """主训练循环"""
        print("=" * 80)
        print("修复版训练器")
        print("=" * 80)
        print(f"训练配置:")
        print(f"  - 训练轮数: {epochs}")
        print(f"  - 批次大小: {batch_size}")
        print(f"  - 算法数量: {len(self.all_algorithms)}")
        print("=" * 80)
        print("\n开始训练...\n")
        print(f"{'Epoch':<8} {'Accuracy':<12} {'Perf Ratio':<12} {'Avg Reward':<12} {'Best Perf':<12}")
        print("-" * 70)
        
        best_perf = 0.0
        patience = 0
        
        for epoch in range(1, epochs + 1):
            result = self.train_epoch(batch_size)
            
            # 更新最佳性能
            if result['avg_performance_ratio'] > best_perf:
                best_perf = result['avg_performance_ratio']
                patience = 0
                # 保存模型
                self.sorter.learning_engine.save_model(self.model_file)
                status = "⭐"
            else:
                patience += 1
                status = "⏳"
            
            print(f"{epoch:<8} {result['accuracy']:<12.4f} "
                  f"{result['avg_performance_ratio']:<12.4f} "
                  f"{result['avg_reward']:<12.4f} "
                  f"{best_perf:<12.4f} {status}")
            
            # 早停
            if patience >= 10:
                print(f"\n⏹ 早停触发 (连续10轮无提升)")
                break
            
            # 动态调整学习率
            if epoch % 10 == 0:
                old_lr = self.sorter.learning_engine.learning_rate
                self.sorter.learning_engine.learning_rate = max(old_lr * 0.8, 0.001)
                print(f"  📉 学习率: {old_lr:.6f} -> {self.sorter.learning_engine.learning_rate:.6f}")
        
        print("\n" + "=" * 80)
        print("训练完成!")
        print(f"最佳性能比: {best_perf:.4f}")
        print(f"总训练样本: {self.total_samples}")
        print(f"模型保存到: {self.model_file}")
        print("=" * 80)
    
    def evaluate(self, num_tests: int = 50):
        """评估模型"""
        print("\n" + "=" * 70)
        print("模型评估")
        print("=" * 70)
        
        correct = 0
        perf_ratios = []
        
        for i in range(num_tests):
            size = random.choice([10, 20, 50, 100, 200, 500])
            data, _ = self.generate_data(size)
            
            # 基准测试
            baseline = self.benchmark_all(data, iterations=2)
            valid = {k: v for k, v in baseline.items() if v < float('inf')}
            if not valid:
                continue
            
            best_algo = min(valid, key=valid.get)
            best_time = valid[best_algo]
            
            # 预测
            features = FeatureExtractor.extract_features(data)
            predicted_algo, _ = self.sorter.learning_engine.predict_algorithm(features)
            predicted_time = baseline.get(predicted_algo, float('inf'))
            
            if predicted_algo == best_algo:
                correct += 1
            
            if best_time > 0 and predicted_time < float('inf'):
                perf_ratios.append(best_time / predicted_time)
        
        print(f"\n评估结果 (测试 {len(perf_ratios)} 个样本):")
        print(f"  准确率: {correct / len(perf_ratios) if perf_ratios else 0:.4f}")
        print(f"  平均性能比: {statistics.mean(perf_ratios) if perf_ratios else 0:.4f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--batch-size', type=int, default=30)
    parser.add_argument('--model', type=str, default='sort_model_fixed.json')
    parser.add_argument('--evaluate', action='store_true')
    
    args = parser.parse_args()
    
    trainer = FixedTrainer(args.model)
    
    trainer.train(epochs=args.epochs, batch_size=args.batch_size)
    
    if args.evaluate:
        trainer.evaluate(50)


if __name__ == "__main__":
    main()