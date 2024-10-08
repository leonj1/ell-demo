# Makefile for GitLab MR Analyzer

# Python interpreter
PYTHON = python3

.PHONY: build

build:
	$(PYTHON) -m pip install -r requirements.txt

