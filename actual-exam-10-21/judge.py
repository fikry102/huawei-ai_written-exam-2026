"""第二套本地 Python 3 模拟判题器。

用法：
  python3 judge.py           # 判 solution1.py 与 solution2.py
  python3 judge.py --serve   # 在 8767 端口启动网页与判题接口

分数和补充测试仅供练习，不代表华为或 CodeFun 官方结果。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parent


P1_TESTS = [
    {
        "name": "公开样例 1",
        "score": 40,
        "input": """5 5
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
""",
        "expected": "1\n1\n0\n1\n0\n",
    },
    {
        "name": "公开样例 2",
        "score": 35,
        "input": """7 5
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
""",
        "expected": "0\n0\n1\n1\n0\n",
    },
    {
        "name": "纯标签叶节点",
        "score": 20,
        "input": """3 2
0 0 0 1
1 0 1 1
0 1 1 1
0 0 1
1 1 0
""",
        "expected": "1\n1\n",
    },
    {
        "name": "零增益停止与平局取 0",
        "score": 25,
        "input": """4 3
0 0 0 0
0 1 0 1
1 0 0 1
1 1 0 0
0 0 1
1 1 1
1 0 0
""",
        "expected": "0\n0\n0\n",
    },
    {
        "name": "分支独立使用特征",
        "score": 30,
        "input": """6 4
0 0 0 0
0 0 1 0
0 1 0 1
1 0 0 1
1 1 0 0
1 1 1 1
0 0 0
0 1 1
1 0 1
1 1 0
""",
        "expected": "0\n1\n1\n0\n",
    },
]


P2_TESTS = [
    {
        "name": "公开样例 1",
        "score": 60,
        "input": """12 2
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
""",
        "expected": """3
1.50 1.50
7.50 6.50
16.00 13.00
0 2 1 0 1 2 0 1 2 0 2 1
""",
    },
    {
        "name": "公开样例 2",
        "score": 50,
        "input": """8 2
4.0 2.0
20.0 10.0
5.0 2.0
22.0 10.0
4.0 3.0
20.0 12.0
5.0 3.0
22.0 12.0
1 3
""",
        "expected": """2
4.50 2.50
21.00 11.00
0 1 0 1 0 1 0 1
""",
    },
    {
        "name": "只枚举一个簇",
        "score": 45,
        "input": """4 2
0 0
2 2
4 4
6 6
1 1
""",
        "expected": """1
3.00 3.00
0 0 0 0
""",
    },
    {
        "name": "重复点与中心排序",
        "score": 55,
        "input": """6 2
0 0
0 0
10 10
10 10
20 20
20 20
2 4
""",
        "expected": """3
0.00 0.00
10.00 10.00
20.00 20.00
0 0 1 1 2 2
""",
    },
    {
        "name": "Kmax 截断与 Kmin 修正",
        "score": 55,
        "input": """3 1
0
10
20
5 6
""",
        "expected": """3
0.00
10.00
20.00
0 1 2
""",
    },
    {
        "name": "空簇保留原中心",
        "score": 35,
        "input": """6 1
-67
8
-81
4
-73
75
3 3
""",
        "expected": """3
-73.67
-45.33
29.00
0 2 0 2 0 2
""",
    },
]


def normalize(text: str) -> str:
    return " ".join(text.split())


def run_python(code_path: Path, input_text: str, timeout: float = 8.0):
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
        return (
            result.returncode,
            result.stdout,
            result.stderr,
            time.perf_counter() - started,
        )
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
        return 124, stdout, stderr or "运行超时", time.perf_counter() - started


def compare_xmeans(actual: str, expected: str, input_text: str):
    actual_lines = [line.strip() for line in actual.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected.splitlines() if line.strip()]
    try:
        expected_k = int(expected_lines[0])
        actual_k = int(actual_lines[0])
        if actual_k != expected_k:
            return False, f"最终簇数应为 {expected_k}，实际为 {actual_k}"
        if len(actual_lines) != actual_k + 2:
            return False, f"应输出 {actual_k + 2} 行，实际为 {len(actual_lines)} 行"

        dimension = int(input_text.split()[1])
        for row in range(actual_k):
            got = list(map(float, actual_lines[row + 1].split()))
            want = list(map(float, expected_lines[row + 1].split()))
            if len(got) != dimension:
                return False, f"第 {row} 个中心维数不正确"
            if any(abs(a - b) > 5e-3 for a, b in zip(got, want)):
                return False, f"第 {row} 个中心不正确"

        got_labels = list(map(int, actual_lines[-1].split()))
        want_labels = list(map(int, expected_lines[-1].split()))
        if got_labels != want_labels:
            return False, "最终标签不正确"
    except (ValueError, IndexError, OverflowError):
        return False, "输出格式无法解析"
    return True, "通过"


def judge_code(problem: int, code: str):
    tests = P1_TESTS if problem == 1 else P2_TESTS
    maximum = sum(test["score"] for test in tests)
    score = 0
    details = []

    with tempfile.TemporaryDirectory(prefix="hw_ai_set2_") as folder:
        path = Path(folder) / "main.py"
        path.write_text(code, encoding="utf-8")

        for test in tests:
            returncode, stdout, stderr, elapsed = run_python(path, test["input"])
            if returncode == 124:
                passed, message = False, "运行超时"
            elif returncode != 0:
                passed, message = False, "运行错误"
            elif problem == 1:
                passed = normalize(stdout) == normalize(test["expected"])
                message = "通过" if passed else "预测标签不一致"
            else:
                passed, message = compare_xmeans(stdout, test["expected"], test["input"])

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
        "notice": "本地练习测试，不是华为或 CodeFun 官方评分。",
    }


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
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
                raise ValueError("请求内容过大")
            data = json.loads(self.rfile.read(length) or b"{}")

            if self.path == "/run":
                code = str(data.get("code", ""))
                input_text = str(data.get("input", ""))
                expected = str(data.get("expected", ""))
                with tempfile.TemporaryDirectory(prefix="hw_ai_run_") as folder:
                    path = Path(folder) / "main.py"
                    path.write_text(code, encoding="utf-8")
                    returncode, stdout, stderr, elapsed = run_python(path, input_text)
                matched = None if not expected.strip() else normalize(stdout) == normalize(expected)
                self.send_json(
                    {
                        "returncode": returncode,
                        "stdout": stdout[:10000],
                        "stderr": stderr[:10000],
                        "elapsed_ms": round(elapsed * 1000, 1),
                        "matched": matched,
                    }
                )
                return

            if self.path == "/judge":
                problem = int(data.get("problem", 0))
                if problem not in (1, 2):
                    raise ValueError("题号必须为 1 或 2")
                self.send_json(judge_code(problem, str(data.get("code", ""))))
                return

            self.send_json({"error": "未知接口"}, 404)
        except Exception as error:
            self.send_json({"error": str(error)}, 400)


def print_result(result):
    print(f"\n题目 {result['problem']}: {result['score']} / {result['maximum']}")
    for item in result["details"]:
        mark = "通过" if item["passed"] else "失败"
        print(
            f"  [{mark}] {item['name']}  "
            f"{item['points']}/{item['maximum']}  {item['elapsed_ms']} ms"
        )
        if not item["passed"]:
            print(f"         {item['message']}")
            if item["stderr"]:
                print(f"         {item['stderr'].splitlines()[-1]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=8767)
    args = parser.parse_args()

    if args.serve:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
        url = f"http://127.0.0.1:{args.port}/"
        print(f"2026-10-21 实际考试复盘网页已启动：{url}")
        print("按 Control+C 停止。")
        webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
        return

    total = maximum = 0
    for problem in (1, 2):
        path = ROOT / f"solution{problem}.py"
        if not path.exists():
            print(f"缺少 {path.name}")
            continue
        result = judge_code(problem, path.read_text(encoding="utf-8"))
        print_result(result)
        total += result["score"]
        maximum += result["maximum"]

    print(f"\n模拟总分: {total} / {maximum}")
    print("说明：这是本地练习测试，不是华为或 CodeFun 官方评分。")


if __name__ == "__main__":
    main()
