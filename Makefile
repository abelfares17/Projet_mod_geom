.PHONY: install run-p1 run-p2 clean

VENV    = .venv
PYTHON  = $(VENV)/bin/python3
PIP     = $(VENV)/bin/pip

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip --quiet
	$(PIP) install -r requirements.txt
	@echo "\n✓ Environnement prêt. Activer avec :  source .venv/bin/activate"

run-p1:
	$(PYTHON) simulations/partie1_mouvement_aleatoire.py

run-p2:
	$(PYTHON) simulations/partie2_trafalgar.py

clean:
	rm -rf $(VENV)
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
