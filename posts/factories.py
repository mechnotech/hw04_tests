import factory

from .models import User, Post


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = str(first_name) + str(last_name)
    email = factory.LazyAttribute(lambda o: f'{o.username}@example.com')
    password = factory.Faker('sentence', nb_words=1)


class PostFactory(factory.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    text = factory.Faker('sentence', nb_words=25)
