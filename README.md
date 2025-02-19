# Установка виртуального окружения для python
python -m venv venv

# Активация виртуального окружения для python
venv/Scripts/activate (для Windows)
source ./venv/bin/actiavte ( для Linux)

# Установка зависимостей
pip install -r .\requirements.txt

# Файл окружения
В корневом каталоге проекта создать файл .env на основе .env.example

# Запуск тестов
pytest .\test dns_test.py
