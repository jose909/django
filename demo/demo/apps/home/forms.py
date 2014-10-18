from django import forms
from django.contrib.auth.models import User 

class ContactForm(forms.Form):
	Email = forms.EmailField(widget=forms.TextInput())
	Titulo = forms.CharField(widget=forms.TextInput())
	Texto = forms.CharField(widget=forms.Textarea())


class loginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))


class RegisterForm(forms.Form):
	username = forms.CharField(label="Nombre de Usuario",widget=forms.TextInput())
	email = forms.EmailField(label="Correo Electronico",widget=forms.TextInput())
	password_one = forms.CharField(label="Password",widget=forms.PasswordInput(render_value=False))
	password_two = forms.CharField(label="Confirmar Password",widget=forms.PasswordInput(render_value=False))

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			u = User.objects.get(username=username)
		except User.DoesNotExit:
			return	username
		raise forms.validationError('Nombre de usuario ua exixte')	

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			u = User.objects.get(email=email)
		except User.DoesNotExit:
			return	email
		raise forms.validationError('Email ya registrado')		

	def clean_password_two(self):
		password_one = self.cleaned_data['password_one']
		password_two = self.cleaned_data['password_two']
		if password_one ==password_two:
			pass
		else:
			raise forms.validationError('password no coinciden')