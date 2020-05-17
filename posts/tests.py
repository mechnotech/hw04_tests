from django.test import Client, TestCase

from .factories import UserFactory


class ProfileTest(TestCase):
    """
    После регистрации пользователя создается его
    персональная cтраница (profile)
    """

    def setUp(self):
        self.client = Client()

    def test_profile(self):
        self.users = UserFactory.create_batch(10)
        for user in self.users:
            self.client.login(username=user.username,
                              password=user.password)

            response = self.client.get(f'/{user.username}/')
            print(user.first_name, user.last_name)
            self.assertEqual(response.status_code, 200,
                         msg='Страница профиля пользователя не создается!')


    # def test_new_post_user(self):
    #     """
    #     Авторизованный пользователь может опубликовать пост (new)
    #     """
    #     text = 'Test text Test AAA 111'
    #     response = self.client.post('/new/',
    #                                 data={'author': self.user, 'text': text},
    #                                 follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     post = self.user.posts.get(author=self.user, text=text)
    #     self.assertEqual(post.text, text,
    #                      msg='Пользователь не может созадать пост в (/new/)')
    #     return text, post
    #
    # def test_new_post_unauthorized(self):
    #     """
    #     Неавторизованный посетитель не может опубликовать пост (его
    #     редиректит на страницу входа)
    #     """
    #     self.tearDown()
    #     response = self.client.get('/new/')
    #     target = '/auth/login/?next=/new/'
    #     self.assertRedirects(response, target,
    #                          status_code=302,
    #                          target_status_code=200,
    #                          msg_prefix='Проверить переход на страницу логина',
    #                          fetch_redirect_response=True)
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

    def tearDown(self):
        self.client.logout()
