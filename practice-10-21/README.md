# Practice Before the 2026-10-21 Exam

这套题是在 2026-10-21 实际考试前制作的考前模拟题，并非当天真题。选择题以 10 月 10 日、10 月 14 日公开复盘主题为主；编程题为 CodeFun P5612（K-Median）和 P5917（CART）。

## 启动

```bash
python3 judge.py --serve
```

默认地址是 `http://127.0.0.1:8766/`。如果 8766 已被占用：

```bash
python3 judge.py --serve --port 9000
```

使用浏览器打开终端显示的新地址即可。网页会自动使用当前端口调用本地判题器。

## NumPy

`solution1.py` 是较短的 NumPy 写法，需要先安装 NumPy：

```bash
pip install numpy
```

若考试环境没有 NumPy，可改用 `solution1_without_numpy.py`。

## 终端判题

```bash
python3 judge.py
```

本地测试只用于练习，不是 CodeFun 或华为官方隐藏测试。
