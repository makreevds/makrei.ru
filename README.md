# Минималистичный Flask-Блог

Минималистичный сайт на Flask с хранением записей блога в базе данных (SQLite), чистым современным интерфейсом и возможностью легко управлять постами.

---

## Структура

- `app.py` — основной код приложения Flask.
- `static/style.css` — кастомные стили (цвета и параметры вынесены в переменные).
- `templates/` — html-шаблоны.
- `requirements.txt` — зависимости.
- `instance/blog.sqlite3` — база данных SQLite (создается автоматически).

---

## Установка и запуск

1. Создайте виртуальное окружение (рекомендуется):

   ```sh
   python -m venv venv
   venv\Scripts\activate   # для Windows
   # source venv/bin/activate  # для Linux/macOS
   ```

2. Установите зависимости:
   ```sh
   pip install -r requirements.txt
   ```

3. Запустите приложение:
   ```sh
   python app.py
   ```

4. Откройте [http://localhost:5000](http://localhost:5000) в браузере.

---

## Работа с постами блога через Python

Все записи блога хранятся в базе данных. Чтобы добавить или редактировать посты, используйте следующий способ:

**Запуск Python-консоли:**
```python
python
```

**Импорт приложения и модели:**
```python
from app import app, db, Post
```

**Добавление поста:**
```python
with app.app_context():
    db.session.add(Post(title="Заголовок", text="Текст записи"))
    db.session.commit()
```

**Изменение поста:**
```python
with app.app_context():
    post = Post.query.filter_by(id=1).first()
    post.text = "Новый текст"
    db.session.commit()
```

**Удаление поста:**
```python
with app.app_context():
    post = Post.query.filter_by(title="Заголовок").first()
    db.session.delete(post)
    db.session.commit()
```

---

## Контакты и поддержка

Если возникнут вопросы по доработке сайта или работе с Flask — открывай issue или пиши напрямую!
