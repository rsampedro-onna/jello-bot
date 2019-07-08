venv: requirements.txt test-requirements.txt
	python3.6 -m venv venv --clear
	$(pip) install -U pip wheel
	$(pip) install -e .

