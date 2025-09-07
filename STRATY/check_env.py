# check_env.py
"""
Szybki test środowiska .venv
Sprawdza, czy są zainstalowane główne biblioteki (Flask, numpy)
i wypisuje ich wersje.
"""

def check_package(pkg_name, import_name=None):
    try:
        if import_name is None:
            import_name = pkg_name
        module = __import__(import_name)
        version = getattr(module, "__version__", "brak wersji")
        print(f"[OK] {pkg_name} wersja: {version}")
    except ImportError:
        print(f"[BŁĄD] {pkg_name} nie jest zainstalowany w tym środowisku!")

def main():
    print("=== Test środowiska .venv ===")
    check_package("Flask", "flask")
    check_package("NumPy", "numpy")
    print("=== Koniec testu ===")

if __name__ == "__main__":
    main()
