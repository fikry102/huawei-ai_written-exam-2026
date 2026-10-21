import math
import numpy as np


def initial_centers(points, k):
    n = len(points)
    if k == 1:
        return points.mean(axis=0, keepdims=True)

    order = np.argsort(points[:, 0], kind="stable")
    positions = [i * (n - 1) // (k - 1) for i in range(k)]
    return points[order[positions]].copy()


def k_means(points, k):
    centers = initial_centers(points, k)
    previous_labels = None

    for _ in range(100):
        distances = ((points[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        labels = distances.argmin(axis=1)

        new_centers = centers.copy()
        for cluster in range(k):
            members = points[labels == cluster]
            if len(members) > 0:
                new_centers[cluster] = members.mean(axis=0)

        centers = new_centers
        if previous_labels is not None and np.array_equal(labels, previous_labels):
            break
        previous_labels = labels.copy()

    return centers, labels


def merge_close_clusters(points, centers, labels):
    k = len(centers)
    parent = list(range(k))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    # 距离小于阈值的中心需要传递合并，因此使用并查集。
    for i in range(k):
        for j in range(i + 1, k):
            distance = np.sum((centers[i] - centers[j]) ** 2)
            if distance < 1e-4:
                union(i, j)

    roots = []
    root_to_new = {}
    for cluster in range(k):
        root = find(cluster)
        if root not in root_to_new:
            root_to_new[root] = len(roots)
            roots.append(root)

    merged_labels = np.array([root_to_new[find(int(x))] for x in labels])
    merged_centers = []

    for cluster in range(len(roots)):
        members = points[merged_labels == cluster]
        if len(members) > 0:
            merged_centers.append(members.mean(axis=0))
        else:
            old_ids = [i for i in range(k) if root_to_new[find(i)] == cluster]
            merged_centers.append(centers[old_ids].mean(axis=0))

    merged_centers = np.array(merged_centers)
    sse = np.sum((points - merged_centers[merged_labels]) ** 2)
    return merged_centers, merged_labels, float(sse)


def calculate_bic(n, sse, k, dimension):
    parameters = k * (dimension + 1)
    return n * math.log((sse + 1e-8) / n) + parameters * math.log(n)


def x_means(points, k_min, k_max):
    n, dimension = points.shape
    k_max = min(k_max, n)
    k_min = min(k_min, k_max)

    best = None
    for requested_k in range(k_min, k_max + 1):
        centers, labels = k_means(points, requested_k)
        centers, labels, sse = merge_close_clusters(points, centers, labels)
        bic = calculate_bic(n, sse, len(centers), dimension)

        if best is None or bic < best[0] - 1e-12 or (
            abs(bic - best[0]) <= 1e-12 and requested_k < best[1]
        ):
            best = bic, requested_k, centers, labels

    _, _, centers, labels = best

    # 中心按字典序输出，并同步重编号每个样本的标签。
    order = sorted(range(len(centers)), key=lambda i: tuple(centers[i]))
    new_id = {old: new for new, old in enumerate(order)}
    centers = centers[order]
    labels = np.array([new_id[int(label)] for label in labels])
    return centers, labels


def format_number(value):
    text = f"{value:.2f}"
    return "0.00" if text == "-0.00" else text


def main():
    n, dimension = map(int, input().split())

    rows = []
    for _ in range(n):
        rows.append(list(map(float, input().split())))
    points = np.array(rows, dtype=float)

    k_min, k_max = map(int, input().split())
    centers, labels = x_means(points, k_min, k_max)

    print(len(centers))
    for center in centers:
        print(*(format_number(value) for value in center))
    print(*labels)


if __name__ == "__main__":
    main()
