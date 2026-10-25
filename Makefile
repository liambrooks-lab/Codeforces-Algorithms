.PHONY: all test benchmark index clean push

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

push:
	git add .
	git commit -m "$(msg)"
	git pull --rebase origin main
	make test
	git push