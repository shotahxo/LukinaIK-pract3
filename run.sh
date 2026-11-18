#!/bin/sh
# Запуск ассемблера: ./run.sh asm ИСХОДНИК РЕЗУЛЬТАТ [--test]
cd "$(dirname "$0")" || exit 1
command="$1"
shift
case "$command" in
    asm) PYTHONPATH=src exec python3 -m uvm.assembler "$@" ;;
    *) echo "использование: ./run.sh asm ..." >&2; exit 2 ;;
esac
