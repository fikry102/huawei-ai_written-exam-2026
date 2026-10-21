# Python 手写代码风格速查

适合机考、面试和日常算法代码。核心目标只有三个：**容易读、容易检查、少写错**。

## 一、基础格式

### 1. 普通赋值和运算符两边留空格

```python
count = 0
distance = x ** 2 + y ** 2
is_valid = left <= value < right
```

函数调用中的关键字参数不留空格：

```python
values.sort(reverse=True)
distances.sum(axis=-1)
np.array(rows, dtype=float)
```

记忆方法：

```python
x = 10       # 普通赋值
print(x=10)  # 关键字参数（仅用于说明格式）
```

### 2. 逗号后留空格，切片冒号两边不留空格

```python
point = [1, 2, 3]
solve(points, centers, labels)

points[:, None, :]
values[left:right]
```

### 3. 长表达式使用括号换行

```python
information_gain = (
    current_entropy
    - left_weight * left_entropy
    - right_weight * right_entropy
)
```

不要使用反斜杠强行续行。

## 二、命名

变量和函数使用小写加下划线：

```python
best_distance = float("inf")

def calculate_bic(sse, n):
    ...
```

常量使用大写：

```python
MAX_ITERATIONS = 100
EPSILON = 1e-8
```

优先使用有含义的名字：

```python
# 清楚
previous_labels = None

# 含义不明确
pre = None
```

算法中约定俗成的 `n`、`m`、`k`、`i`、`j` 可以保留。

## 三、组织代码

### 1. 一行只做一件主要事情

```python
# 推荐：可以逐步检查形状和结果
diff = points[:, None, :] - centers[None, :, :]
distances = (diff ** 2).sum(axis=-1)
labels = distances.argmin(axis=1)
```

避免全部挤在一行：

```python
labels = (((points[:, None, :] - centers[None, :, :]) ** 2).sum(axis=-1)).argmin(axis=1)
```

### 2. 一个函数只负责一类工作

把输入输出与算法分开：

```python
def solve(points, k):
    # 只处理算法
    ...


def main():
    n, k = map(int, input().split())

    points = []
    for _ in range(n):
        points.append(list(map(float, input().split())))

    answer = solve(points, k)
    print(answer)


if __name__ == "__main__":
    main()
```

### 3. 用提前结束减少嵌套

```python
for cluster in range(k):
    members = points[labels == cluster]
    if len(members) == 0:
        continue

    centers[cluster] = members.mean(axis=0)
```

## 四、注释

注释应说明代码背后的原因：

```python
# 使用稳定排序，保证第一维相同时维持原输入顺序。
order = np.argsort(points[:, 0], kind="stable")
```

不要重复代码已经表达清楚的动作：

```python
# 不推荐：给 count 加 1
count += 1
```

对于并列规则、精度处理、特殊边界等题目要求，建议保留简短注释。

## 五、NumPy 常用写法

### 1. 用 `axis=-1` 表示最后一个维度

```python
diff = points[:, None, :] - centers[None, :, :]
distances = (diff ** 2).sum(axis=-1)
```

如果 `diff.shape == (n, k, d)`，那么 `axis=-1` 就是沿特征维度 `d` 求和，结果形状为 `(n, k)`。

### 2. 不要直接判断 NumPy 数组真假

Python 列表可以直接判断：

```python
if not labels:
    ...
```

NumPy 数组需要明确说明判断方式：

```python
if len(array) == 0:
    ...

if np.any(mask):
    ...

if np.all(labels == previous_labels):
    ...
```

### 3. 让中间变量展示数组含义

```python
diff = points[:, None, :] - centers[None, :, :]
squared_diff = diff ** 2
distances = squared_diff.sum(axis=-1)
```

调试时可以临时查看：

```python
print(diff.shape)
print(distances.shape)
```

提交前记得删除调试输出。

## 六、输入与输出

### 1. 使用清楚、容易记忆的输入方式

```python
rows = []
for _ in range(n):
    rows.append(list(map(float, input().split())))

points = np.array(rows, dtype=float)
```

### 2. 使用 `*` 拆开序列输出

```python
labels = [0, 1, 1, 0]
print(*labels)
```

输出：

```text
0 1 1 0
```

### 3. 两种浮点格式化写法等价

```python
text_1 = f"{value:.2f}"
text_2 = format(value, ".2f")
```

两者都会返回保留两位小数的字符串：

```python
value = 3.14159

f"{value:.2f}"          # "3.14"
format(value, ".2f")   # "3.14"
```

区别主要在使用场景：

```python
# f-string 适合把变量放入完整文本
message = f"中心坐标为 {value:.2f}"

# format() 适合只转换一个值
formatted_value = format(value, ".2f")
```

列表推导式：

```python
formatted = [f"{value:.2f}" for value in center]
```

等价于：

```python
formatted = []
for value in center:
    formatted.append(format(value, ".2f"))
```

最后可以直接输出：

```python
print(*formatted)
```

## 七、机考提交前检查

不要从头到尾杂乱扫描，按下面四组依次检查。

### A. 输入与流程

- 第一行各变量的顺序是否读对；
- 后续需要读取的行数是否正确；
- `main()` 是否已经调用；
- 题目要求的所有步骤是否都执行了。

### B. 循环与条件

- `range()` 的终点是否需要包含；
- `<` 与 `<=`、`>` 与 `>=` 是否写对；
- `== 0` 与 `== 1` 是否存在复制后的笔误；
- 并列时取较小编号等规则是否实现。

### C. 边界与数值

- 空数组、空簇、单元素是否处理；
- `k=1`、`n=1` 等最小规模能否运行；
- `/` 与 `//` 是否使用正确；
- `log(0)`、除以零和浮点误差是否处理；
- 最大数据量下时间和内存是否可接受。

### D. 输出

- 输出行数、顺序和分隔符是否正确；
- 是否需要固定小数位；
- 是否可能出现 `-0.00`；
- 是否残留调试输出。

最后用题目样例手动走一遍关键步骤，再提交。
