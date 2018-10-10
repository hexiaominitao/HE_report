from flask_wtf import FlaskForm
from flask_wtf.file import DataRequired
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, EqualTo, Required
from flask_wtf.file import FileField, FileRequired, FileAllowed

from .. import filezips


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('登录')


class RegistFrom(FlaskForm):
    telephone = StringField('Username', validators=[DataRequired(), Length(1, 11)])
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password2')])
    submit = SubmitField('注册')


# filezip = UploadSet('zipfile', ARCHIVES)
# # configure_uploads(app, filezip)
# # patch_request_class(app)
class SeqGroupForm(FlaskForm):
    filezip = FileField('上传文件', validators=[FileRequired(), FileAllowed(filezips)])
    submit = SubmitField('病理结果上传')


class ReportInfoForm(FlaskForm):
    filezip = FileField('上传文件', validators=[FileRequired(), FileAllowed(filezips)])
    submit = SubmitField('样本信息上传')


class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('上传')
