from django.test import Client, TestCase

from .factories import UserFactory, PostFactory, reset_factory_random


# class ProfileTest(TestCase):
#     """
#     После регистрации пользователя создается его
#     персональная cтраница (profile)
#     """
#
#     def setUp(self):
#         self.client = Client()
#
#     def test_profile(self):
#         reset_factory_random()
#         self.users = UserFactory.build_batch(10)
#         for user in self.users:
#             response = self.client.get(f'/{user.username}/')
#             with self.subTest(f'Профиль пользователя {user.username}'
#                               f'появился до создания учетной записи!'):
#                 self.assertEqual(response.status_code, 404)
#
#         reset_factory_random()
#         self.users = UserFactory.create_batch(10)
#         for user in self.users:
#             response = self.client.get(f'/{user.username}/')
#             with self.subTest(f'Страница профиля пользователя {user.username}'
#                               f' не создается при создании учетной записи!'):
#                 self.assertEqual(response.status_code, 200)

#
# class UserNewPostTest(TestCase):
#     """
#     1) Авторизованный пользователь может опубликовать пост (new),
#     2) Неавторизованный посетитель не может опубликовать пост (его
#     редиректит на страницу входа)
#     """
#
#     def setUp(self):
#         self.client = Client()
#         self.user = UserFactory.create()
#         self.records = PostFactory.build_batch(15, author=self.user)
#
#     def test_user_new_post(self):
#         self.client.force_login(self.user)
#         for record in self.records:
#             responce = self.client.post('/new/',
#                                         data={'author': self.user,
#                                               'text': record.text},
#                                         follow=True)
#             with self.subTest('Ошибка темплейта или формы /new/'):
#                 self.assertEqual(responce.status_code, 200)
#         post = self.user.posts.filter(author=self.user).last()
#         with self.subTest('Пост не попадает в базу данных (/new/)'):
#             self.assertEqual(post.text, self.records[-1].text)
#
#     def test_unauthorized_new_post(self):
#         response = self.client.get('/new/')
#         target = '/auth/login/?next=/new/'
#         with self.subTest(
#                 f'Проверить редирект на страницу логина для неавторизованного '
#                 f'пользователя {self.user.username} со страницы /new/'):
#             self.assertRedirects(response, target,
#                                  status_code=302,
#                                  target_status_code=200,
#                                  fetch_redirect_response=True)


class UserNewPostTest(TestCase):
    """
    После публикации поста новая запись появляется на главной
    транице сайта (index), на персональной странице пользователя (
    profile), и на отдельной странице поста (post)
    """

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create()
        self.client.force_login(self.user)
        self.record = PostFactory(author=self.user)
        self.client.post('/new/', data={'author': self.user,
                                        'text': self.record.text})
        print(self.record.text)

    def new_post_main_visible_test(self):
        response = self.client.get('/')
        self.assertContains(response, self.record.text, status_code=200,
                            msg_prefix='Записи нет на главной', html=True)
        print(self.record.text)

    def new_post_profile_visible_test(self):
        response = self.client.get(f'/{self.user}/')
        self.assertContains(response, self.record.text, status_code=200,
                            msg_prefix='Записи нет в профиле', html=True)
        print(self.record.text)

    def new_post_own_page_visible_test(self):
        response = self.client.get(f'/{self.user}/{self.record.pk}/')
        self.assertContains(response, self.record.text, count=None,
                            status_code=200,
                            msg_prefix='Записи нет на станице поста',
                            html=False)
        print(self.record.text)

    # def tearDown(self):
    #     self.client.logout()

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
