#!/bin/sh
# Ассемблер:     ./run.sh asm ИСХОДНИК.asm ПРОГРАММА.bin [--test]
# Интерпретатор: ./run.sh run ПРОГРАММА.bin ДАМП.csv НАЧАЛО-КОНЕЦ
cd "$(dirname "$0")" || exit 1
command="$1"
shift
case "$command" in
    asm) PYTHONPATH=src exec python3 -m uvm.assembler "$@" ;;
    run) PYTHONPATH=src exec python3 -m uvm.interpreter "$@" ;;
    *) echo "использование: ./run.sh asm|run ..." >&2; exit 2 ;;
esac
