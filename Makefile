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

run-p2-bis:
	$(PYTHON) simulations/partie2_bis.py

run-p3:
	$(PYTHON) simulations/partie3_aoki.py

run-p4:
	$(PYTHON) simulations/partie4_densite.py

run-p5:
	$(PYTHON) simulations/partie5_visual_network.py


clean:
	rm -rf $(VENV)
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
