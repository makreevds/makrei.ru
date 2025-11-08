from flask import render_template, request, redirect, url_for, flash, Response, session, current_app
from functools import wraps
from datetime import datetime
from typing import List, Optional

from . import db, ADMIN_USERNAME, ADMIN_PASSWORD
from .models import Post, Visit
from flask import Blueprint

bp = Blueprint('main', __name__)

# --- Декоратор авторизации ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function


# --- Логирование посещений ---
@bp.before_app_request
def log_visit():
    if request.endpoint in ('static',) or request.path.startswith('/static') or request.path == '/favicon.ico':
        return
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.user_agent.string
    path = request.path
    visit = Visit(ip=ip, user_agent=user_agent, path=path)
    db.session.add(visit)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()

# --- Маршруты сайта ---
@bp.route('/')
def index():
    return render_template('home.html')

@bp.route('/blog')
def blog():
    posts = Post.query.order_by(Post.published_at.desc()).all()
    return render_template('blog.html', posts=posts)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('Успешный вход в админ-панель!', 'success')
            return redirect(url_for('main.admin'))
        else:
            flash('Неверный логин или пароль!', 'error')
    if session.get('logged_in'):
        return redirect(url_for('main.admin'))
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Вы успешно вышли из админ-панели!', 'success')
    return redirect(url_for('main.index'))

@bp.route('/admin')
@login_required
def admin():
    posts = Post.query.order_by(Post.published_at.desc()).all()
    return render_template('admin.html', posts=posts)

@bp.route('/admin/create', methods=['POST'])
@login_required
def create_post():
    title = request.form.get('title', '').strip()
    text = request.form.get('text', '').strip()
    if not title or not text:
        flash('Заголовок и текст обязательны для заполнения!', 'error')
        return redirect(url_for('main.admin'))
    new_post = Post(title=title, text=text, published_at=datetime.utcnow())
    db.session.add(new_post)
    db.session.commit()
    flash('Пост успешно создан!', 'success')
    return redirect(url_for('main.admin', post_id=new_post.id))

@bp.route('/admin/edit/<int:post_id>', methods=['POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    title = request.form.get('title', '').strip()
    text = request.form.get('text', '').strip()
    if not title or not text:
        flash('Заголовок и текст обязательны для заполнения!', 'error')
        return redirect(url_for('main.admin', post_id=post_id))
    post.title = title
    post.text = text
    db.session.commit()
    flash('Пост успешно обновлен!', 'success')
    return redirect(url_for('main.admin', post_id=post_id))

@bp.route('/admin/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Пост успешно удален!', 'success')
    return redirect(url_for('main.admin'))

@bp.route('/visits')
@login_required
def visits():
    visits = Visit.query.order_by(Visit.timestamp.desc()).limit(200).all()
    return render_template('visits.html', visits=visits)

@bp.route('/visits/clear', methods=['POST'])
@login_required
def clear_visits():
    Visit.query.delete()
    db.session.commit()
    flash('Логи посещений очищены.', 'success')
    return redirect(url_for('main.visits'))
