# Установка виртуального окружения для python
```bash
python -m venv venv
```

# Активация виртуального окружения для python
```bash
venv/Scripts/activate  # (для Windows)
source ./venv/bin/actiavte  # ( для Linux)
```

# Установка зависимостей в pip
```bash
pip install -r .\requirements.txt
```

# Для Debian нужно установить chrome браузер
```bash
wget -nc https://dl-ssl.google.com/linux/linux_signing_key.pub 
cat linux_signing_key.pub | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/linux_signing_key.gpg  >/dev/null
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/chrome.list'
sudo apt update
sudo apt install google-chrome-stable
```

# Установка зависимостей для Allure
```bash
sudo apt install default-jdk -y
```

# Установка Allure
https://allurereport.org/docs/install-for-linux/
```bash
wget https://github.com/allure-framework/allure2/releases/download/2.32.2/allure_2.32.2-1_all.deb
sudo dpkg -i ./allure*.deb
```

# Файл окружения
В корневом каталоге проекта создать файл .env на основе .env.example

# Запуск тестов
```bash
pytest .\tests dns_test.py
pytest --count=10 .\tests\dns_test.py  # запустить тест 10 раз
```
