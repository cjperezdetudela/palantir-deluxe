import base64
import codecs
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def analyze_file(filepath):
    print(f"\n=================== {filepath} ===================")
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    for varname in ['elfary', 'valderrama', 'montolla', 'farina']:
        m = re.search(r"^" + varname + r"\s*=\s*'([^']+)'", code, re.MULTILINE)
        if m:
            val = m.group(1)
            print(f"\n--- {varname} (len={len(val)}) ---")
            # Try b64
            try:
                rem = len(val) % 4
                s_b64 = val[:-rem] if rem else val
                b64_dec = base64.b64decode(s_b64).decode('utf-8', errors='ignore')
                print(f"[B64 sample]: {b64_dec[:200]}")
            except Exception as e:
                print(f"[B64 err]: {e}")
            # Try rot13
            try:
                rot13_dec = codecs.decode(val, 'rot13')
                print(f"[ROT13 sample]: {rot13_dec[:200]}")
            except Exception as e:
                print(f"[ROT13 err]: {e}")

analyze_file(r"extracted_plugin.video.palantir3\plugin.video.palantir3\default.py")
analyze_file(r"extracted_plugin.video.palantir3\plugin.video.palantir3\context.py")
