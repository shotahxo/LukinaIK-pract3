#!/bin/sh
# Демонстрация сообщений об ошибках ассемблера.
cd "$(dirname "$0")/.." || exit 1
for file in examples/errors/*.asm examples/errors/no_such_file.asm; do
    printf '\n>>> %s\n' "$file"
    ./run.sh asm "$file" output/error.bin --test
    printf '<<< код завершения: %s\n' "$?"
done
