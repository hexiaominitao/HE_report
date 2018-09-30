import os
import pandas as pd
from pandas import DataFrame
from flask import render_template, redirect, session, url_for, request, current_app
from werkzeug import security

from . import main
from .. import db, filezips
from app.models import User
from .forms import LoginForm, SeqGroupForm, RegistFrom, PhotoForm


@main.route('/', methods=['GET', 'POST'])
def index():
    path_wk = os.getcwd()
    path_zip = current_app.config['UPLOADED_ZIPFILE_DEST']
    return render_template('index.html', path_wk=path_wk, path_zip=path_zip)


@main.route('/seqinfo/')
def seqinfo():
    return render_template('user.html')


@main.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login1.html', form=form)
    if form.validate_on_submit():
        username = form.username.data
        # print(username)
        password = form.password.data
        # print(password)
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('main.index'))
        else:
            return redirect(url_for('main.regist'))


# @main.route('/login1/', methods=["GET", "POST"])
# def login1():
#     if request.method == 'GET':
#         return render_template('login.html')
#     else:
#         username = request.form.get('username')
#         password = request.form.get('password')
#         user = User.query.filter(User.username == username, User.password == password).first()
#         if user:
#             session['user_id'] = user.id
#             session.permanent = True
#             return redirect(url_for('main.index'))
#         else:
#             return redirect(url_for('main.regist'))


@main.route("/logout/")
def logout():
    # session.clear
    # session.pop('user_id')
    del session['user_id']
    return redirect(url_for('main.login'))


@main.route('/regist/', methods=["GET", "POST"])
def regist():
    re_form = RegistFrom()
    if re_form.validate_on_submit():
        user = User.query.filter(User.telephone == re_form.telephone.data).first()

        if user:
            return '该用户已注册'
        else:
            user = User(telephone=re_form.telephone.data, username=re_form.username.data,
                        password=re_form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.login'))
    return render_template('regist1.html', form=re_form)


@main.route('/report/')
def report():
    return render_template('he-report.html')


def excel_rd(path_xl):
    data_sample = pd.read_excel(path_xl, sep='/t', encoding='utf-8')
    df = DataFrame(data_sample)
    return df


@main.route('/heinfo/', methods=['GET', 'POST'])
def heinfo():
    filename = None
    up_form = SeqGroupForm()
    if up_form.validate_on_submit():
        for filename in request.files.getlist('filezip'):
            filezips.save(filename)
        print(os.listdir(current_app.config['UPLOADED_ZIPFILE_DEST']))
    return render_template('seqinfo.html', form=up_form, filename=filename)


# @main.route('/regist1/', methods=["GET", "POST"])
# def regist1():
#     if request.method == 'GET':
#         return render_template('regist.html')
#     else:
#         telephone = request.form.get('telephone')
#         username = request.form.get('username')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')
#         user = User.query.filter(User.telephone == telephone).first()
#
#         if user:
#             return '该用户已注册'
#         else:
#             if password1 != password2:
#                 return '两次输入的密码不一样，请重新输入'
#             else:
#                 user = User(telephone=telephone, username=username, password=password2)
#                 db.session.add(user)
#                 db.session.commit()
#                 return redirect(url_for('main.login'))


@main.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


