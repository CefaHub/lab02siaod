# Лабораторная работа № 2 — СИАОД

**Вариант:** 14  
**Seed:** 44

## Состав проекта

- `lab02.py` — рекурсивные функции, `DynamicArray`, `Stack`, `Deque`, проверки и замеры.
- `generate_variant_data.py` — генерация входных данных варианта 14.
- `REPORT.md` — отчёт с анализом сложности и результатами измерений.
- `requirements.txt` — зависимость для построения графиков.

## Запуск

Требуется Python 3.10 или новее.

```bash
python generate_variant_data.py
python lab02.py --variant 14 --data data/generated --out .
```

Для построения графиков:

```bash
python -m pip install -r requirements.txt
```

Встроенные проверки выполняются перед замерами. Сгенерированные входные данные хранятся в `data/generated` и не добавляются в репозиторий.
