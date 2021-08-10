# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta

from flask import Blueprint, send_from_directory, render_template, abort, request
from flask_login import current_user

from apps.common.auth import signin_required
from apps.database.models import Post, Tag, View, Comment
from apps.database.session import db
from config import Config

app = Blueprint('index', __name__, url_prefix='/')


@app.route('', methods=['GET'])
@signin_required
def index():
    args = request.args
    page = int(args.get('page') or 1)
    per_page = 3

    pagination = Post.query.order_by(Post.id.desc()).paginate(page, per_page)
    posts = pagination.items
    for post in posts:
        post.content = re.sub(r'<img.*/>', '', post.content)[:20]
    return render_template('main/index.html', posts=posts, pagination=pagination)


@app.route('/<int:post_id>', methods=['GET'])
@signin_required
def get_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    if not post:
        abort(404)
    view = View.query.filter(View.ip_address == request.remote_addr, View.post_id == post.id,
                             View.user_id == current_user.id,
                             View.created_at > datetime.now() - timedelta(minutes=30)).first()
    if not view:
        view = View(ip_address=request.remote_addr, post_id=post.id, user_id=current_user.id)
        db.session.add(view)
        db.session.commit()
    view_cnt = View.query.filter(View.post_id == post.id).count()

    prev_post = Post.query.filter(Post.id < post_id).order_by(Post.id.desc()).first()
    next_post = Post.query.filter(Post.id > post_id).order_by(Post.id.desc()).first()

    related_posts = []
    for tag in post.tags:
        tags = Tag.query.filter(Tag.title == tag.title, Tag.post_id != post.id).order_by(Tag.id.desc()).limit(2).all()
        for t in tags:
            if not [x for x in related_posts if x.id == t.post.id]:
                t.post.thumbnail = re.search(r'<img.*/>', t.post.content)
                t.post.thumbnail = t.post.thumbnail.group() if t.post.thumbnail else None
                t.post.content = re.sub(r'<img.*/>', '', t.post.content)[:20]
                related_posts.append(t.post)
    related_posts = related_posts[:6]

    comments = Comment.query.filter(Comment.post_id == post.id, Comment.parent_id == None).all()
    for comment in comments:
        comment.comments = Comment.query.filter(Comment.parent_id == comment.id).all()
    return render_template('main/post.html', post=post, prev_post=prev_post, next_post=next_post,
                           related_posts=related_posts, view_cnt=view_cnt, comments=comments)


@app.route('/<int:post_id>/update', methods=['GET'])
@signin_required
def update(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    if not post:
        abort(404)
    return render_template('main/update.html', post=post)


@app.route('/about', methods=['GET'])
@signin_required
def about():
    return render_template('main/about.html')


@app.route('/create', methods=['GET'])
@signin_required
def create():
    return render_template('main/create.html')


@app.route('favicon.ico')
def favicon():
    return send_from_directory(Config.STATIC_DIR, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
