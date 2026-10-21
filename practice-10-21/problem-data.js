const problemDataComplete = {
  1: {
    sample: `3 2 1\n2 8\n6 1\n4 5\n`,
    expected: `0 0 0\n4.000000 5.000000\n11.000000\n`,
    starter: `import numpy as np\n\ndef solve(points, k):\n    # TODO: 按题面规则完成 K-Median\n    pass\n\ndef main():\n    n, d, k = map(int, input().split())\n    rows = []\n    for _ in range(n):\n        rows.append(list(map(float, input().split())))\n    points = np.array(rows)\n    solve(points, k)\n\nif __name__ == "__main__":\n    main()\n`,
    html: `<div class="problem-head"><div class="problem-meta"><span class="source">CodeFun P5612</span><span>华为</span><span>聚类 · 模拟</span></div><h1>P5612. 第2题-K-Median 聚类</h1><a href="https://codefun2000.com/ide/P5612?pset=hw" target="_blank">打开原题页面 ↗</a></div>
<p>K-Median 与 K-Means 的迭代框架相似，但距离使用曼哈顿距离，簇中心使用逐维中位数。给定 <i>n</i> 个 <i>d</i> 维样本，按照下面固定规则划分为 <i>k</i> 个簇。本题要求输出规定迭代流程的结果，不是另行寻找全局最优解。</p>
<h2>算法规则</h2>
<ol><li><b>初始化：</b>输入中的前 <i>k</i> 个样本依次作为编号 0 到 <i>k−1</i> 的初始中心。</li><li><b>分配：</b>计算每个样本到各中心的曼哈顿距离，把它分到最近的簇；距离相同时选择编号更小的簇。</li><li><b>更新：</b>非空簇对每个维度分别取中位数。样本数为奇数时取排序后的中间值；为偶数时取中间两个值的算术平均。空簇保持旧中心不变。</li><li><b>终止：</b>更新后，若所有簇、所有维度的新旧中心坐标绝对差之和小于 10<sup>−4</sup>，立即停止；否则继续，最多进行 100 轮。</li></ol>
<div class="formula">d(x,c)=∑<sub>j=1</sub><sup>d</sup>|x<sub>j</sub>−c<sub>j</sub>|</div>
<div class="formula">change=∑<sub>r=0</sub><sup>k−1</sup>∑<sub>j=1</sub><sup>d</sup>|c′<sub>r,j</sub>−c<sub>r,j</sub>|</div>
<p class="requirement"><b>输出时点：</b>输出最后一轮“分配”得到的簇编号和该轮“更新”后的中心。停止后不要再额外执行一次分配。inertia 也使用这组标签与更新后的中心计算。</p>
<div class="formula">inertia=∑<sub>i=1</sub><sup>n</sup>d(x<sub>i</sub>,c<sub>label<sub>i</sub></sub>)</div>
<h2>输入描述</h2><div class="io">第一行：n d k<br>接下来 n 行：每行 d 个浮点数，表示一个样本</div>
<ul><li>1 ≤ n ≤ 5000</li><li>1 ≤ d ≤ 20</li><li>1 ≤ k ≤ min(100,n)</li><li>每个特征值位于 [−10<sup>4</sup>,10<sup>4</sup>]</li></ul>
<h2>输出描述</h2><div class="io">第 1 行：n 个整数，依次为每个样本的簇编号<br>接下来 k 行：每行 d 个浮点数，按簇编号输出中心<br>最后 1 行：inertia</div>
<p>中心坐标和 inertia 均保留 6 位小数。结果为零时输出正零，避免出现 <code>-0.000000</code>。</p>
<h2>样例 1</h2><pre>输入
3 2 1
2 8
6 1
4 5

输出
0 0 0
4.000000 5.000000
11.000000</pre>
<p class="example-explain">三个样本都属于唯一的簇。两个维度的中位数分别为 4 和 5；到新中心的曼哈顿距离之和为 5+6+0=11。</p>
<h2>样例 2</h2><pre>输入
4 2 2
1 1
4 2
5 5
8 8

输出
0 0 1 1
2.500000 1.500000
6.500000 6.500000
10.000000</pre>`
  },
  2: {
    sample: `8\n0 0 0 0 0\n1 1 0 1 0\n2 2 0 0 0\n3 1 0 1 0\n0 1 1 0 1\n1 2 1 1 1\n2 0 1 0 1\n3 2 1 1 1\n4\n2 1 0 1\n0 2 1 0\n3 0 0 0\n1 1 1 1\n`,
    expected: `0 1 0 1\n`,
    starter: `def solve(train, tests):\n    # TODO: 建立 CART 二叉分类树并预测\n    pass\n\ndef main():\n    n = int(input())\n    train = []\n    for _ in range(n):\n        train.append(list(map(int, input().split())))\n    m = int(input())\n    tests = []\n    for _ in range(m):\n        tests.append(list(map(int, input().split())))\n    print(*solve(train, tests))\n\nif __name__ == "__main__":\n    main()\n`,
    html: `<div class="problem-head"><div class="problem-meta"><span class="source">CodeFun P5917</span><span>华为</span><span>决策树 · 递归</span></div><h1>P5917. 用 CART 分类树预测客户是否购房</h1><a href="https://codefun2000.com/ide/P5917?pset=hw" target="_blank">打开原题页面 ↗</a></div>
<p>根据历史客户记录构建一棵 CART 二叉分类树，再预测新客户是否购房。每条记录包含 4 个整数枚举特征和一个二分类标签。</p>
<h2>数据字段</h2><table class="spec-table"><thead><tr><th>列</th><th>含义</th><th>取值</th></tr></thead><tbody><tr><td>特征 1</td><td>年龄段</td><td>0：18–30 岁；1：31–40 岁；2：41–55 岁；3：56 岁及以上</td></tr><tr><td>特征 2</td><td>婚姻状况</td><td>0：单身；1：恋爱；2：已婚</td></tr><tr><td>特征 3</td><td>是否有房</td><td>0：无；1：有</td></tr><tr><td>特征 4</td><td>是否有工作</td><td>0：无；1：有</td></tr><tr><td>标签</td><td>购房结果</td><td>0：否；1：是</td></tr></tbody></table>
<h2>基尼指数</h2><p>设当前节点样本集合为 D，类别 0 和 1 的占比分别为 p<sub>0</sub>、p<sub>1</sub>：</p>
<div class="formula">Gini(D)=1−p<sub>0</sub><sup>2</sup>−p<sub>1</sub><sup>2</sup></div>
<p>对每个特征 A，把当前节点中该特征出现过的每个取值 v 都作为候选切分。A=v 的样本进入左子集 D<sub>L</sub>，A≠v 的样本进入右子集 D<sub>R</sub>：</p>
<div class="formula">Gini(D,A,v)=|D<sub>L</sub>|/|D| · Gini(D<sub>L</sub>)+|D<sub>R</sub>|/|D| · Gini(D<sub>R</sub>)</div>
<h2>建树规则</h2><ol><li>只接受加权基尼指数<b>严格小于</b>当前节点基尼指数的切分。</li><li>在可接受切分中选择加权基尼最小者；若并列，先选特征编号较小者；仍并列时选切分值较小者。</li><li>左子树接收 A=v 的样本，右子树接收 A≠v 的样本，然后递归建树。</li></ol>
<h2>停止与叶节点</h2><p>满足任意一项即停止：当前节点全部标签相同；当前节点样本数小于 2；不存在能严格降低基尼指数的切分。叶节点取样本中的多数标签，0 和 1 数量相同时取 0。</p>
<h2>预测</h2><p>从根节点开始，测试样本当前特征等于切分值时走左子树，否则走右子树，直到叶节点。</p>
<h2>输入描述</h2><div class="io">第一行：训练样本数 N<br>接下来 N 行：f1 f2 f3 f4 label<br>下一行：待预测样本数 M<br>接下来 M 行：f1 f2 f3 f4</div>
<p>4 ≤ N ≤ 20，1 ≤ M ≤ 10；所有输入均为整数枚举值。</p>
<h2>输出描述</h2><p>输出一行 M 个整数，依次表示每个测试样本的预测标签，以空格分隔。</p>
<h2>样例</h2><pre>输入
8
0 0 0 0 0
1 1 0 1 0
2 2 0 0 0
3 1 0 1 0
0 1 1 0 1
1 2 1 1 1
2 0 1 0 1
3 2 1 1 1
4
2 1 0 1
0 2 1 0
3 0 0 0
1 1 1 1

输出
0 1 0 1</pre>`
  }
};
