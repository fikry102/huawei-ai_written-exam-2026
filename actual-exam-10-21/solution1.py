import math


def entropy(labels):
    """计算只含 0、1 两类标签的熵。"""
    if not labels:
        return 0.0

    probability = sum(labels) / len(labels)
    if probability == 0 or probability == 1:
        return 0.0

    return (
        -probability * math.log2(probability)
        - (1 - probability) * math.log2(1 - probability)
    )


def majority_vote(labels):
    """类别 1 更多时返回 1；数量相同时按题意返回 0。"""
    return 1 if sum(labels) * 2 > len(labels) else 0


def build_tree(features, labels, available_features):
    # 当前节点已经是纯节点。
    if len(set(labels)) == 1:
        return labels[0]

    # 当前路径上的三个特征都已使用。
    if not available_features:
        return majority_vote(labels)

    current_entropy = entropy(labels)
    best_feature = -1
    best_gain = 0.0
    best_split = None

    # 按特征编号从小到大遍历，因此增益严格相同时自然保留较小编号。
    for feature in available_features:
        labels_0 = [
            labels[i]
            for i in range(len(labels))
            if features[i][feature] == 0
        ]
        labels_1 = [
            labels[i]
            for i in range(len(labels))
            if features[i][feature] == 1
        ]

        conditional_entropy = (
            len(labels_0) * entropy(labels_0)
            + len(labels_1) * entropy(labels_1)
        ) / len(labels)
        information_gain = current_entropy - conditional_entropy

        if information_gain > best_gain + 1e-12:
            best_feature = feature
            best_gain = information_gain
            best_split = (labels_0, labels_1)

    # 所有剩余特征的信息增益都不大于 0。
    if best_feature == -1:
        return majority_vote(labels)

    labels_0, labels_1 = best_split
    features_0 = [row for row in features if row[best_feature] == 0]
    features_1 = [row for row in features if row[best_feature] == 1]
    next_features = [f for f in available_features if f != best_feature]

    left = build_tree(features_0, labels_0, next_features)
    right = build_tree(features_1, labels_1, next_features)
    return best_feature, left, right


def predict(tree, sample):
    if isinstance(tree, int):
        return tree

    feature, left, right = tree
    if sample[feature] == 0:
        return predict(left, sample)
    return predict(right, sample)


def main():
    n, m = map(int, input().split())

    features = []
    labels = []
    for _ in range(n):
        row = list(map(int, input().split()))
        features.append(row[:3])
        labels.append(row[3])

    tree = build_tree(features, labels, [0, 1, 2])

    for _ in range(m):
        sample = list(map(int, input().split()))
        print(predict(tree, sample))


if __name__ == "__main__":
    main()
