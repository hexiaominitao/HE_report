import os, datetime
import pandas as pd
from pandas import DataFrame
from flask import render_template, redirect, session, url_for, request, current_app
from werkzeug import security
from sqlalchemy import create_engine

from . import main
from .. import db, filezips
from app.models import User
from .forms import LoginForm, SeqGroupForm, RegistFrom, PhotoForm, ReportInfoForm


@main.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


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
    df = get_info()
    status =df.loc[:,['申请单号', '病理诊断:']].values
    return render_template('report.html', status=status)


@main.route('/report/<report_id>')
def report_detail(report_id):
    df = get_info()
    # print((df[df['申请单号'] == 'MG1816390469'])['申请单号'].values)
    sample_id = (((report_id).split('=')[-1]).split(')')[0])
    def sample_info(item):
        if (df[df['申请单号'] == sample_id])[item].values:
            try:
                return str(float((df[df['申请单号'] == sample_id])[item].values))
            except:
                return ''.join((df[df['申请单号'] == sample_id])[item].values)
        else:
            return ' '

    def Time_set(get_time):
        T = get_time[0: 4] + '-' + get_time[4: 6] + '-' + get_time[6: 8]
        return T
    # print(sample_info('申请单号'))
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    return render_template('he-report.html', now=now, sample_info=sample_info, Time_set=Time_set)


def excel_rd(path_xl):
    data_sample = pd.read_excel(path_xl, sep='/t', encoding='utf-8')
    df = DataFrame(data_sample)
    return df


@main.route('/heinfo/', methods=['GET', 'POST'])
def heinfo():
    filename = None
    up_form = SeqGroupForm()
    # Report_form = ReportInfoForm()
    # 上传病理检测信息保存到数据库，并删除文件
    if up_form.validate_on_submit():
        for filename in request.files.getlist('filezip'):
            filezips.save(filename)
        path_zip = current_app.config['UPLOADED_ZIPFILE_DEST']
        for file in os.listdir(path_zip):
            data_sample = pd.read_excel(os.path.join(path_zip, file), sep='/t', encoding='utf-8')
            df = DataFrame(data_sample)
            ex_connect = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
            if '报告收件人' in df.columns:
                df.to_sql(name='sampleInfo', con=ex_connect, if_exists='replace', index=False)
            if '报告人' in df.columns:
                df.to_sql(name='seqInfo', con=ex_connect, if_exists='replace', index=False)
            os.remove(os.path.join(path_zip, file))
            # 提示上传成功
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


def get_info():
    sql1 = 'SELECT * FROM sampleInfo'
    sql2 = 'SELECT * FROM seqInfo'
    ex_connect = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    df1 = pd.read_sql(sql1, ex_connect)
    df2 = pd.read_sql(sql2, ex_connect)
    df3 = pd.DataFrame((df1[df1['申请单号'].isin(df2['申请单号'].values)]).values, index=df2.index, columns=df1.columns)
    df2.drop(['申请单号'], axis=1, inplace=True)
    df = df3.join(df2)
    return df
