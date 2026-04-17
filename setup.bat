@echo off
python -m venv .venv
.venv\Scripts\pip install --upgrade pip --quiet
.venv\Scripts\pip install -r requirements.txt
echo.
echo Environnement pret. Activer avec :  .venv\Scripts\activate
