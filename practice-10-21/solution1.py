"""K-Median 聚类：NumPy 实现。"""

import numpy as np


def format_number(value):
    value = float(value)
    if abs(value) < 0.5e-9:
        value = 0.0
    return f"{value:.6f}"


def k_median(points, k):
    n, d = points.shape
    centers = points[:k].copy()
    labels = np.zeros(n, dtype=np.int64)

    for _ in range(100):
        # 按维累加，避免创建 n×k×d 的超大临时数组。
        distances = np.zeros((n, k), dtype=np.float64)
        for feature in range(d):
            distances += np.abs(
                points[:, feature, None] - centers[None, :, feature]
            )

        # argmin 在距离相同时自然选择编号较小的簇。
        labels = np.argmin(distances, axis=1)
        new_centers = centers.copy()
        for cluster in range(k):
            members = points[labels == cluster]
            if members.size:  # 空簇保持原中心。
                new_centers[cluster] = np.median(members, axis=0)

        shift = np.abs(new_centers - centers).sum()
        centers = new_centers
        if shift < 1e-4:
            break

    inertia = np.abs(points - centers[labels]).sum()
    return labels, centers, inertia


def main():
    n, d, k = map(int, input().split())

    rows = []
    for _ in range(n):
        rows.append(list(map(float, input().split())))

    points = np.array(rows)
    labels, centers, inertia = k_median(points, k)

    print(*labels)
    for center in centers:
        print(*(format_number(value) for value in center))
    print(format_number(inertia))


if __name__ == "__main__":
    main()
