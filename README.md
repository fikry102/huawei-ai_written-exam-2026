# Huawei AI Written Exam 2026

这是一个用于整理华为 AI 方向笔试材料的本地项目，包含一套考前练习和一套 2026-10-21 实际考试整理。两者已按背景分开，避免把实际考试误写成模拟题。

## 目录

| 目录 | 性质 | 内容 | 默认端口 |
| --- | --- | --- | --- |
| `practice-10-21` | 实际考试前制作的练习 | 20 道选择题、P5612 K-Median、P5917 CART | 8766 |
| `actual-exam-10-21` | 2026-10-21 实际考试整理 | 20 道选择题、P5939 决策树、P5940 X-Means | 8767 |

## 启动网页

进入想做的一套题，再启动本地网页：

```bash
cd practice-10-21
python3 judge.py --serve
```

或：

```bash
cd actual-exam-10-21
python3 judge.py --serve
```

如果提示端口已被占用，可以指定另一个端口，例如：

```bash
python3 judge.py --serve --port 9000
```

随后打开终端中显示的地址，例如 `http://127.0.0.1:9000/`。网页中的选择题、代码草稿和倒计时保存在浏览器本地。

## Python 与 NumPy

建议使用 Python 3.9 或更高版本。第一套的 `solution1.py` 需要使用 NumPy：

```bash
pip install numpy
```

第一套同时提供不依赖第三方库的 `solution1_without_numpy.py`。

## 说明

- 本项目不是华为、牛客或 CodeFun 官方题库；
- 实际考试部分来自公开题面整理，可能与官方测试和排版存在差异；
- 本地测试点和估算分数不代表官方评测结果；
- 公开题目的著作权归原作者和原平台所有，页面保留原题链接。

## Star History

<a href="https://www.star-history.com/?repos=fikry102%2Fhuawei-ai_written-exam-2026&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=fikry102/huawei-ai_written-exam-2026&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=fikry102/huawei-ai_written-exam-2026&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=fikry102/huawei-ai_written-exam-2026&type=date&legend=top-left" />
 </picture>
</a>
