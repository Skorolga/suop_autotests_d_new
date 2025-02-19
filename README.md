# Установка виртуального окружения для python
python -m venv venv

# Активация виртуального окружения для python
venv/Scripts/activate (для Windows)
source ./venv/bin/actiavte ( для Linux)

# Установка зависимостей в pip
pip install -r .\requirements.txt

# Для Debian нужно установить chrome браузер
```
wget -nc https://dl-ssl.google.com/linux/linux_signing_key.pub 
cat linux_signing_key.pub | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/linux_signing_key.gpg  >/dev/null
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/chrome.list'
sudo apt update
sudo apt install google-chrome-stable
```

# Установка зависимостей для Allure
```
sudo apt install default-jdk -y
```
# Установка Allure
https://allurereport.org/docs/install-for-linux/

```commandline
wget https://github.com/allure-framework/allure2/releases/download/2.32.2/allure_2.32.2-1_all.deb
sudo dpkg -i ./allure*.deb
```

# Файл окружения
В корневом каталоге проекта создать файл .env на основе .env.example

# Запуск тестов
pytest .\test dns_test.py
