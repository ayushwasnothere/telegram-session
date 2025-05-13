---
# 🤖 Telegram Session Generator Bot

A Telegram bot to generate session strings for **Telethon** and **Pyrogram**, using an interactive chat interface with buttons. Useful for developers who want to authenticate Telegram accounts for bots or automation scripts.
---

## ✨ Features

- ✅ Supports **Telethon** and **Pyrogram** session generation.
- 📱 User-friendly interface with Telegram Reply Keyboards.
- ❌ Cancel current operation at any step.
- 🔁 Retry session generation with a single button.
- 🧹 Automatically removes reply keyboards on cancel or completion.
- 🔐 Secure: Keeps session strings private and doesn't store any data.

---

## 🧰 Dependencies

This bot uses the following Python libraries:

- [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot)
- [`telethon`](https://github.com/LonamiWebs/Telethon)
- [`pyrogram`](https://github.com/pyrogram/pyrogram)
- [`tgcrypto`](https://pypi.org/project/tgcrypto/) (for fast Pyrogram encryption)

Install them using:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```txt
python-telegram-bot==20.8
telethon==1.34.0
pyrogram==2.0.106
tgcrypto

```

---

## ⚙️ Configuration

Configuration is handled via **environment variables**. You need to set the following before running the bot:

| Variable    | Description                                 |
| ----------- | ------------------------------------------- |
| `BOT_TOKEN` | Your Telegram Bot token                     |
| `API_ID`    | Your Telegram API ID from my.telegram.org   |
| `API_HASH`  | Your Telegram API Hash from my.telegram.org |

You can set them in a `.env` file or export them manually:

### Option 1: Using `.env` file (recommended)

Create a `.env` file in the root directory:

```env
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
API_ID=12345678
API_HASH=abcd1234efgh5678ijkl9012mnop3456
```

Then, load the environment variables in your script using `python-dotenv` (if you're using it).

### Option 2: Manual export (Linux/macOS)

```bash
export BOT_TOKEN=123456:ABC...
export API_ID=12345678
export API_HASH=abcd1234...
```

---

## ▶️ Running the Bot

After installing dependencies and setting environment variables:

```bash
python main.py
```

If you are using a `.env` file, you can run the bot with:

```bash
python -m dotenv main.py
```

---

## 💡 How to Use

1. Start the bot with `/start`.
2. Select **Telethon** or **Pyrogram** from the options.
3. Enter your **phone number** (e.g., `+911234567890`).
4. Enter the **verification code** received in your Telegram app.
5. You will receive your **session string**.
6. Tap 🔁 **Again** to generate another, or ❌ **Cancel** to stop.

---

## 🛡️ Security Notice

⚠️ The generated session string provides full access to your Telegram account.

- Never share it publicly.
- This bot does **not** store any session strings or credentials.
- Use only in trusted or local environments.

---

## 🛠️ Development Tips

- Use a virtual environment to isolate dependencies:

  ```bash
  python -m venv venv
  source venv/bin/activate  # or .\venv\Scripts\activate on Windows
  ```

- Debug logging can be enabled for troubleshooting.

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

Built with ❤️ by [`ayushwasnothere`](https://github.com/ayushwasnothere)
Feel free to contribute or open issues!
