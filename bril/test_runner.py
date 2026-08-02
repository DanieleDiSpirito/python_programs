import sys
import subprocess

if len(sys.argv) < 3:
    print("Usage: python3 test_runner.py <file.t> <file.bril>")
    sys.exit(1)

test_file = sys.argv[1]
bril_file = sys.argv[2]

with open(test_file, 'r') as f:
    lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

has_failed = False

for i in range(0, len(lines), 2):
    if i + 1 >= len(lines):
        break
    
    arg = lines[i]
    expected = lines[i + 1]

    cmd = f"bril2json < {bril_file} | brili {arg}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    actual = result.stdout.strip()

    if actual == expected:
        print(f"[OK]   Input: {arg} -> Output: {actual}")
    else:
        print(f"[FAIL] Input: {arg} -> Expected: {expected} | Got: {actual}")
        has_failed = True

if has_failed:
    sys.exit(1)
