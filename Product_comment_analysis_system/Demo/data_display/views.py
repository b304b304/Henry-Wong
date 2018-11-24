from django.http import HttpResponse
from django.template import loader
import json

from .data import get_product_data


# Create your views here.
def index(request):
    pro_data = get_product_data()
    template = loader.get_template('index.html')
    return HttpResponse(template.render(pro_data, request))
