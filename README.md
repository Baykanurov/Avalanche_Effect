<h1 align="center">
Уникальный алгоритм хеширования на основе SHA-256 с лавинным эффектом
</h1>

## Поддерживаемые методы скрипта:
- Чтение из файла
- Чтение из строки
- Запись результата в файл

## Примеры
```bash
python hash.py -t "Test"
```
Результат:
```bash
Original hash: 53 2e aa bd 95 74 88 0d bf 76 b9 b8 cc 00 83 2c 20 a6 ec 11 3d 68 22 99 55 0d 7a 6e 0f 34 5e 25
Modified hash: 08 4c a7 69 6e 2a 49 95 38 71 81 ed 17 d4 41 66 a8 7a 18 0d 32 46 ff 8a 02 14 e7 a4 db e4 bb 06
Number of changed bits: 3
```

```bash
python hash.py -f ./test.txt
```
```bash
python hash.py -f ./test.txt -o ./result.txt
```



