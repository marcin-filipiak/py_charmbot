# Charmbot - Discord Moderation & Utility Bot

```
   ____       _    _         __          _____       __    __      ____        ____       _______    
  / __ \     | |  | |      /    \       |  __ \     |  \  /  |    |  _ \      / __ \     |__   __|   
 / /  \_|    | |__| |     /  /\  \      | |__) |    |   \/   |    | |_| |    | |  | |       | |      
| |          |  __  |    /  /__\  \     |  _  /     | |\  /| |    |  _  {    | |  | |       | |      
| \____      | |  | |   /  /    \  \    | | \ \     | | \/ | |    | |_| |    | |__| |       | |      
 \_____|     |_|  |_|   \_/      \_/    |_|  \_\    |_|    |_|    |____/      \____/        |_|       

Copyright (c) 2025 Marcin Filipiak  
Licensed under the MIT License
```

---

## 📘 Opis projektu

Bot Discord napisany w Pythonie z wykorzystaniem biblioteki **discord.py**, pełniący funkcję **moderatora** oraz **asystenta społeczności**.
Oferuje funkcje automatycznego przydzielania ról, reagowania na wiadomości, nakładania timeoutów, flirtujących odpowiedzi oraz dodawania stempli do obrazów.

---

## ⚙️ Funkcje

### 🛡️ Moderacja

* automatyczne **usuwanie wiadomości zawierających zakazane frazy**,
* nakładanie **timeoutu (24h)** na użytkowników łamiących regulamin,
* wysyłanie powiadomień o karach na kanał moderatorów,
* przydzielanie roli (`ROLE_NAME`) po pierwszej aktywności użytkownika.

### 💬 Interakcje

* flirtujące odpowiedzi, gdy bot zostanie wspomniany,
* komenda `?zaczep <kanał>` — losowo wybiera użytkownika, który ostatnio reagował emoji w danym kanale, i wysyła do niego zaczepkę,
* komenda `?ping` — testowa, sprawdzająca aktywność bota.

### 🖼️ Obrazki

* komenda `?stamp` — nakłada półprzezroczysty stempel (`stamp.gif`) na przesłane obrazy.

### ⏰ Automatyczne zadania

* przypomnienia o komendzie `/bump` (jeśli `ENABLE_TASKS=True` i `BUMP_INTERVAL_HOURS>0`).

---

## 🧩 Wymagania

* Python 3.10 lub nowszy
* Zainstalowane biblioteki:

  ```bash
  pip install discord.py Pillow aiohttp
  ```

---

## 📁 Struktura projektu

```
discord-bot/
│
├── charmbot.py                 # główny plik bota
├── config.py              # konfiguracja i ustawienia
├── flirty.txt             # lista flirtujących odpowiedzi
├── banned_phrases.txt     # lista zakazanych fraz
├── stamp.gif              # stempel nakładany na obrazy
├── LICENSE
└── README.md
```

---

## 🔧 Konfiguracja

W pliku `config.py` można ustawić wszystkie parametry działania bota:

| Nazwa                      | Opis                                                  | Przykład               |
| -------------------------- | ----------------------------------------------------- | ---------------------- |
| `TOKEN`                    | Token bota Discord                                    | `'...'`                |
| `ROLE_NAME`                | Nazwa roli nadawanej po pierwszym poście              | `'Podglądacz'`         |
| `MOD_CHANNEL_NAME`         | Kanał, na który wysyłane są powiadomienia moderatorów | `'moderator-only'`     |
| `TIMEOUT_DURATION_SECONDS` | Czas wyciszenia użytkownika w sekundach               | `86400`                |
| `FLIRTY_FILE`              | Ścieżka do pliku z flirtującymi tekstami              | `'flirty.txt'`         |
| `BANNED_PHRASES_FILE`      | Ścieżka do pliku z zakazanymi frazami                 | `'banned_phrases.txt'` |
| `ENABLE_TASKS`             | Czy bot ma wykonywać zadania okresowe                 | `True`                 |
| `BUMP_CHANNEL_NAME`        | Kanał, gdzie wysyłane są przypomnienia `/bump`        | `'bump'`               |
| `BUMP_INTERVAL_HOURS`      | Częstotliwość przypomnień w godzinach (0 = wyłączone) | `4`                    |
| `COMMAND_PREFIX`           | Prefiks komend bota                                   | `'?'`                  |

---

## 🚀 Uruchomienie

1. Skopiuj repozytorium:

   ```bash
   git clone https://github.com/<twoje_repo>/discord-bot.git
   cd discord-bot
   ```

2. Utwórz wirtualne środowisko (opcjonalnie, ale zalecane):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Zainstaluj zależności:

   ```bash
   pip install -r requirements.txt
   ```

4. Skonfiguruj plik `config.py` — wstaw token bota i odpowiednie nazwy kanałów.

5. Uruchom bota:

   ```bash
   python3 charmbot.py
   ```

---

## 🧠 Dodatkowe informacje

* Bot reaguje tylko na wiadomości użytkowników (ignoruje inne boty).
* Jeśli plik `flirty.txt` nie istnieje, bot użyje domyślnej wiadomości flirtującej.
* Zakazane frazy są sprawdzane bez rozróżniania wielkości liter.
* Plik `stamp.gif` powinien być w tym samym katalogu co `charmbot.py`.

---

## 📜 Licencja

Projekt udostępniany na licencji MIT License.
Autor: Marcin Filipiak, 2025.

Projekt udostępniany na licencji **MIT License**.
Autor: **Marcin Filipiak**, 2025.
