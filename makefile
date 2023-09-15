SHELL = /bin/bash

# run style formatting
.PHONY: format
format:
	black .

.PHONY: run
run: 
	python3 scripts/process.py

# Cleaning
.PHONY: clean
clean: 
	find . -type f -name "*.DS_Store" -ls -delete
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	find . | grep -E ".trash" | xargs rm -rf
	rm -f .coverage

.PHONY: help
help:
	@echo "Commands:"
	@echo "format   : executes style formatting."
	@echo "clean    : deletes all unnecessary files "
	@echo "run   	: starts running the pipeline."