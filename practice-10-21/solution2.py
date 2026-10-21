"""CART 分类树：Python 3 参考实现（仅使用标准库）。"""

def impurity_mass(rows):
    """返回 |D| * Gini(D)，以分数 (分子, 分母) 表示。"""
    if not rows:
        return 0, 1
    ones = sum(row[4] for row in rows)
    zeros = len(rows) - ones
    return 2 * zeros * ones, len(rows)


def add_fraction(left, right):
    return (
        left[0] * right[1] + right[0] * left[1],
        left[1] * right[1],
    )


def fraction_less(left, right):
    return left[0] * right[1] < right[0] * left[1]


def build_tree(rows):
    ones = sum(row[4] for row in rows)
    zeros = len(rows) - ones
    majority = 1 if ones > zeros else 0

    if len(rows) < 2 or ones == 0 or zeros == 0:
        return ("leaf", majority)

    best_score = impurity_mass(rows)
    best_feature = None
    best_value = None

    # 按特征编号、取值递增枚举；同分时不覆盖，自然满足平局规则。
    for feature in range(4):
        for value in sorted({row[feature] for row in rows}):
            left = [row for row in rows if row[feature] == value]
            right = [row for row in rows if row[feature] != value]
            score = add_fraction(impurity_mass(left), impurity_mass(right))

            if fraction_less(score, best_score):
                best_score = score
                best_feature = feature
                best_value = value

    # 题目要求基尼指数必须严格下降，否则直接成为叶子。
    if best_feature is None:
        return ("leaf", majority)

    left = [row for row in rows if row[best_feature] == best_value]
    right = [row for row in rows if row[best_feature] != best_value]
    return (
        "node",
        best_feature,
        best_value,
        build_tree(left),
        build_tree(right),
    )


def predict(tree, sample):
    while tree[0] == "node":
        _, feature, value, left, right = tree
        tree = left if sample[feature] == value else right
    return tree[1]


def classify(train, tests):
    tree = build_tree(train)
    return [predict(tree, sample) for sample in tests]


def main():
    n = int(input())

    train = []
    for _ in range(n):
        train.append(list(map(int, input().split())))

    m = int(input())

    tests = []
    for _ in range(m):
        tests.append(list(map(int, input().split())))

    print(*classify(train, tests))


if __name__ == "__main__":
    main()
