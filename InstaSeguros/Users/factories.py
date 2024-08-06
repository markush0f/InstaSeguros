import factory
from .models import User

# https://www.youtube.com/watch?v=SmNRdK0OB_I


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birth = factory.Faker("date_of_birth")
