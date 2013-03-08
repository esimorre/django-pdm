from django.contrib import databrowse
from models import *

databrowse.site.register(Product)
databrowse.site.register(Document)
databrowse.site.register(ProductDocumentation)