import random

import factory.random
from faker import Faker

from .models import Post, User


def reset_factory_random(seed='3ef42b5001a'):
    factory.random.reseed_random(f'Yatube project seed {seed}')


def get_random_url():
    fake = Faker()
    url = fake.pystr(10)
    return f'/{url}/'


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
    text = factory.Faker('sentence', nb_words=600 * random.random())
