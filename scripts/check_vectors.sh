#!/bin/sh
# Ассемблирует и выполняет три программы векторного sqrt,
# сравнивает дампы памяти с ожидаемыми (examples/expected/*.csv).
cd "$(dirname "$0")/.." || exit 1
status=0
for item in vector_squares:100-109 vector_mixed:500-509 vector_large:1000-1009; do
    name="${item%%:*}"
    range="${item#*:}"
    echo "== $name ($range)"
    ./run.sh asm "examples/$name.asm" "output/$name.bin" || exit 1
    ./run.sh run "output/$name.bin" "output/$name.csv" "$range" || exit 1
    if diff "examples/expected/$name.csv" "output/$name.csv"; then
        echo "OK: дамп совпадает с ожидаемым"
    else
        echo "ОШИБКА: дамп отличается"
        status=1
    fi
    tr '\n' ' ' < "output/$name.csv"
    echo
done
exit $status
