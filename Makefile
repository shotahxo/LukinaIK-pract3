PYTHON ?= python3
export PYTHONPATH := src:tests

.PHONY: test spec errors

test:
	$(PYTHON) -m unittest discover -s tests -v

spec:
	./run.sh asm examples/spec_tests.asm output/spec_tests.bin --test

errors:
	./scripts/check_asm_errors.sh
