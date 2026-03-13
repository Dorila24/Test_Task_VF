# CLI Vector Editor

Простой векторный редактор с интерфейсом командной строки на Python 3.14.
Приложение хранит фигуры только в памяти текущего запуска и поддерживает:

- создание фигур `point`, `segment`, `circle`, `square`
- удаление фигур по авто-ID
- просмотр списка созданных фигур

## Запуск

Из корня проекта:

```bash
python -m vector_editor
```

## Команды

```text
create point <x> <y>
create segment <x1> <y1> <x2> <y2>
create circle <cx> <cy> <radius>
create square <x> <y> <side>
delete <id>
list
help
exit
quit
```

Правила:

- все координаты и размеры читаются как `float`
- `radius` и `side` должны быть больше `0`
- квадрат задается через левый верхний угол `x y` и длину стороны
- фигуры выводятся в порядке создания

## Пример сессии

```text
> create point 1 2
Created point with id=1
> create square 7 8 2
Created square with id=2
> list
[1] point x=1 y=2
[2] square x=7 y=8 side=2
> delete 1
Deleted shape id=1
> list
[2] square x=7 y=8 side=2
> exit
```

## Тесты

```bash
python -m unittest discover -s tests -v
```
