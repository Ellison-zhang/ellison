from app01 import models
from django import forms
from django.core.exceptions import ValidationError
import hashlib


class RegForm(forms.ModelForm):
	password = forms.CharField(min_length=6,widget=forms.PasswordInput(attrs={'placeholder': '您的密码'}))
	re_password = forms.CharField(min_length=6,widget=forms.PasswordInput(attrs={'placeholder': '确认您的密码'}))

	class Meta:
		model = models.UserProfile
		fields = '__all__'  # ['字段名']  显示的字段
		exclude = ['is_active']		# 排除的字段

		widgets = {
			'username': forms.TextInput(attrs={'placeholder': '您的用户名','oncontextmenu':"return false"}),
			'name': forms.TextInput(attrs={'placeholder': '您的真实姓名'}),
			'mobile': forms.TextInput(attrs={'placeholder': '您的手机号'}),
		}

		error_messages = {
			'username': {'invalid': '请输入正确的邮箱地址'}
		}

	def clean(self):
		# 获取到两次密码
		password = self.cleaned_data.get('password')
		re_password = self.cleaned_data.get('re_password')
		if password == re_password and password and re_password:
			# 加密后返回
			md5 = hashlib.md5()
			md5.update(password.encode('utf-8'))
			password = md5.hexdigest()
			self.cleaned_data['password'] = password
			# 返回所有数据
			return self.cleaned_data
		# 抛出异常
		self.add_error('re_password','两次密码不一致!!')
		raise ValidationError('两次密码不一致')

