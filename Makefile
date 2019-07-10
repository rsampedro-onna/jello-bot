pip = ./venv/bin/pip
.PHONY: clean

clean:
	rm -rf venv/
	rm -rf dist/
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -f .coverage
	rm -rf .pytest_cache
	rm -rf *.egg-info
	@echo 'Removing docker images...'
	rm -rf ./docker/spyder_build

venv: requirements.txt
	python3.6 -m venv venv --clear
	$(pip) install -U pip wheel
	$(pip) install -e .
