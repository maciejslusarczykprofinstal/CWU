# CWU - System Obliczania Strat Ciepła

## Gdzie są moje pliki? / Where are my files?

Wszystkie pliki Twojego projektu znajdują się w następujących lokalizacjach:

### 📁 Główna struktura katalogu

```
CWU/
├── .github/workflows/         # Konfiguracja CI/CD
│   └── ci.yml                # Automatyczne testy
├── STRATY/                   # 🎯 GŁÓWNY KATALOG APLIKACJI
│   ├── app.py               # Główny plik aplikacji Flask
│   ├── calc/                # Moduły obliczeniowe
│   ├── static/              # Pliki statyczne (CSS, JS, HTML)
│   ├── templates/           # Szablony Flask
│   ├── tests/              # Testy jednostkowe
│   ├── requirements.txt     # Zależności Python
│   ├── check_env.py        # Sprawdzanie środowiska
│   └── tasks.json          # Konfiguracja zadań
└── README.md               # Ten plik dokumentacji
```

## 🔍 Szczegółowa mapa plików

### 🧮 Moduły obliczeniowe (`STRATY/calc/`)
- `__init__.py` - Inicjalizacja pakietu
- `dhw_demand.py` - Obliczenia zapotrzebowania na ciepłą wodę
- `finance.py` - Obliczenia finansowe i kosztów
- `heat_loss.py` - Obliczenia strat ciepła
- `norms.py` - Normy i standardy
- `pipes.py` - Obliczenia dla rurociągów
- `storage.py` - Obliczenia dla zasobników
- `Nowy dokument tekstowy.txt` - Pusty plik tekstowy (może być usunięty)

### 🌐 Interface użytkownika (`STRATY/static/` i `STRATY/templates/`)
- `static/index.html` - Strona główna
- `static/main.js` - Logika JavaScript
- `static/style.css` - Style CSS
- `templates/4_Straty.html` - Szablon formularza obliczeń

### 🧪 Testy (`STRATY/tests/`)
- `test_repo_layout.py` - Test struktury repozytorium

### ⚙️ Konfiguracja
- `requirements.txt` - Lista wymaganych bibliotek Python
- `check_env.py` - Skrypt sprawdzania środowiska
- `tasks.json` - Konfiguracja zadań

## 🚀 Jak uruchomić aplikację

1. **Instalacja zależności:**
   ```bash
   cd STRATY
   pip install -r requirements.txt
   ```

2. **Sprawdzenie środowiska:**
   ```bash
   python check_env.py
   ```

3. **Uruchomienie aplikacji:**
   ```bash
   python app.py
   ```

4. **Otwórz przeglądarkę:** http://localhost:5000

## 🔧 Co robi aplikacja

Aplikacja CWU służy do obliczania strat ciepła w systemach ciepłej wody użytkowej:

- **Straty pętli cyrkulacyjnej** - obliczenia strat w rurociągach
- **Straty zasobnika** - straty postojowe zbiorników
- **Bilans energetyczny** - roczne zużycie energii
- **Koszty eksploatacji** - obliczenia kosztów rocznych

## 📊 Stan projektu

✅ **Wszystkie pliki są na miejscu i działają poprawnie:**
- Aplikacja Flask uruchamia się bez błędów
- Moduły obliczeniowe są kompletne
- Testy przechodzą pomyślnie
- Środowisko jest skonfigurowane

## 🛠️ Rozwój

Aby dodać nowe funkcjonalności:
1. Dodaj obliczenia w katalogu `calc/`
2. Zaktualizuj `app.py` jeśli potrzeba nowych endpoint-ów
3. Dodaj testy w `tests/`
4. Zaktualizuj interface w `static/` i `templates/`

---

**Twoje pliki są bezpieczne i kompletne!** 🎉