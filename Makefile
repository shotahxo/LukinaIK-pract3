PYTHON ?= python3
export PYTHONPATH := src:tests

.PHONY: test spec errors copy sqrt vectors

test:
	$(PYTHON) -m unittest discover -s tests -v

spec:
	./run.sh asm examples/spec_tests.asm output/spec_tests.bin --test
	od -An -tx1 output/spec_tests.bin

errors:
	./scripts/check_asm_errors.sh

copy:
	./run.sh asm examples/copy_array.asm output/copy_array.bin
	./run.sh run output/copy_array.bin output/copy_array.csv 100-304
	grep -E '^(10[0-4]|20[0-4]|30[0-4]),' output/copy_array.csv

sqrt:
	./run.sh asm examples/sqrt_test.asm output/sqrt_test.bin
	./run.sh run output/sqrt_test.bin output/sqrt_test.csv 20-44
	grep -E '^(2[0-4]|4[0-4]),' output/sqrt_test.csv

vectors:
	./scripts/check_vectors.sh
