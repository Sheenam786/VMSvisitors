from django.contrib import admin
from .models import Receptionist, Visitor, VisitReason


# Register your models here.
admin.site.register((Receptionist, Visitor, VisitReason))