import random

import factory.random

from .models import User, Post


def reset_factory_random():
    factory.random.reseed_random('Yatube project salt 3ef42b5001a')


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
    text = factory.Faker('sentence', nb_words=1000 + 6000 * random.random())


reset_factory_random()
