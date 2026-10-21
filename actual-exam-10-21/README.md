# Actual Exam on 2026-10-21

这是作者参加的 2026-10-21 华为 AI 方向实际考试整理，不是考前模拟卷。

- 20 道选择题：15 道单选、5 道不定项；
- 编程题 1：P5939，使用信息增益构建决策树；
- 编程题 2：P5940，自动确定簇数的 X-Means 聚类。

## 启动

```bash
python3 judge.py --serve
```

默认地址是 `http://127.0.0.1:8767/`。若端口被占用：

```bash
python3 judge.py --serve --port 9001
```

## 终端判题

```bash
python3 judge.py
```

`solution1.py` 是作者考试时通过版本的整理版，只调整了命名、排版、注释并修正了分组代码中的明显笔误。`solution2.py` 是在作者现场代码基础上补完的 NumPy 版本，因此需要：

```bash
python3 -m pip install numpy
```

## 文件

```text
actual-exam-10-21/
├── index.html
├── data.js
├── solution1.py
├── solution2.py
├── judge.py
└── README.md
```

本地测试点和分数只用于复盘，不代表官方隐藏测试结果。
