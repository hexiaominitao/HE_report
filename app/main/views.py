import os, datetime

import pdfkit
import xlrd
import pandas as pd
from pandas import DataFrame
from flask import render_template, redirect, session, url_for, request, current_app, flash, g, send_from_directory
from werkzeug import security
from sqlalchemy import create_engine
from flask_restful import request as req

from . import main
from .. import db, filezips, photos
from app.models import User, HeInfo, SampleInfo
from .forms import LoginForm, SeqGroupForm, RegistFrom, PhotoForm


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


@main.route('/report/', methods=['GET', 'POST'])
def report():
    if request.method == 'GET':
        now = ''
    else:
        now = request.form.get('data')
    print('111{}111'.format(now))
    df = HeInfo.query.filter(HeInfo.病理报告时间.startswith(str(now))).all()
    status = []
    for i in df:
        status.extend([[i.申请单号, i.病理审核]])
    return render_template('report.html', status=status, now=now)


@main.route('/pdf/<filename>')
def report_download(filename):
    report_id = filename.strip('.pdf')
    pdffile = os.path.join(current_app.config['PDF_FILE'], filename)
    url_report = 'http://localhost:5000/report/{}'.format(report_id)
    pdfkit.from_url(url_report, pdffile)
    path = os.path.join(os.getcwd(),current_app.config['PDF_FILE'])
    return send_from_directory(path, filename=filename, as_attachment=True)


# @main.route('/imginfo/', methods=['GET', 'POST'])
# def imginfo():
#     img_form = PhotoForm()
#     if img_form.validate_on_submit():
#         for filename in request.files.getlist('up_photo'):
#             photos.save(filename)
#     return render_template('imginfo.html', img_form=img_form)


@main.route('/report/<report_id>')
def report_detail(report_id):
    def Time_set(get_time):
        T = get_time[0: 4] + '-' + get_time[4: 6] + '-' + get_time[6: 8]
        return T
    sample_info = HeInfo.query.filter(HeInfo.申请单号 == report_id).first()
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    url_report = str(req.url)  #得到当前网页的url
    return render_template('he-report.html', now=now, sample_info=sample_info, Time_set=Time_set)



def excel_rd(path_xl):
    data_sample = pd.read_excel(path_xl, sep='/t', encoding='utf-8')
    df = DataFrame(data_sample)
    return df


@main.route('/heinfo/', methods=['GET', 'POST'])
def heinfo():
    filename = None
    up_form = SeqGroupForm()
    img_form = PhotoForm()
    if request.method == 'GET':
        path_zip = current_app.config['UPLOADED_ZIPFILE_DEST']
        for file in os.listdir(path_zip):
            os.remove(os.path.join(path_zip, file))
    if img_form.validate_on_submit():
        for filename in request.files.getlist('up_photo'):
            photos.save(filename)
            flash('图片上传成功')

    def sample_info(item_sample):
        Value = rows[title_ex.index(item_sample)]
        if type(Value) is float:
            Value = int(Value)
        return str(Value)

    # Report_form = ReportInfoForm()
    # 上传病理检测信息保存到数据库，并删除文件
    if up_form.validate_on_submit():
        for filename in request.files.getlist('filezip'):
            filezips.save(filename)
        path_zip = current_app.config['UPLOADED_ZIPFILE_DEST']
        for file in os.listdir(path_zip):
            wb_e = xlrd.open_workbook(os.path.join(path_zip, file))
            table = wb_e.sheets()[0]
            title_ex = table.row_values(0)
            print(title_ex)
            id_sa = title_ex.index('迈景编号')
            cols = table.col_values(id_sa)
            cols.pop(0)

            # data_sample = pd.read_excel(os.path.join(path_zip, file), sep='/t', encoding='utf-8')
            # df = DataFrame(data_sample)
            # ex_connect = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
            if '报告收件人' in title_ex:
                # df.to_sql(name='sampleInfo', con=ex_connect, if_exists='replace', index=False)
                for sample_id in cols:
                    sam = cols.index(sample_id) + 1
                    rows = (table.row_values(sam))

                    samp_info = SampleInfo(序号=sample_info('序号'), 迈景编号=sample_info('迈景编号'),
                                           PI姓名=sample_info('PI姓名'),销售代表=sample_info('销售代表'),
                                           申请单号=sample_info('申请单号'), 患者姓名=sample_info('患者姓名'),
                                           病人性别=sample_info('病人性别'), 病人年龄=sample_info('病人年龄'),
                                           民族=sample_info('民族'),籍贯=sample_info('籍贯'),
                                           检测项目=sample_info('检测项目'), 病人联系方式=sample_info('病人联系方式'),
                                           病人身份证号码=sample_info('病人身份证号码'), 病人地址=sample_info('病人地址'),
                                           门诊住院号=sample_info('门诊/住院号'), 医生姓名=sample_info('医生姓名'),
                                           医院名称=sample_info('医院名称'), 科室=sample_info('科室'),
                                           病理号=sample_info('病理号'),临床诊断=sample_info('临床诊断'),
                                           临床诊断日期=sample_info('诊断日期'),病理诊断=sample_info('病理诊断'),
                                           病理诊断日期=sample_info('诊断日期'),
                                           病理样本收到日期=sample_info('病理样本收到日期'),
                                           组织大小=sample_info('组织大小（单位mm）'),
                                           病理审核=sample_info('病理审核'), 标本内细胞总量=sample_info('标本内细胞总量'),
                                           肿瘤细胞含量=sample_info('肿瘤细胞含量'), 特殊说明=sample_info('特殊说明'),
                                           是否接受化疗=sample_info('是否接受化疗'), 化疗开始时间=sample_info('开始时间'),
                                           化疗结束时间=sample_info('结束时间'), 化疗治疗效果=sample_info('治疗效果'),
                                           是否靶向药治疗=sample_info('是否靶向药治疗'),
                                           靶向药治疗开始时间=sample_info('开始时间'),
                                           靶向药治疗结束时间=sample_info('结束时间'),
                                           靶向药治疗治疗效果=sample_info('治疗效果'),
                                           是否放疗=sample_info('是否放疗'), 放疗开始时间=sample_info('起始时间'),
                                           放疗结束时间=sample_info('结束时间'), 放疗治疗效果=sample_info('治疗效果'),
                                           有无家族遗传疾病=sample_info('有无家族遗传疾病'),
                                           有无其他基因疾病=sample_info('有无其他基因疾病'),
                                           有无吸烟史=sample_info('有无吸烟史'), 项目类型=sample_info('项目类型'),
                                           样本来源=sample_info('样本来源'), 采样方式=sample_info('采样方式'),
                                           样本类型=sample_info('样本类型'),数量=sample_info('数量'),
                                           运输方式=sample_info('运输方式'), 状态是否正常=sample_info('状态是否正常'),
                                           送检人=sample_info('送检人'), 送检日期=sample_info('送检日期'),
                                           收样人=sample_info('收样人'),收样日期=sample_info('收样日期'),
                                           检测日期=sample_info('检测日期'),报告发出时间=sample_info('报告发出时间'),
                                           报告收件人=sample_info('报告收件人'),联系电话=sample_info('联系电话'),
                                           联系地址=sample_info('联系地址'), 备注=sample_info('备注'),
                                           申请单病理报告扫描件命名=sample_info('申请单、病理报告扫描件命名'),
                                           不出报告原因 = sample_info('不出报告原因'), 录入 = sample_info('录入'),
                                           审核 = sample_info('审核'))
                    if SampleInfo.query.filter(SampleInfo.迈景编号 == sample_id).first():
                        pass
                    else:
                        db.session.add(samp_info)
                        db.session.commit()
                        flash('成功上传样本信息登记表')
            if '报告人' in title_ex:
                # data_sample = pd.read_excel(os.path.join(pat
                for sample_id in cols:
                    sam = cols.index(sample_id) + 1
                    rows = (table.row_values(sam))
                    now = datetime.datetime.now().strftime('%Y-%m-%d')
                    hesamp_info = SampleInfo.query.filter(SampleInfo.迈景编号 == sample_info('迈景编号')).first()

                    hesample_info = HeInfo(序号=hesamp_info.序号, 迈景编号=hesamp_info.迈景编号,
                                           PI姓名=hesamp_info.PI姓名,
                                           销售代表=hesamp_info.销售代表,
                                           申请单号=hesamp_info.申请单号, 患者姓名=hesamp_info.患者姓名,
                                           病人性别=hesamp_info.病人性别, 病人年龄=hesamp_info.病人年龄,
                                           民族=hesamp_info.民族,籍贯=hesamp_info.籍贯,
                                           检测项目=hesamp_info.检测项目, 病人联系方式=hesamp_info.病人联系方式,
                                           病人身份证号码=hesamp_info.病人身份证号码, 病人地址=hesamp_info.病人地址,
                                           门诊住院号=hesamp_info.门诊住院号, 医生姓名=hesamp_info.医生姓名,
                                           医院名称=hesamp_info.医院名称, 科室=hesamp_info.科室,
                                           病理号=hesamp_info.病理号, 临床诊断=hesamp_info.临床诊断,
                                           临床诊断日期=hesamp_info.临床诊断日期,
                                           病理诊断=hesamp_info.病理诊断, 病理诊断日期=hesamp_info.病理诊断日期,
                                           病理样本收到日期=hesamp_info.病理样本收到日期, 组织大小=hesamp_info.组织大小,
                                           病理审核=sample_info('病理诊断'), 标本内细胞总量=sample_info('细胞总量'),
                                           肿瘤细胞含量=sample_info('肿瘤比例'), 特殊说明=sample_info('特殊说明'),
                                           镜下所见=sample_info('镜下所见'), 病理报告人=sample_info('报告人'),
                                           是否接受化疗=hesamp_info.是否接受化疗, 化疗开始时间=hesamp_info.化疗开始时间,
                                           化疗结束时间=hesamp_info.化疗结束时间, 化疗治疗效果=hesamp_info.化疗治疗效果,
                                           是否靶向药治疗=hesamp_info.是否靶向药治疗,
                                           靶向药治疗开始时间=hesamp_info.靶向药治疗开始时间,
                                           靶向药治疗结束时间=hesamp_info.靶向药治疗结束时间,
                                           靶向药治疗治疗效果=hesamp_info.靶向药治疗治疗效果,
                                           是否放疗=hesamp_info.是否放疗, 放疗开始时间=hesamp_info.放疗开始时间,
                                           放疗结束时间=hesamp_info.放疗结束时间,放疗治疗效果=hesamp_info.放疗治疗效果,
                                           有无家族遗传疾病=hesamp_info.有无家族遗传疾病,
                                           有无其他基因疾病=hesamp_info.有无其他基因疾病, 有无吸烟史=hesamp_info.有无吸烟史,
                                           项目类型=hesamp_info.项目类型, 样本来源=hesamp_info.样本来源,
                                           采样方式=hesamp_info.采样方式,样本类型=hesamp_info.样本类型,
                                           数量=hesamp_info.数量, 运输方式=hesamp_info.运输方式,
                                           状态是否正常=hesamp_info.状态是否正常, 送检人=hesamp_info.送检人,
                                           送检日期=hesamp_info.送检日期,收样人=hesamp_info.收样人,
                                           收样日期=hesamp_info.收样日期, 检测日期=hesamp_info.检测日期,
                                           报告发出时间=hesamp_info.报告发出时间, 报告收件人=hesamp_info.报告收件人,
                                           联系电话=hesamp_info.联系电话,联系地址=hesamp_info.联系地址,
                                           备注=hesamp_info.备注,
                                           申请单病理报告扫描件命名=hesamp_info.申请单病理报告扫描件命名,
                                           不出报告原因=hesamp_info.不出报告原因,
                                           录入=hesamp_info.录入, 审核=hesamp_info.审核, 病理报告时间=now)
                    if HeInfo.query.filter(HeInfo.迈景编号 == sample_id).first():

                        # db.session.add(HeInfo.query.filter(HeInfo.迈景编号 == sample_id).first())
                        # db.session.commit()
                        pass
                    else:
                        db.session.add(hesample_info)
                        db.session.commit()
                        flash('成功上传病理信息')
            os.remove(os.path.join(path_zip, file))
            # 提示上传成功
    return render_template('seqinfo.html', form=up_form, img_form=img_form, filename=filename)



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