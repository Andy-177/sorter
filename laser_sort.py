def laser_sort(pillars):
    """
    激光排序
    pillars: 整数列表（代表柱子的高度）
    """
    if not pillars:
        return []
    
    # 统计柱子总数
    total_count = len(pillars)
    print(f"初始柱子数量: {total_count}")
    
    # 结果列表
    result = []
    
    # 第一阶段：从下到上扫描，找到最高高度
    height = 1
    max_height = 0
    
    while True:
        hit = False
        for p in pillars:              # 遍历所有柱子
            if p >= height:            # 碰撞检测
                hit = True
                break
        if hit:
            max_height = height
            height += 1
        else:
            break
    
    print(f"最高高度: {max_height}")
    
    # 第二阶段：从上到下扫描，碰撞 → 记录 → 消失
    remaining = pillars.copy()
    
    for h in range(max_height, 0, -1):
        # 遍历当前所有还存在的柱子
        for p in remaining[:]:         # 遍历副本，避免跳过元素
            if p == h:                 # 碰撞检测（精确匹配）
                result.append(p)       # 记录高度
                remaining.remove(p)    # 柱子消失
                total_count -= 1       # 剩余柱子数量-1
                print(f"柱子 {p} 消失，剩余柱子数量: {total_count}")
                
                # 当所有柱子都消失时，提前结束排序
                if total_count == 0:
                    print("所有柱子已消失，排序完成")
                    return result
    
    return result


# 测试
if __name__ == "__main__":
    # 柱子高度列表
    pillars = [3, 1, 5, 2, 10000000]
    
    sorted_values = laser_sort(pillars)
    print(f"排序结果: {sorted_values}")
