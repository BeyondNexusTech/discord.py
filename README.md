# 🤖 BeyondNexusTech Discord Bot

Un bot Discord développé en Python avec `discord.py`. Il propose des commandes utiles, ludiques, et personnalisables, comme le classique **pile ou face**, ainsi que des commandes administratives et des extensions futures.

---

## 🚀 Fonctionnalités

- 🎮 `!pileouface` → Lance une pièce virtuelle
- 📌 Système de commandes modulaires (`commands/`, `cogs/`)
- 🛠️ Gestion des événements (`on_ready`, `on_message`, etc.)
- 🔒 Chargement sécurisé via `.env` (token Discord)
- ⚙️ Prêt à être déployé sur un serveur Linux/Docker

---

## 🧰 Technologies

- Python 3.10+
- `discord.py` (v2.x)
- `python-dotenv` pour les variables d'environnement

---

## 📦 Installation

```bash
git clone https://github.com/ton-utilisateur/ton-bot.git
cd ton-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
