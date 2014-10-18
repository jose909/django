# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from demo.apps.ventas.models import producto
from demo.apps.home.forms import ContactForm,loginForm,RegisterForm
from django.core.mail import EmailMultiAlternatives #Enviamos Html

from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
#paginacio en django
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.contrib.auth.models import User
import django
from django.contrib.auth.decorators import login_required
from demo.settings import URL_LOGIN

def index_view(request):

		return render_to_response('home/index.html',context_instance=RequestContext(request))

@login_required(login_url=URL_LOGIN)
def about_view(request):
	version = django.get_version()
	mensaje= "esto es un mensaje desde mi vista"
	ctx = {'msg':mensaje,'version':version}
	return render_to_response('home/about.html',ctx,context_instance=RequestContext(request))
	
@login_required(login_url=URL_LOGIN)
def productos_view(request,pagina):
	lista_prod = producto.objects.filter(status=True) #select * from ventas_productos where status = True
	paginator = Paginator(lista_prod,3)#cuanto productos quiere por pagina? = 3
	try:
		page = int(pagina)
	except:
		page = 1 	
	try:
		 productos = paginator.page(page)
	except (Emptypage,InvalidPage):
		productos = paginator.page(paginator.num_pages)
	ctx = {'productos':productos}
	return render_to_response('home/productos.html',ctx,context_instance=RequestContext(request))


def singleProduct_view(request,id_prod):
	prod = producto.objects.get(id=id_prod)
	cats = prod.categorias.all()# Obteniendo las categorias del producto encontrado
	ctx = {'producto':prod,'categorias':cats} 
	return render_to_response('home/SingleProducto.html',ctx,context_instance=RequestContext(request))


@login_required(login_url=URL_LOGIN)
def contacto_view(request):
	info_enviado = False 
	email = " "
	titulo = ""
	texto = ""
	if request.method == "POST":
		formulario = ContactForm(request.POST)
		if formulario.is_valid():
			info_enviado = True
			email = formulario.cleaned_data['Email']
			titulo = formulario.cleaned_data['Titulo']
			texto = formulario.cleaned_data['Texto']
			
			#Configuracion enviado mensaje via live
			to_admin = 'rosaleayal19@hotmail.com'
			html_content = "Informacio recibida [%s]<br><br><br>***Mensaje***<br><br>%s"%(email,texto)
			msg = EmailMultiAlternatives('Correo de Contacto',html_content,'from@server.com',[to_admin])
			msg.attach_alternative(html_content,'text/html')#definimos el contenido como HTML
			msg.send()
	else:		
		formulario = ContactForm()
	ctx = { 'form':formulario,'email':email,'titulo':titulo,'texto':texto,'info_enviado':info_enviado}
	return render_to_response('home/contacto.html',ctx,context_instance=RequestContext(request))





def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
			return HttpResponseRedirect('/')
	else:
			if request.method =="POST":
				form = loginForm(request.POST)
				if form.is_valid():
					next = request.POST['next']
					username = form.cleaned_data['username']
					password = form.cleaned_data['password']
					usuario = authenticate(username=username,password=password)
					if usuario is not None and usuario.is_active:
						login(request,usuario)
						return HttpResponseRedirect(next)
					else:	
						mensaje="usuario y/o password incorrecto"
			next = request.REQUEST.get('next')
			form = loginForm()			
			ctx = {'form':form,'mensaje':mensaje,'next':next}
			return render_to_response('home/login.html',ctx,context_instance=RequestContext(request))


def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def register_view(request):
	form = RegisterForm()
	if request.method =="POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			u = User.objects.create_user(username=usuario,email=email,password=password_one)
			u.save()
			return render_to_response('home/thanks_register.html',context_instance=RequestContext(request))
		else:
			ctx = {'form':form}
			return render_to_response('home/register.html',ctx,context_instance=RequestContext(request))
			
	ctx = {'form':form}
	return render_to_response('home/register.html',ctx,context_instance=RequestContext(request))
