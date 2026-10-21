const questionsSet2 = [
  {
    type: 'single', source: 'P5938 · 第 1 题',
    stem: '只有一个输出神经元的二分类模型，要把它的输出解释成“属于正类的概率”，最后一层应接哪个激活函数？',
    options: ['ReLU', 'Softmax', 'Sigmoid', 'Tanh'], answer: [2],
    explain: 'Sigmoid 把单个实数映射到 (0,1)，可直接解释为二分类中的正类概率。'
  },
  {
    type: 'single', source: 'P5938 · 第 2 题',
    stem: '回归任务中混进了少量误差极大的离群点，下面关于 MSE 与 MAE 的说法，正确的是？',
    options: ['绝对值损失 MAE 对离群点更敏感', '平方损失 MSE 对离群点更敏感', '平方损失 MSE 在误差为 0 处不可导', '绝对值损失 MAE 的收敛速度一般快于 MSE'], answer: [1],
    explain: 'MSE 会对误差平方，极端误差的影响会被显著放大；MAE 才是在 0 处不可导。'
  },
  {
    type: 'single', source: 'P5938 · 第 3 题',
    stem: '缩放点积注意力里把 QKᵀ 除以 √dₖ，这样做的目的是什么？',
    options: ['把单头计算拆成多头并行', '降低矩阵乘法的计算量', '增加模型可训练参数', '避免内积过大使 Softmax 饱和、梯度接近 0'], answer: [3],
    explain: '点积的尺度会随维度增大；除以 √dₖ 可控制方差，避免 Softmax 过度饱和。'
  },
  {
    type: 'single', source: 'P5938 · 第 4 题',
    stem: '有 6 个逐元素小算子串行执行。每次下发 GPU kernel 的固定开销为 8 μs，每个算子的纯执行时间为 2 μs。忽略访存优化，不融合耗时为 T₁，融合成一个 kernel 后为 T₂，则 T₁/T₂ 约为多少？',
    options: ['1.5 倍', '2 倍', '3 倍', '3.6 倍'], answer: [2],
    explain: 'T₁=6×(8+2)=60 μs；T₂=8+6×2=20 μs，所以 T₁/T₂=3。'
  },
  {
    type: 'single', source: 'P5938 · 第 5 题',
    stem: 'RAG 流程中，向量检索这一步最终要拿到的东西是什么？',
    options: ['对问题做分词并截断到固定长度', '从库里取出与问题语义最接近的文档片段', '由生成模型据此写出最终答案', '只要算出一个相似度分数就算完成'], answer: [1],
    explain: '向量检索负责返回相关文档片段；生成最终答案属于后续生成阶段。'
  },
  {
    type: 'single', source: 'P5938 · 第 6 题',
    stem: '用 Self-Instruct 方法自动构造指令数据，起步时需要准备的是什么？',
    options: ['一个已经对齐好的奖励模型', '一批带标注的测试集', '大规模无标注图像', '一小批人工编写的种子指令'], answer: [3],
    explain: 'Self-Instruct 从少量高质量种子指令出发，让模型扩展并筛选新的指令数据。'
  },
  {
    type: 'single', source: 'P5938 · 第 7 题',
    stem: '设 V 是 n 维向量空间，W 是 V 的子空间，则 dim W 最大能取到多少？',
    options: ['n−1', 'n', '1', '0'], answer: [1],
    explain: '子空间可以就是原空间本身，即 W=V，因此 dim W 最大为 n。'
  },
  {
    type: 'single', source: 'P5938 · 第 8 题',
    stem: '用 ViT 做视觉编码器时，常把切出的视觉 token 再做一次压缩，其主要目的是？',
    options: ['提升输入图像的原始分辨率', '让图像语义自动变准确', '降低后续计算量与显存占用', '增加视觉侧可训练参数量'], answer: [2],
    explain: '减少视觉 token 数量可直接降低后续注意力和多模态交互的计算、显存成本。'
  },
  {
    type: 'single', source: 'P5938 · 第 9 题',
    stem: '关于 t-SNE，下面说法正确的是？',
    options: ['它是非线性方法，主要保留高维数据的局部邻域结构', '它属于线性降维，结果对特征缩放敏感', '它计算量很小，百万级样本可以随意直接跑', '它每次运行结果完全随机，没有参考价值'], answer: [0],
    explain: 't-SNE 是强调局部邻域关系的非线性可视化方法；结果受超参数和随机初始化影响，但仍有分析价值。'
  },
  {
    type: 'single', source: 'P5938 · 第 10 题',
    stem: 'PagedAttention 缓解 KV Cache 显存碎片化的做法是？',
    options: ['把 KV Cache 压缩为 INT8，靠降位宽省显存', '丢弃部分早期 KV Cache，靠释放显存腾出空间', '每步重算 KV 向量，靠减少存储量避免碎片', '把 KV Cache 切成固定大小的页，让离散空闲块以页为单位使用'], answer: [3],
    explain: 'PagedAttention 借鉴虚拟内存分页，把 KV Cache 分成固定大小的块，避免要求物理显存连续。'
  },
  {
    type: 'single', source: 'P5938 · 第 11 题题意整理',
    stem: '关于 GPU 的 HBM 与片上 Shared Memory（SRAM）访问延迟，哪项说法正确？',
    options: ['两者访问延迟基本相同', 'Shared Memory / SRAM 的访问延迟远低于 HBM', 'Shared Memory / SRAM 的访问延迟高于 HBM', '两者只有写入延迟不同，读取延迟相同'], answer: [1],
    explain: 'SRAM 位于 GPU 片上，访问延迟远低于片外 HBM；分块复用正是许多 GPU 优化的基础。'
  },
  {
    type: 'single', source: 'P5938 · 第 12 题题意整理',
    stem: '下面哪一种回归指标或损失最容易被少量极端离群点显著影响？',
    options: ['MAE', 'Huber Loss', 'MSE', '中位数绝对误差'], answer: [2],
    explain: 'MSE 对误差平方，极端误差的权重增长最快。'
  },
  {
    type: 'single', source: 'P5938 · 第 13 题题意整理',
    stem: '把 Conv、BatchNorm、ReLU 融合成一个 CUDA kernel，最核心的硬件收益通常是什么？',
    options: ['减少浮点运算次数，降低计算功耗', '提高 GPU 的 occupancy，让并发线程更多', '突破算力上限，让计算密集型算子跑得更快', '减少中间结果往返 HBM 的重复读写，绕开内存墙'], answer: [3],
    explain: '算子融合让中间数据尽量留在寄存器或片上存储，主要减少昂贵的 HBM 往返。'
  },
  {
    type: 'single', source: 'P5938 · 第 14 题题意整理',
    stem: '构造合成训练数据时，哪种方案更有可能同时兼顾样本多样性与事实真实性？',
    options: ['先用大模型生成，再进行多轮人工校验和事实对齐', '只用固定模板批量填空', '随机拼接互不相关的语料', '只换成更小模型批量蒸馏且不做核验'], answer: [0],
    explain: '生成模型提供多样性，人工核验与事实对齐负责控制幻觉和事实错误。'
  },
  {
    type: 'single', source: 'P5938 · 第 15 题题意整理',
    stem: 'ROC 曲线的横轴和纵轴分别是什么？',
    options: ['横轴 FPR，纵轴 TPR', '横轴 TPR，纵轴 Precision', '横轴 Recall，纵轴 Specificity', '横轴 F1，纵轴 Accuracy'], answer: [0],
    explain: 'ROC 横轴为假正例率 FPR，纵轴为真正例率 TPR（也就是 Recall）。'
  },
  {
    type: 'multi', source: 'P5938 · 第 16 题题意整理',
    stem: '某模型训练准确率 94%，测试准确率 57%，下列哪些措施通常有助于缓解该问题？',
    options: ['加入 Dropout', '使用 L2 正则化', '继续增加网络深度', '扩充训练数据', '进行特征选择，删除冗余特征'], answer: [0, 1, 3, 4],
    explain: '这是明显过拟合。Dropout、L2、更多数据和移除冗余特征均可能改善；继续加深通常会增加容量。'
  },
  {
    type: 'multi', source: 'P5938 · 第 17 题题意整理',
    stem: '关于损失函数、经验风险和结构风险，下列说法正确的有？',
    options: ['结构风险通常可写成经验风险加正则项', '经验风险是模型在总体数据分布上的期望损失', '不同损失函数的光滑性和凸性会影响适用的优化方法', '损失函数的选择会影响最终解与泛化表现'], answer: [0, 2, 3],
    explain: '经验风险是有限训练样本上的平均损失；总体分布上的期望是期望风险。其余三项成立。'
  },
  {
    type: 'multi', source: 'P5938 · 第 18 题题意整理',
    stem: '有限精度浮点计算中，下列哪些做法通常有助于控制舍入误差？',
    options: ['避免两个非常接近的数直接相减', '避免除以绝对值极小的数', '适当合并可合并的运算，减少中间舍入', '累加不同数量级的数时优先从较小量级开始'], answer: [0, 1, 2, 3],
    explain: '四项分别针对灾难性消去、误差放大、中间舍入次数，以及小量被大量吞没的问题。'
  },
  {
    type: 'multi', source: 'P5938 · 第 19 题题意整理',
    stem: '关于多模态模型中视觉—文本注意力的组织方式，下列说法正确的有？',
    options: ['先在视觉侧聚合可减少送入文本侧的视觉 token，但过早聚合可能丢失与文本相关的细粒度信息', 'Q-Former 可用少量可学习 Query 压缩大量视觉 token', '只要使用交叉注意力，梯度就一定无法影响视觉表示', '视觉与文本 token 拼接后统一做自注意力可充分双向交互；但视觉 token 往往更多，文本信号可能被视觉噪声淹没，推理时仍需加载全部视觉 token'], answer: [0, 1, 3],
    explain: '除非显式冻结视觉编码器，否则交叉注意力的梯度仍可能传回视觉侧，因此 C 错误。'
  },
  {
    type: 'multi', source: 'P5938 · 第 20 题题意整理',
    stem: '关于 Transformer 前向传播中的常见组件，下列说法正确的有？',
    options: ['Embedding 将离散 token ID 映射为连续向量', 'FFN 只负责提取局部位置特征，不进行特征维变换', '自注意力可建模不同位置 token 之间的依赖', 'SwiGLU 提供带门控的非线性变换', 'RMSNorm 不计算均值，通常比 LayerNorm 更轻量'], answer: [0, 2, 3, 4],
    explain: 'FFN 对每个位置的特征维进行非线性变换，不能概括成“只提取局部特征”；其余四项正确。'
  }
];

const problemDataSet2 = {
  1: {
    sample: `5 5
1 0 1 1
1 1 0 1
0 0 1 0
0 1 1 1
1 0 0 0
1 0 1
1 1 0
0 0 1
0 1 1
1 0 0
`,
    expected: `1
1
0
1
0
`,
    starter: `def solve(train, tests):
    # TODO: 构建信息增益决策树并预测
    pass


def main():
    n, m = map(int, input().split())
    train = [list(map(int, input().split())) for _ in range(n)]
    tests = [list(map(int, input().split())) for _ in range(m)]
    for answer in solve(train, tests):
        print(answer)


if __name__ == "__main__":
    main()
`,
    html: `<div class="problem-head"><div class="problem-meta"><span class="source">CodeFun P5939</span><span>难度 5</span><span>150 分</span></div><h1>第2题－游戏皮肤推荐：用决策树判断玩家购买意向</h1><a href="https://codefun2000.com/ide/P5939?pset=hw" target="_blank" rel="noreferrer">打开 CodeFun 原页面 ↗</a></div>
<p>一款 5v5 竞技手游每逢版本更新都会上新皮肤。商店推荐位如果不加区分地把所有皮肤推给所有玩家，玩家划得累，购买转化率也上不去。项目组的做法是：先从历史数据里攒一批“看过页面、最终买没买”的记录，用决策树把购买意向学出来，再把新玩家逐条喂进这棵树做预测。</p>
<p>购买意向只用三个布尔特征描述，编号为 0、1、2：</p>
<table class="spec-table"><thead><tr><th>特征编号</th><th>含义</th><th>取值</th></tr></thead><tbody><tr><td>0</td><td>是否 VIP 会员（含月卡）</td><td>0 表示否，1 表示是</td></tr><tr><td>1</td><td>是否买过该英雄的皮肤</td><td>0 表示否，1 表示是</td></tr><tr><td>2</td><td>是否把该英雄打上过最高段位</td><td>0 表示否，1 表示是</td></tr></tbody></table>
<p>训练样本的类别也只有两种：0 表示不购买（不推荐），1 表示购买（推荐）。</p>
<h2>决策树的构建规则</h2>
<h3>熵</h3><p>对只含两类的样本集 S，记类别 0、1 的样本占比为 p₀、p₁（p₀+p₁=1），熵定义为：</p><div class="formula">$$H(S)=-\\sum_{x\\in\\{0,1\\}}p_x\\log_2p_x$$</div><p>其中 p<sub>x</sub>=0 的项按 0·log₂0=0 处理。</p>
<h3>条件熵与信息增益</h3><p>用特征 A 把 S 分成 S₀（取值为 0）与 S₁（取值为 1）。分裂后的条件熵是两棵子树熵按样本量加权平均：</p><div class="formula">$$H(S\\mid A)=\\sum_{v\\in\\{0,1\\}}\\frac{|S_v|}{|S|}H(S_v)$$$$\\operatorname{IG}(S,A)=H(S)-H(S\\mid A)$$</div>
<h3>节点分裂</h3><p>从根节点开始递归建树。在当前节点上，对<strong>尚未出现在从根到该节点路径上</strong>的特征逐个计算信息增益，取增益最大的特征作为分裂特征；如果多个特征的增益并列最大，取编号最小者。特征值为 0 的样本进入左子树，值为 1 的进入右子树。</p><p>某个特征一旦在某条路径上用过，就不能在该路径的下层节点再次使用；但在另一条分支上仍然可用。</p>
<h3>终止条件</h3><p>满足下列任意一条，当前节点成为叶节点：</p><ol><li>节点内所有样本的类别相同；</li><li>三个特征都已经在从根到当前节点的路径上出现；</li><li>所有尚未使用特征的信息增益都不大于 0。</li></ol><p>条件 1 的叶节点类别就是样本类别；条件 2、3 使用多数表决：类别 1 更多取 1，类别 0 更多取 0，数量相等取 0。</p>
<h3>预测</h3><p>对一条待预测样本，从根节点出发，读取当前节点分裂特征的取值：0 走左子树，1 走右子树，直到叶节点并输出其类别。</p>
<h2>输入格式</h2><ul><li>第一行：两个整数 N、M，分别表示训练样本数与待预测样本数。</li><li>第 2 至 N+1 行：每行 4 个整数，前三个是特征 0、1、2 的取值，第四个是类别。</li><li>第 N+2 至 N+M+1 行：每行 3 个整数，是待预测样本的三个特征。</li></ul><p>下面这段输入表示 4 条训练样本与 4 条待预测样本：</p><pre>4 4
1 1 1 1
1 1 0 0
1 1 1 0
0 0 0 0
1 1 1
1 1 0
1 0 1
0 0 1</pre>
<h2>输出格式</h2><p>输出 M 行，每行一个整数 0 或 1，按输入顺序给出每条待预测样本的类别。不要输出多余空格或空行。</p>
<h2>数据范围</h2><ul class="limits"><li>1 ≤ N ≤ 10⁵，1 ≤ M ≤ 10⁵；</li><li>所有特征取值与类别均为 0 或 1；</li><li>需要比较信息增益时，真正并列的增益在数学上完全相等；若不并列，最大值与次大值之差不少于 10⁻³。</li></ul>
<h2>解答要求</h2><div class="requirement"><span>时间限制：C/C++ 1000 ms，其他语言 2000 ms</span><span>内存限制：C/C++ 512 MB，其他语言 1024 MB</span></div>
<h2>样例 1</h2><pre>输入
5 5
1 0 1 1
1 1 0 1
0 0 1 0
0 1 1 1
1 0 0 0
1 0 1
1 1 0
0 0 1
0 1 1
1 0 0

输出
1
1
0
1
0</pre><div class="example-explain"><strong>样例解释：</strong>训练集类别 0 有 2 条、类别 1 有 3 条，H(S)≈0.9710。三个特征的信息增益约为 0.0200、0.4200、0.0200，因此根节点选择特征 1。特征 1=0 的一侧中，特征 0 与 2 的增益并列（约 0.2516），按规则选择编号较小的特征 0；必要时再用特征 2。特征 1=1 的一侧类别全为 1。五条测试样本最终输出 1、1、0、1、0。</div>
<h2>样例 2</h2><pre>输入
7 5
0 1 0 1
0 0 1 0
0 1 1 1
0 0 0 0
1 0 0 0
1 0 1 1
1 1 0 0
0 0 0
1 1 1
1 0 1
0 1 0
1 1 0

输出
0
0
1
1
0</pre><div class="example-explain"><strong>样例解释：</strong>训练集类别 0 有 4 条、类别 1 有 3 条，H(S)≈0.9852。特征 0 的增益约为 0.0202，特征 1 与特征 2 的增益并列最大（约 0.1281），所以根节点选择编号更小的特征 1。特征 1=1 分支中，特征 0、2 的增益约为 0.9183、0.2516；特征 1=0 分支中，特征 0、2 的增益并列约为 0.3113。最终输出 0、0、1、1、0。</div>
<h2>提示</h2><table class="tip-table"><thead><tr><th>要点</th><th>说明</th></tr></thead><tbody><tr><td>并列取小</td><td>只在数学上严格相等时按编号取小；不要用过大的浮点容差制造“伪并列”。</td></tr><tr><td>特征按路径禁用</td><td>禁用范围是根到当前节点的一条路径，不是整棵树；另一条分支仍可再次使用同一特征。</td></tr><tr><td>增益为 0</td><td>某特征在节点内取值全同，或分裂后两侧类别分布相同，信息增益为 0，不能作为分裂特征。</td></tr><tr><td>表决并列</td><td>多数表决时两类样本数量相同，选择类别 0。</td></tr><tr><td>样本不会分空</td><td>只有增益大于 0 的特征才会被选中，因此被选特征的两个取值都出现过，左右子树不会为空。</td></tr></tbody></table>`
  },
  2: {
    sample: `12 2
1.0 1.0
15.0 12.0
7.0 6.0
2.0 1.0
8.0 6.0
17.0 12.0
1.0 2.0
7.0 7.0
15.0 14.0
2.0 2.0
17.0 14.0
8.0 7.0
1 5
`,
    expected: `3
1.50 1.50
7.50 6.50
16.00 13.00
0 2 1 0 1 2 0 1 2 0 2 1
`,
    starter: `def xmeans(points, k_min, k_max):
    # TODO: 枚举 K，运行确定性 K-Means，合并近中心并计算 BIC
    pass


def main():
    n, d = map(int, input().split())
    points = [list(map(float, input().split())) for _ in range(n)]
    k_min, k_max = map(int, input().split())
    centers, labels = xmeans(points, k_min, k_max)
    print(len(centers))
    for center in centers:
        print(*(f"{value:.2f}" for value in center))
    print(*labels)


if __name__ == "__main__":
    main()
`,
    html: `<div class="problem-head"><div class="problem-meta"><span class="source">CodeFun P5940</span><span>难度 5</span><span>300 分</span></div><h1>第3题－自动确定簇数的 X-Means 聚类</h1><a href="https://codefun2000.com/ide/P5940?pset=hw" target="_blank" rel="noreferrer">打开 CodeFun 原页面 ↗</a></div>
<p>做用户分群、图像分割或测点归组时，往往事先不知道应该分成多少组。K-Means 需要人工给出簇数 K；X-Means 则在外层使用 BIC（贝叶斯信息准则），从候选区间中自动选择 K。</p><p>给定 N 个 d 维数据点与候选区间 [K<sub>min</sub>, K<sub>max</sub>]，请确定最优簇数，输出各簇中心以及每个点的簇标签。</p>
<h2>算法介绍</h2>
<h3>K-Means 基础</h3><p>K-Means 将 N 个点划分为 K 个簇，目标是减小簇内误差平方和 SSE：</p><div class="formula">$$\\operatorname{SSE}=\\sum_{i=1}^{N}\\left\\|x_i-\\mu_{c(i)}\\right\\|^2$$</div><p>也就是把每个点到其所属簇中心的欧氏距离平方全部累加。</p>
<p>每个候选 K 按下面的确定性流程运行：</p><ol><li><strong>初始化：</strong>K=1 时取全体点的逐维均值；K&gt;1 时按第一维坐标稳定升序排序，对 i=0,…,K−1，选择排序后下标 floor(i·(N−1)/(K−1)) 的点作为第 i 个中心。不得随机初始化。</li><li><strong>分配：</strong>把每个点分到欧氏距离平方最小的中心；距离相同选择编号较小的簇。</li><li><strong>更新：</strong>非空簇的中心改为簇内点的逐维均值；空簇保留原中心。</li><li><strong>停止：</strong>某轮分配得到的全部标签与上一轮一致，或已完成 100 轮时停止。即使标签不变，也要完成本轮中心更新。</li></ol>
<h3>合并重合中心</h3><p>K-Means 结束后，若任意两个中心的距离平方小于 10⁻⁴，则把它们合并。合并具有传递性：A 与 B 接近、B 与 C 接近时，三者属于同一连通分量。合并后的中心取该分量所含全部样本的逐维均值，并重新映射标签；此时的簇数记为 K<sub>actual</sub>。</p>
<h3>BIC（贝叶斯信息准则）</h3><p>BIC 同时衡量拟合误差与模型复杂度。仅当 SSE=0 时，先把 SSE 替换为 10⁻⁸，以避免出现 ln(0)；SSE&gt;0 时直接使用原值：</p><div class="formula">$$SSE'=\\begin{cases}10^{-8},&SSE=0\\\\SSE,&SSE>0\\end{cases}$$$$\\operatorname{BIC}=N\\ln\\left(\\frac{SSE'}{N}\\right)+p\\ln(N)$$$$p=K_{\\mathrm{actual}}(d+1)$$</div>
<table class="spec-table"><thead><tr><th>符号</th><th>含义</th></tr></thead><tbody><tr><td>N</td><td>数据点总数</td></tr><tr><td>SSE</td><td>所有点到最终所属中心的误差平方和</td></tr><tr><td>p</td><td>K<sub>actual</sub> 个 d 维中心，加上每簇 1 个权重参数</td></tr><tr><td>K<sub>actual</sub></td><td>重合中心完成合并后的实际簇数</td></tr><tr><td>SSE′</td><td>SSE 为 0 时取 10⁻⁸，否则保持原 SSE</td></tr></tbody></table>
<ul><li>BIC 越小越好；第一项偏好较小 SSE，第二项惩罚过多的簇。</li><li>如果多个候选 K 得到相同 BIC，选择<strong>枚举值 K 较小</strong>的方案。</li><li>只有 SSE=0 时才使用 10⁻⁸；非零 SSE 不额外加 ε。</li></ul>
<h3>X-Means 流程</h3><pre>输入：数据集 X，簇数区间 [Kmin, Kmax]

先令 Kmax = min(Kmax, N)
若 Kmin &gt; Kmax，则令 Kmin = Kmax

对 K = Kmin, Kmin+1, ..., Kmax：
    执行确定性 K-Means
    传递地合并距离平方 &lt; 1e-4 的中心
    重新计算中心、标签、SSE 与实际簇数
    计算 BIC

选择 BIC 最小的方案</pre>
<h3>最终编号</h3><p>对所选方案的中心按全部坐标进行字典序升序排序：先比较第一维，相同再比较第二维，依此类推。排序后重新编号为 0、1、2、…，并同步重映射所有标签。</p>
<h2>数据范围</h2><ul class="limits"><li>1 ≤ N ≤ 2000；</li><li>1 ≤ d ≤ 10；</li><li>每个坐标的绝对值不超过 10³；</li><li>公开题面给出的基础范围为 1 ≤ K<sub>min</sub> ≤ K<sub>max</sub> ≤ N；</li><li>按题目提示，实现中仍须先执行 K<sub>max</sub>=min(K<sub>max</sub>,N)，截断后若 K<sub>min</sub>&gt;K<sub>max</sub>，则令 K<sub>min</sub>=K<sub>max</sub>。</li></ul>
<h2>解答要求</h2><div class="requirement"><span>时间限制：C/C++ 1000 ms，其他语言 2000 ms</span><span>内存限制：C/C++ 512 MB，其他语言 1024 MB</span></div>
<h2>输入</h2><ul><li>第一行：两个整数 N、d，分别表示数据点数量和维度。</li><li>接下来 N 行：每行 d 个浮点数，表示一个数据点。</li><li>最后一行：两个整数 K<sub>min</sub>、K<sub>max</sub>。</li></ul>
<h2>输出</h2><ul><li>第一行输出最终簇数 K。</li><li>接下来 K 行，每行输出一个 d 维中心，各坐标保留两位小数。</li><li>最后一行输出 N 个整数标签，按原始输入顺序排列，取值范围为 0 到 K−1。</li><li>若无法聚类，输出 0。</li></ul><p>若坐标四舍五入后出现 −0.00，必须输出 0.00。</p>
<h2>样例 1</h2><pre>输入
12 2
1.0 1.0
15.0 12.0
7.0 6.0
2.0 1.0
8.0 6.0
17.0 12.0
1.0 2.0
7.0 7.0
15.0 14.0
2.0 2.0
17.0 14.0
8.0 7.0
1 5

输出
3
1.50 1.50
7.50 6.50
16.00 13.00
0 2 1 0 1 2 0 1 2 0 2 1</pre><div class="example-explain"><strong>样例解释：</strong>12 个二维点形成三组，每组 4 个点，中心分别为 (1.50,1.50)、(7.50,6.50)、(16.00,13.00)。枚举 K=1…5 得到的 BIC 依次约为 56.29、43.86、22.36、29.13、32.90，因此选择 K=3。中心按字典序编号后，再按原输入顺序得到最后一行标签。</div>
<h2>样例 2</h2><pre>输入
8 2
4.0 2.0
20.0 10.0
5.0 2.0
22.0 10.0
4.0 3.0
20.0 12.0
5.0 3.0
22.0 12.0
1 3

输出
2
4.50 2.50
21.00 11.00
0 1 0 1 0 1 0 1</pre><div class="example-explain"><strong>样例解释：</strong>8 个点分成左右两组，均值分别为 (4.50,2.50) 与 (21.00,11.00)。K=1、2、3 时 BIC 约为 42.00、14.26、19.95，故选择 K=2；字典序编号后左侧为 0、右侧为 1。</div>
<h2>提示</h2><table class="tip-table"><thead><tr><th>要点</th><th>说明</th></tr></thead><tbody><tr><td>确定性初始化</td><td>按第一维稳定排序并按 floor(i·(N−1)/(K−1)) 取点；K=1 取全体均值，不得随机初始化。</td></tr><tr><td>收敛条件</td><td>一轮结束后标签完全不变即收敛；最多 100 轮。</td></tr><tr><td>标签排序</td><td>输出前按中心全部坐标的字典序重新编号，保证结果唯一。</td></tr><tr><td>Kmax 截断</td><td>先执行 Kmax=min(Kmax,N)；若 Kmin&gt;Kmax，则令 Kmin=Kmax。</td></tr><tr><td>SSE 为零</td><td>仅当 SSE=0 时将其替换为 1e-8；SSE&gt;0 时直接计算 SSE/N。</td></tr><tr><td>空簇处理</td><td>某簇没有样本时保留原中心，不参与均值更新。</td></tr><tr><td>重合中心合并</td><td>中心距离平方 &lt;1e-4 时传递合并；合并后的中心取全部归属样本的均值。</td></tr><tr><td>Kmin=Kmax</td><td>只对这个固定 K 运行一次 K-Means，无需枚举其他值。</td></tr><tr><td>距离相同</td><td>点到多个中心等距时，选择编号最小的簇。</td></tr><tr><td>零的符号</td><td>四舍五入得到 −0.00 时输出 0.00。</td></tr></tbody></table>`
  }
};
