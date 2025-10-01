from typing import List, Tuple

def min_sum_and_path_lowmem(triangle: List[List[int]]) -> Tuple[int, str]:
    """
    Возвращает (min_sum, path_string) для имеющегося треугольника.
    Память: O(n), время: O(n^2).
    Формат пути: "a -> b -> c -> ...".
    """
    if not triangle:
        raise ValueError("triangle must be non-empty")

    n = len(triangle)

    # 1) Вычисляем минимальную сумму снизу-вверх, O(n) памяти
    dp = triangle[-1][:]
    for i in range(n - 2, -1, -1):
        # для каждой позиции j в строке i берем min(dp[j], dp[j+1])
        dp = [triangle[i][j] + min(dp[j], dp[j+1]) for j in range(i + 1)]
    min_sum = dp[0]

    # Вспомогательная функция: минимальные стоимости от каждой позиции строки r до основания (включая r)
    def backward_cost_to_row(r: int) -> List[int]:
        # строим DP от низа до строки r (поднимаясь вверх), O(n) памяти
        cur = triangle[-1][:]
        for i in range(len(triangle) - 2, r - 1, -1):
            nxt = [triangle[i][j] + min(cur[j], cur[j + 1]) for j in range(i + 1)]
            cur = nxt
        return cur  # length r+1

    # 2) Восстанавливаем путь сверху вниз:
    path = [triangle[0][0]]
    j = 0
    for i in range(0, n - 1):
        # получаем массив минимальных затрат от строки i+1 до низа
        bwd = backward_cost_to_row(i + 1)
        # выбираем между (i+1, j) и (i+1, j+1)
        # (так как префикс до i одинаков для обоих, достаточно сравнить стоимости продолжений)
        # при равенстве выбираем "влево" (стабильность)
        if bwd[j] <= bwd[j + 1]:
            j = j
        else:
            j = j + 1
        path.append(triangle[i + 1][j])

    path_str = " -> ".join(str(x) for x in path)
    return min_sum, path_str


# ========== Примеры ==========
if __name__ == "__main__":
    tri1 = [[2],
            [3, 4],
            [6, 5, 7],
            [4, 1, 8, 3]]
    s1, p1 = min_sum_and_path_lowmem(tri1)
    print("Минимальная сумма:", s1)   # 11
    print("Путь:", p1)               # "2 -> 3 -> 5 -> 1"

    tri2 = [[-1],
            [2, 3],
            [1, -1, -3],
            [4, 2, 1, 3]]
    s2, p2 = min_sum_and_path_lowmem(tri2)
    print("Минимальная сумма:", s2)   # 0
    print("Путь:", p2)               # "-1 -> 3 -> -3 -> 1"

