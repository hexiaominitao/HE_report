from flask_wtf import FlaskForm
from flask_wtf.file import DataRequired
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, EqualTo, Required
from flask_wtf.file import FileField, FileRequired, FileAllowed

from .. import filezips, photos


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('登录')


class RegistFrom(FlaskForm):
    telephone = StringField('电话号码', validators=[DataRequired(), Length(1, 11)])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128)])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password2')])
    submit = SubmitField('注册')


# filezip = UploadSet('zipfile', ARCHIVES)
# # configure_uploads(app, filezip)
# # patch_request_class(app)
class SeqGroupForm(FlaskForm):
    filezip = FileField('上传文件', validators=[FileRequired(), FileAllowed(filezips)])
    submit = SubmitField('上传')


class PhotoForm(FlaskForm):
    up_photo = FileField(validators=[FileRequired(), FileAllowed(photos)])
    submit = SubmitField('上传图片')

