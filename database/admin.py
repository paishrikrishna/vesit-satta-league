from django.contrib import admin
from .models import login_model , fixture_model , prediction_model
# Register your models here.
admin.site.register(login_model)
admin.site.register(fixture_model)
admin.site.register(prediction_model)