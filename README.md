# Performance Reports CLI

Короткий консольный инструмент для генерации различных отчётов по данным из CSV-файлов.  
Проект использует только стандартную библиотеку Python (argparse, csv и др.),  
при этом архитектура позволяет быстро добавлять новые типы отчётов.

## Пример запуска

```bash
python main.py --files data1.csv data2.csv --report performance
