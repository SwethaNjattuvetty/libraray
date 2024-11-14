from django.contrib import admin
from users.models import Users

admin.site.register(Users)
# Register your models here.cd l

from users.models import CustomUser

admin.site.register(CustomUser)


