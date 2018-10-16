from . import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __reper__(seif):
        return '<Note %r>' %seif.body


class HeInfo(db.Model):
    __tablename__ = "heinfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mg_id = db.Column(db.String(50), nullable=False)
    scope_view = db.Column(db.String(500), nullable=False)
    pathology = db.Column(db.String(50), nullable=False)
    cell_c = db.Column(db.String(10), nullable=False)
    cell_p = db.Column(db.Integer, nullable=False)
    He_desc = db.Column(db.String(50), nullable=False)
    report_name = db.Column(db.String(10), nullable=False)

    def __reper__(seif):
        return '<Note %r>' % seif.body


class SampleInfo(db.Model):
    __tablename__ = "sampleinfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    序号 = db.Column(db.String(50), nullable=False)
    迈景编号 = db.Column(db.String(50), nullable=False)
    PI姓名 = db.Column(db.String(50), nullable=True)
    销售代表 = db.Column(db.String(50), nullable=True)
    申请单号 = db.Column(db.String(50), nullable=True)
    患者姓名 = db.Column(db.String(50), nullable=True)
    病人性别 = db.Column(db.String(50), nullable=True)
    病人年龄 = db.Column(db.String(50), nullable=True)
    民族 = db.Column(db.String(50), nullable=True)
    籍贯 = db.Column(db.String(50), nullable=True)
    检测项目 = db.Column(db.String(50), nullable=True)
    病人联系方式 = db.Column(db.String(50), nullable=True)
    病人身份证号码 = db.Column(db.String(50), nullable=True)
    病人地址 = db.Column(db.String(50), nullable=True)
    门诊住院号 = db.Column(db.String(50), nullable=True)
    医生姓名 = db.Column(db.String(50), nullable=True)
    医院名称 = db.Column(db.String(50), nullable=True)
    科室 = db.Column(db.String(50), nullable=True)
    病理号 = db.Column(db.String(50), nullable=True)
    临床诊断 = db.Column(db.String(500), nullable=True)
    临床诊断日期 = db.Column(db.String(50), nullable=True)
    病理诊断 = db.Column(db.String(500), nullable=True)
    病理诊断日期 = db.Column(db.String(50), nullable=True)
    病理样本收到日期 = db.Column(db.String(50), nullable=True)
    组织大小 = db.Column(db.String(50), nullable=True)
    病理审核 = db.Column(db.String(500), nullable=True)
    标本内细胞总量 = db.Column(db.String(50), nullable=True)
    肿瘤细胞含量 = db.Column(db.String(50), nullable=True)
    特殊说明 = db.Column(db.String(50), nullable=True)
    是否接受化疗 = db.Column(db.String(50), nullable=True)
    化疗开始时间 = db.Column(db.String(50), nullable=True)
    化疗结束时间 = db.Column(db.String(50), nullable=True)
    化疗治疗效果 = db.Column(db.String(50), nullable=True)
    是否靶向药治疗 = db.Column(db.String(50), nullable=True)
    靶向药治疗开始时间 = db.Column(db.String(50), nullable=True)
    靶向药治疗结束时间 = db.Column(db.String(50), nullable=True)
    靶向药治疗治疗效果 = db.Column(db.String(50), nullable=True)
    是否放疗 = db.Column(db.String(50), nullable=True)
    放疗开始时间 = db.Column(db.String(50), nullable=True)
    放疗结束时间 = db.Column(db.String(50), nullable=True)
    放疗治疗效果 = db.Column(db.String(50), nullable=True)
    有无家族遗传疾病 = db.Column(db.String(50), nullable=True)
    有无其他基因疾病 = db.Column(db.String(50), nullable=True)
    有无吸烟史 = db.Column(db.String(50), nullable=True)
    项目类型 = db.Column(db.String(50), nullable=True)
    样本来源 = db.Column(db.String(50), nullable=True)
    采样方式 = db.Column(db.String(50), nullable=True)
    样本类型 = db.Column(db.String(50), nullable=True)
    数量 = db.Column(db.String(50), nullable=True)
    运输方式 = db.Column(db.String(50), nullable=True)
    状态是否正常 = db.Column(db.String(50), nullable=True)
    送检人 = db.Column(db.String(50), nullable=True)
    送检日期 = db.Column(db.String(50), nullable=True)
    收样人 = db.Column(db.String(50), nullable=True)
    收样日期 = db.Column(db.String(50), nullable=True)
    检测日期 = db.Column(db.String(50), nullable=True)
    报告发出时间 = db.Column(db.String(50), nullable=True)
    报告收件人 = db.Column(db.String(50), nullable=True)
    联系电话 = db.Column(db.String(50), nullable=True)
    联系地址 = db.Column(db.String(50), nullable=True)
    备注 = db.Column(db.String(500), nullable=True)
    申请单病理报告扫描件命名 = db.Column(db.String(50), nullable=True)
    不出报告原因 = db.Column(db.String(200), nullable=True)
    录入 = db.Column(db.String(50), nullable=True)
    审核 = db.Column(db.String(50), nullable=True)

    def __reper__(seif):
        return '<Note %r>' % seif.body