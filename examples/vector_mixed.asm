; Поэлементный sqrt() над вектором длины 10, результат — в исходный вектор.
; Данные: числа, не являющиеся точными квадратами.
; Вектор лежит по адресам 500–509, ячейка 0 — указатель на текущий элемент.
; Для каждого элемента: указатель = его адрес, затем SQRT элемент, указатель,
; то есть mem[500+i] = sqrt(mem[500+i]).
; Дамп: ./run.sh run output/vector_mixed.bin output/vector_mixed.csv 500-509

; Исходный вектор
LOAD 500, 2
LOAD 501, 3
LOAD 502, 5
LOAD 503, 8
LOAD 504, 15
LOAD 505, 17
LOAD 506, 24
LOAD 507, 26
LOAD 508, 99
LOAD 509, 101

; sqrt по каждому элементу на месте
LOAD 0, 500
SQRT 500, 0       ; sqrt(2) = 1
LOAD 0, 501
SQRT 501, 0       ; sqrt(3) = 1
LOAD 0, 502
SQRT 502, 0       ; sqrt(5) = 2
LOAD 0, 503
SQRT 503, 0       ; sqrt(8) = 2
LOAD 0, 504
SQRT 504, 0       ; sqrt(15) = 3
LOAD 0, 505
SQRT 505, 0       ; sqrt(17) = 4
LOAD 0, 506
SQRT 506, 0       ; sqrt(24) = 4
LOAD 0, 507
SQRT 507, 0       ; sqrt(26) = 5
LOAD 0, 508
SQRT 508, 0       ; sqrt(99) = 9
LOAD 0, 509
SQRT 509, 0       ; sqrt(101) = 10
