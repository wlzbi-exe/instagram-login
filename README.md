# instagram-login
Instagram Session &amp; Login Toolkit Python-based Instagram authentication utility with login handling, 2FA verification, device approval, response debugging, and session/token parsing. Built for authorized security research and testing only.
Instagram Login & Session Toolkit

<p align="center">
  <b>Instagram Authentication & Session Handling Toolkit</b><br>
  Python-based utility for authorized testing and research
</p><p align="center">
  <a href="https://t.me/rejerks">
    <img src="https://img.shields.io/badge/Telegram-@rejerks-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white">
  </a>
  <a href="https://t.me/Wlzbi">
    <img src="https://img.shields.io/badge/Channel-@Wlzbi-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white">
  </a>
</p>---

✨ Features

- 🔐 Instagram login request handling
- 🔑 Username/email authentication
- 🛡️ Two-factor authentication flow
- 📱 Device approval / Limbo handling
- 🎫 Session and authorization token parsing
- 🧩 Instagram Bloks API request handling
- 📝 Response logging for debugging
- 🔄 Automatic retry handling
- ⚙️ Dynamic device and session identifiers
- 🐍 Lightweight Python implementation

---

🛠️ Requirements

- Python 3.8+
- "requests"

Install the dependency:

pip install requests

---

🚀 Usage

Run the script:

python session-graber.py

Enter the requested credentials when prompted:

Enter username or email: your_username
Enter password: your_password

The tool handles the authentication flow and processes supported verification states.

---

🔐 2FA Support

The toolkit includes handling for accounts requiring additional verification.

Supported flows include:

- Two-step verification
- Authentication code entry
- Device approval
- Verification response processing

When required, the script prompts for the verification code.

---

📁 Response Logs

Authentication responses are saved to:

response.txt

This can be useful for debugging unexpected authentication responses or investigating failed requests.

Do not share "response.txt" publicly if it contains sensitive account or session information.

---

⚠️ Disclaimer

This project is intended only for authorized security research, development, testing, and educational purposes.

Use it only with accounts and systems you own or have explicit permission to test.

The author is not responsible for:

- Unauthorized account access
- Misuse of extracted authentication data
- Account restrictions or suspensions
- Loss of credentials or session data
- Any damage resulting from improper use

Never use this project to access accounts without authorization.

---

📌 Security Notice

Authentication tokens, session IDs, passwords, and response dumps can contain highly sensitive information.

Never:

- Commit credentials to GitHub
- Share session IDs publicly
- Upload "response.txt"
- Hard-code passwords into source code
- Share authentication tokens with third parties

Consider adding sensitive files to ".gitignore":

response.txt
*.session
.env
__pycache__/

---

📬 Contact

<p align="center">
  <a href="https://t.me/rejerks">
    <img src="https://img.shields.io/badge/Telegram-@rejerks-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white">
  </a>
  <a href="https://t.me/Wlzbi">
    <img src="https://img.shields.io/badge/Telegram%20Channel-@Wlzbi-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white">
  </a>
</p><p align="center">
  <b>Developer:</b> @rejerks &nbsp;•&nbsp; <b>Channel:</b> @Wlzbi
</p>

---

<p align="center">
  <b>WLZBI</b><br>
  
</p>
