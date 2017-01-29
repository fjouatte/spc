from django.contrib import admin
from spc.models import Edition, Map, Rules
from spc.forms import RulesForm, RulesFormAdmin

admin.site.register(Edition)
admin.site.register(Map)
admin.site.register(Rules)
