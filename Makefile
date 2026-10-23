.PHONY: all test benchmark index clean

PYTHON ?= python

all: test

test:
	$(PYTHON) scripts/tester.py

benchmark:
	$(PYTHON) scripts/benchmarker.py

index:
	$(PYTHON) scripts/indexer.py

clean:
	$(PYTHON) scripts/cleaner.py
