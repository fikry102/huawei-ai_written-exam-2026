"""本地 Python 3 模拟判题器。

用法：
  python3 judge.py           # 判 solution1.py 与 solution2.py
  python3 judge.py --serve   # 启动网页与本地判题接口

测试与分数均为练习用途，不代表华为或 CodeFun 官方结果。
"""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import tempfile
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def kmedian_oracle(text: str) -> str:
    values = text.split()
    n, d, k = map(int, values[:3])
    pos = 3
    points = []
    for _ in range(n):
        points.append([float(value) for value in values[pos : pos + d]])
        pos += d

    centers = [point[:] for point in points[:k]]
    labels = [0] * n
    for _ in range(100):
        groups = [[] for _ in range(k)]
        for index, point in enumerate(points):
            distances = [
                sum(abs(point[j] - centers[c][j]) for j in range(d))
                for c in range(k)
            ]
            label = min(range(k), key=lambda c: (distances[c], c))
            labels[index] = label
            groups[label].append(index)

        updated = [center[:] for center in centers]
        for cluster, members in enumerate(groups):
            if not members:
                continue
            for feature in range(d):
                column = sorted(points[index][feature] for index in members)
                middle = len(column) // 2
                if len(column) % 2:
                    updated[cluster][feature] = column[middle]
                else:
                    updated[cluster][feature] = (
                        column[middle - 1] + column[middle]
                    ) / 2.0

        shift = sum(
            abs(updated[c][j] - centers[c][j])
            for c in range(k)
            for j in range(d)
        )
        centers = updated
        if shift < 1e-4:
            break

    inertia = sum(
        abs(points[i][j] - centers[labels[i]][j])
        for i in range(n)
        for j in range(d)
    )

    def f6(value: float) -> str:
        if abs(value) < 0.5e-9:
            value = 0.0
        return f"{value:.6f}"

    lines = [" ".join(map(str, labels))]
    lines.extend(" ".join(f6(value) for value in center) for center in centers)
    lines.append(f6(inertia))
    return "\n".join(lines)


def impurity_mass(rows):
    if not rows:
        return 0, 1
    ones = sum(row[4] for row in rows)
    zeros = len(rows) - ones
    return 2 * zeros * ones, len(rows)


def add_fraction(left, right):
    return left[0] * right[1] + right[0] * left[1], left[1] * right[1]


def fraction_less(left, right):
    return left[0] * right[1] < right[0] * left[1]


def cart_tree(rows):
    ones = sum(row[4] for row in rows)
    zeros = len(rows) - ones
    majority = int(ones > zeros)
    if len(rows) < 2 or ones == 0 or zeros == 0:
        return "leaf", majority

    best_score = impurity_mass(rows)
    best_feature = best_value = None
    for feature in range(4):
        for value in sorted({row[feature] for row in rows}):
            left = [row for row in rows if row[feature] == value]
            right = [row for row in rows if row[feature] != value]
            score = add_fraction(impurity_mass(left), impurity_mass(right))
            if fraction_less(score, best_score):
                best_score = score
                best_feature, best_value = feature, value

    if best_feature is None:
        return "leaf", majority
    left = [row for row in rows if row[best_feature] == best_value]
    right = [row for row in rows if row[best_feature] != best_value]
    return "node", best_feature, best_value, cart_tree(left), cart_tree(right)


def cart_oracle(text: str) -> str:
    data = list(map(int, text.split()))
    iterator = iter(data)
    n = next(iterator)
    train = [[next(iterator) for _ in range(5)] for _ in range(n)]
    tree = cart_tree(train)
    m = next(iterator)
    tests = [[next(iterator) for _ in range(4)] for _ in range(m)]

    def predict(sample):
        node = tree
        while node[0] == "node":
            _, feature, value, left, right = node
            node = left if sample[feature] == value else right
        return node[1]

    return " ".join(str(predict(sample)) for sample in tests)


P1_TESTS = [
    {
        "name": "公开样例 1",
        "score": 20,
        "input": "3 2 1\n2 8\n6 1\n4 5\n",
    },
    {
        "name": "公开样例 2",
        "score": 20,
        "input": "4 2 2\n1 1\n4 2\n5 5\n8 8\n",
    },
    {
        "name": "双簇与离群点",
        "score": 20,
        "input": "4 2 2\n0 0\n1 1\n2 2\n100 100\n",
    },
    {
        "name": "距离相同取小编号",
        "score": 15,
        "input": "3 1 2\n0\n2\n1\n",
    },
    {
        "name": "重复中心与空簇",
        "score": 20,
        "input": "3 1 2\n0\n0\n10\n",
    },
    {
        "name": "偶数中位数",
        "score": 20,
        "input": "6 2 2\n0 0\n10 10\n2 4\n4 2\n8 6\n12 8\n",
    },
    {
        "name": "负数与三维数据",
        "score": 35,
        "input": "7 3 3\n-5 -1 0\n5 1 2\n0 8 -3\n-4 -2 1\n6 2 3\n1 7 -2\n0 9 -4\n",
    },
]


P2_TESTS = [
    {
        "name": "公开样例 1",
        "score": 60,
        "input": """8
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
""",
    },
    {
        "name": "补充综合用例",
        "score": 60,
        "input": """20
0 0 0 1 1
0 0 1 0 0
0 1 0 0 0
0 1 1 1 1
0 2 0 1 1
1 0 0 0 0
1 0 1 1 1
1 1 0 1 1
1 1 1 0 0
1 2 1 0 0
2 0 0 1 1
2 0 1 0 1
2 1 0 0 0
2 1 1 1 1
2 2 0 0 0
3 0 0 0 0
3 0 1 1 0
3 1 0 1 1
3 1 1 0 0
3 2 0 1 0
10
1 1 1 0
2 0 0 1
3 2 0 1
0 0 0 1
1 2 1 0
2 1 0 0
3 0 1 1
0 1 1 1
1 0 0 0
2 2 0 0
""",
    },
    {
        "name": "纯标签叶子",
        "score": 30,
        "input": """4
0 0 0 0 1
1 1 0 1 1
2 2 1 0 1
3 0 1 1 1
3
0 2 1 0
1 0 0 1
3 2 0 0
""",
    },
    {
        "name": "多数票平局取 0",
        "score": 40,
        "input": """4
0 0 0 0 0
0 0 0 0 1
0 0 0 0 0
0 0 0 0 1
2
0 0 0 0
3 2 1 1
""",
    },
    {
        "name": "XOR 不强行分裂",
        "score": 40,
        "input": """4
0 0 0 0 0
0 1 0 0 1
1 0 0 0 1
1 1 0 0 0
4
0 0 0 0
0 1 0 0
1 0 0 0
1 1 0 0
""",
    },
    {
        "name": "切分同分规则",
        "score": 30,
        "input": """6
0 0 0 0 0
0 1 0 0 0
1 0 0 0 1
1 1 0 0 1
2 0 1 0 0
2 1 1 0 1
4
0 2 0 0
1 2 0 0
2 0 1 0
3 1 1 0
""",
    },
    {
        "name": "测试值未在训练集中出现",
        "score": 40,
        "input": """6
0 0 0 0 0
0 1 0 1 0
1 0 1 0 1
1 1 1 1 1
2 0 0 0 1
2 1 1 0 1
3
3 2 0 0
3 0 1 1
0 2 1 0
""",
    },
]


def prepare_tests(problem: int):
    source = P1_TESTS if problem == 1 else P2_TESTS
    oracle = kmedian_oracle if problem == 1 else cart_oracle
    return [dict(test, expected=oracle(test["input"])) for test in source]


def run_python(code_path: Path, input_text: str, timeout: float):
    started = time.perf_counter()
    try:
        result = subprocess.run(
            [sys.executable, str(code_path)],
            input=input_text,
            text=True,
            capture_output=True,
            timeout=timeout,
            cwd=str(code_path.parent),
        )
        elapsed = time.perf_counter() - started
        return result.returncode, result.stdout, result.stderr, elapsed
    except subprocess.TimeoutExpired as error:
        elapsed = time.perf_counter() - started
        stdout = error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
        return 124, stdout, stderr or "运行超时", elapsed


def compare_kmedian(actual: str, expected: str, input_text: str):
    first = input_text.split()
    n, d, k = map(int, first[:3])
    actual_lines = [line.strip() for line in actual.strip().splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected.strip().splitlines() if line.strip()]
    if len(actual_lines) != k + 2:
        return False, f"应输出 {k + 2} 行，实际为 {len(actual_lines)} 行"
    try:
        labels = list(map(int, actual_lines[0].split()))
        expected_labels = list(map(int, expected_lines[0].split()))
        if len(labels) != n or labels != expected_labels:
            return False, "簇编号不正确"
        for row in range(k):
            got = list(map(float, actual_lines[row + 1].split()))
            want = list(map(float, expected_lines[row + 1].split()))
            if len(got) != d or any(abs(a - b) > 5e-5 for a, b in zip(got, want)):
                return False, f"第 {row} 个中心不正确"
        got_inertia = float(actual_lines[-1])
        want_inertia = float(expected_lines[-1])
        if abs(got_inertia - want_inertia) > 5e-5:
            return False, "inertia 不正确"
    except (ValueError, OverflowError):
        return False, "输出格式无法解析"
    return True, "通过"


def compare_cart(actual: str, expected: str):
    try:
        got = list(map(int, actual.split()))
        want = list(map(int, expected.split()))
    except ValueError:
        return False, "输出应全部为整数标签"
    if got != want:
        return False, "预测标签不一致"
    return True, "通过"


def judge_code(problem: int, code: str):
    tests = prepare_tests(problem)
    maximum = sum(test["score"] for test in tests)
    score = 0
    details = []

    with tempfile.TemporaryDirectory(prefix="hw_ai_judge_") as folder:
        path = Path(folder) / "main.py"
        path.write_text(code, encoding="utf-8")
        for test in tests:
            returncode, stdout, stderr, elapsed = run_python(path, test["input"], 8.0)
            if returncode == 124:
                passed, message = False, "运行超时"
            elif returncode != 0:
                passed, message = False, "运行错误"
            elif problem == 1:
                passed, message = compare_kmedian(stdout, test["expected"], test["input"])
            else:
                passed, message = compare_cart(stdout, test["expected"])

            if passed:
                score += test["score"]
            details.append(
                {
                    "name": test["name"],
                    "passed": passed,
                    "points": test["score"] if passed else 0,
                    "maximum": test["score"],
                    "message": message,
                    "elapsed_ms": round(elapsed * 1000, 1),
                    "actual": stdout[:1600],
                    "expected": test["expected"][:1600],
                    "stderr": stderr[:1600],
                }
            )

    return {
        "problem": problem,
        "score": score,
        "maximum": maximum,
        "passed": sum(item["passed"] for item in details),
        "total": len(details),
        "details": details,
        "notice": "本地模拟分数，不是华为或 CodeFun 官方结果。",
    }


class JudgeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 2_000_000:
                self.send_json({"error": "请求过大"}, 413)
                return
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            code = str(payload.get("code", ""))
            if not code.strip():
                self.send_json({"error": "代码为空"}, 400)
                return

            if self.path == "/judge":
                problem = int(payload.get("problem", 0))
                if problem not in (1, 2):
                    self.send_json({"error": "未知题号"}, 400)
                    return
                self.send_json(judge_code(problem, code))
                return

            if self.path == "/run":
                input_text = str(payload.get("input", ""))
                expected = str(payload.get("expected", ""))
                with tempfile.TemporaryDirectory(prefix="hw_ai_run_") as folder:
                    path = Path(folder) / "main.py"
                    path.write_text(code, encoding="utf-8")
                    returncode, stdout, stderr, elapsed = run_python(path, input_text, 8.0)
                matched = None
                if expected.strip() and returncode == 0:
                    matched = stdout.split() == expected.split()
                self.send_json(
                    {
                        "returncode": returncode,
                        "stdout": stdout[:8000],
                        "stderr": stderr[:8000],
                        "elapsed_ms": round(elapsed * 1000, 1),
                        "matched": matched,
                    }
                )
                return

            self.send_json({"error": "接口不存在"}, 404)
        except Exception as error:  # 保持本地工具可诊断，不吞掉错误。
            self.send_json({"error": f"判题器异常：{error}"}, 500)

    def log_message(self, format, *args):
        if self.path.startswith(("/judge", "/run")):
            super().log_message(format, *args)


def cli_judge():
    overall = 0
    maximum = 0
    for problem in (1, 2):
        path = ROOT / f"solution{problem}.py"
        if not path.exists():
            print(f"[题目 {problem}] 找不到 {path.name}")
            continue
        result = judge_code(problem, path.read_text(encoding="utf-8"))
        overall += result["score"]
        maximum += result["maximum"]
        print(f"\n题目 {problem}: {result['score']} / {result['maximum']}")
        for item in result["details"]:
            mark = "通过" if item["passed"] else "失败"
            print(
                f"  [{mark}] {item['name']}  "
                f"{item['points']}/{item['maximum']}  {item['elapsed_ms']} ms"
            )
            if not item["passed"]:
                print(f"         {item['message']}")
                if item["stderr"]:
                    print("         " + item["stderr"].splitlines()[-1][:180])
    print(f"\n模拟总分: {overall} / {maximum}")
    print("说明：这是本地练习测试，不是华为或 CodeFun 官方评分。")


def main():
    parser = argparse.ArgumentParser(description="华为 AI 岗考前练习本地判题器")
    parser.add_argument("--serve", action="store_true", help="启动网页与判题服务")
    parser.add_argument("--port", type=int, default=8766, help="服务端口，默认 8766")
    args = parser.parse_args()
    if not args.serve:
        cli_judge()
        return

    server = ThreadingHTTPServer(("127.0.0.1", args.port), JudgeHandler)
    url = f"http://127.0.0.1:{args.port}/"
    print(f"考前练习网页已启动：{url}")
    print("按 Control+C 停止。判题器会执行你在网页中提交的 Python 代码。")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
