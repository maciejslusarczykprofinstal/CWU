from pathlib import Path

def test_layout_has_expected_files():
    root = Path(".")
    required = ["app.py", "requirements.txt", "templates", "static", "calc", "tasks.json"]
    missing = [p for p in required if not (root / p).exists()]
    assert not missing, f"Brakuje plików/katalogów: {missing}"
