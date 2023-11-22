from django.contrib import admin
# from django.contrib.auth.models import User

# superusers = User.objects.filter(is_superuser=True)
# for user in superusers:
#     print("Логин:", user.username)
#     print("Пароль:", user.password)

# Register your models here.
from .models import Question, Profile, Tag, Like, Answer

admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Answer)