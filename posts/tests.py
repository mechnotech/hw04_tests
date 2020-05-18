from django.test import Client, TestCase

from .factories import UserFactory, PostFactory


class ProfileTest(TestCase):
    """
    После регистрации пользователя создается его
    персональная cтраница (profile)
    """

    def setUp(self):
        self.client = Client()

    def test_profile(self):

        with self.subTest():
            pass
        self.users = UserFactory.create_batch(10)
        for user in self.users:
            response = self.client.get(f'/{user.username}/')
            with self.subTest(f'Страница профиля пользователя {user.username}'
                              f' не создается при создании учетной записи!'):
                self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.client.logout()


class NewPostTest(TestCase):
    """
    Авторизованный пользователь может опубликовать пост (new)
    """

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.client.login(username=self.user.username,
                          password=self.user.password)
        self.records = PostFactory.create_batch(10, author=self.user)

    def test_user_make_new_post(self):
        for record in self.records:
            response = self.client.post('/new/',
                                        data={'author': self.user,
                                              'text': record.text},
                                        follow=True)
            with self.subTest(f'Интерфейс /new/ ответил ошибкой'
                              f'для, входных данных:'
                              f' user {self.user.username}'):
                self.assertEqual(response.status_code, 200)
            post = self.user.posts.get(author=self.user,
                                       text=record.text)
            with self.subTest(f'Пост не попадает в базу данных из /new/  '
                              f'входные данные: '
                              f' user {self.user.username}'):
                self.assertEqual(post.text, record.text)

    def tearDown(self):
        self.client.logout()


class UnauthorizedUserPostTest(TestCase):
    """
    Неавторизованный посетитель не может опубликовать пост (его
    редиректит на страницу входа)
    """

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_new_post_unauthorized(self):
        self.tearDown()
        response = self.client.get('/new/')
        target = '/auth/login/?next=/new/'
        with self.subTest(
                f'Проверить переход на страницу логина для неавторизованного '
                f'пользователя {self.user.username} со страницы /new/'):
            self.assertRedirects(response, target,
                                 status_code=302,
                                 target_status_code=200,
                                 fetch_redirect_response=True)
    #
    # def test_is_newpost_visible(self):
    #     """
    #     После публикации поста новая запись появляется на главной
    #     странице сайта (index), на персональной странице пользователя (
    #     profile), и на отдельной странице поста (post)
    #     """
    #     text, post = self.test_new_post_user()
    #
    #     response = self.client.get('/')
    #     self.assertContains(response, text, count=None, status_code=200,
    #                         msg_prefix='Записи нет на главной', html=True)
    #     response = self.client.get(f'/{self.user}/')
    #     self.assertContains(response, text, count=None, status_code=200,
    #                         msg_prefix='Записи нет в профиле', html=True)
    #     response = self.client.get(f'/{self.user}/{post.pk}/')
    #     self.assertContains(response, text, count=None, status_code=200,
    #                         msg_prefix='Записи нет на станице поста',
    #                         html=False)
    #
    # def test_user_can_edit_post(self):
    #     """
    #     Авторизованный пользователь может отредактировать свой пост и его
    #     содержимое изменится на всех связанных страницах
    #     """
    #     text, post = self.test_new_post_user()
    #     text += ' edited data!'
    #     edit_path = f'/{self.user}/{post.pk}/edit'
    #
    #     self.client.post(edit_path, data={'author': self.user, 'text': text},
    #                      follow=True)
    #
    #     response = self.client.get('/')
    #     self.assertContains(response, text, count=None, status_code=200,
    #                         msg_prefix='Редактированной записи нет на главной',
    #                         html=True)
    #     response = self.client.get(f'/{self.user}/')
    #     self.assertContains(response, text, count=None, status_code=200,
    #                         msg_prefix='Редактированной записи нет в профиле',
    #                         html=True)
    #     response = self.client.get(f'/{self.user}/{post.pk}/')
    #     self.assertContains(response, text, count=None, status_code=200,
    #                         msg_prefix='Редактированной записи нет на '
    #                                    'станице поста',
    #                         html=False)
