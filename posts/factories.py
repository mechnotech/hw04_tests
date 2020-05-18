import factory
import random
from .models import User, Post


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User


    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')


class PostFactory(factory.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    text = factory.Faker('sentence', nb_words=1000+6000*random.random())
