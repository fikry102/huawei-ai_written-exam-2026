"""P5612 K-Median 聚类：不依赖 NumPy 的标准库实现。"""

def median(values):
    values.sort()
    middle = len(values) // 2
    if len(values) % 2:
        return values[middle]
    return (values[middle - 1] + values[middle]) / 2.0


def format_number(value):
    if abs(value) < 0.5e-9:
        value = 0.0
    return f"{value:.6f}"


def k_median(points, k):
    n = len(points)
    d = len(points[0])
    centers = [point[:] for point in points[:k]]
    labels = [0] * n

    for _ in range(100):
        groups = [[] for _ in range(k)]
        for index, point in enumerate(points):
            best_cluster = 0
            best_distance = sum(abs(point[j] - centers[0][j]) for j in range(d))
            for cluster in range(1, k):
                distance = sum(
                    abs(point[j] - centers[cluster][j]) for j in range(d)
                )
                if distance < best_distance:
                    best_distance = distance
                    best_cluster = cluster
            labels[index] = best_cluster
            groups[best_cluster].append(index)

        new_centers = [center[:] for center in centers]
        for cluster, members in enumerate(groups):
            if not members:  # 空簇保持原中心。
                continue
            for feature in range(d):
                new_centers[cluster][feature] = median(
                    [points[index][feature] for index in members]
                )

        shift = sum(
            abs(new_centers[c][j] - centers[c][j])
            for c in range(k)
            for j in range(d)
        )
        centers = new_centers
        if shift < 1e-4:
            break

    inertia = sum(
        abs(points[i][j] - centers[labels[i]][j])
        for i in range(n)
        for j in range(d)
    )
    return labels, centers, inertia


def main():
    n, d, k = map(int, input().split())

    points = []
    for _ in range(n):
        points.append(list(map(float, input().split())))

    labels, centers, inertia = k_median(points, k)

    print(*labels)
    for center in centers:
        print(*(format_number(value) for value in center))
    print(format_number(inertia))


if __name__ == "__main__":
    main()
