from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from import_export.admin import ImportExportModelAdmin
from .forms import *

# Register your models here.


class MyUserAdmin(BaseUserAdmin):

    model = MyUser
    list_display = ['email', 'entite', 'is_staff']
    ordering = ('email',)


admin.site.register(MyUser)
