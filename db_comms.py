from blogpost.models import CustomUser

users = CustomUser.objects.all()
for user in users:
    print(user)