# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

def add_product_view(request):

	return render_to_response('ventas/addProducto.html',context_instance=RequestContext(request))
