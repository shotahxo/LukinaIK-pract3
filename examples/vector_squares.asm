; Поэлементный sqrt() над вектором длины 10, результат — в исходный вектор.
; Данные: точные квадраты.
; Вектор лежит по адресам 100–109, ячейка 0 — указатель на текущий элемент.
; Для каждого элемента: указатель = его адрес, затем SQRT элемент, указатель,
; то есть mem[100+i] = sqrt(mem[100+i]).
; Дамп: ./run.sh run output/vector_squares.bin output/vector_squares.csv 100-109

; Исходный вектор
LOAD 100, 0
LOAD 101, 1
LOAD 102, 4
LOAD 103, 9
LOAD 104, 16
LOAD 105, 25
LOAD 106, 36
LOAD 107, 49
LOAD 108, 64
LOAD 109, 81

; sqrt по каждому элементу на месте
LOAD 0, 100
SQRT 100, 0       ; sqrt(0) = 0
LOAD 0, 101
SQRT 101, 0       ; sqrt(1) = 1
LOAD 0, 102
SQRT 102, 0       ; sqrt(4) = 2
LOAD 0, 103
SQRT 103, 0       ; sqrt(9) = 3
LOAD 0, 104
SQRT 104, 0       ; sqrt(16) = 4
LOAD 0, 105
SQRT 105, 0       ; sqrt(25) = 5
LOAD 0, 106
SQRT 106, 0       ; sqrt(36) = 6
LOAD 0, 107
SQRT 107, 0       ; sqrt(49) = 7
LOAD 0, 108
SQRT 108, 0       ; sqrt(64) = 8
LOAD 0, 109
SQRT 109, 0       ; sqrt(81) = 9
