# 1. Удалить старый venv
rm -rf /root/Projects/Dart/venv/

# 2. Создать новый venv
cd /root/Projects/Dart/
python3 -m venv venv

# 3. Активировать venv
source venv/bin/activate

# 4. Установить зависимости
pip install -r requirements.txt

# 5. Запустить Gunicorn
sudo systemctl daemon-reload
sudo systemctl restart guni.service
sudo systemctl status guni.service