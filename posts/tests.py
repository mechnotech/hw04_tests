from django.test import Client, TestCase

from posts.models import User

TEST_USERNAME = 'Test_User'


class ProfileTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username=TEST_USERNAME,
                                             email='test@test.com',
                                             password='12345ABCDEF')
        self.client.login(username=TEST_USERNAME, password='12345ABCDEF')

    def test_profile(self):
        """
        После регистрации пользователя создается его персональная
        страница (profile)
        """

        response = self.client.get(f'/{TEST_USERNAME}/')
        self.assertEqual(response.status_code, 200,
                         msg='Страница профиля пользователя не отображается!')

    def test_new_post_user(self):
        """
        Авторизованный пользователь может опубликовать пост (new)
        """
        text = 'Test text Test AAA 111'
        response = self.client.post('/new/',
                                    data={'author': self.user, 'text': text},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        post = self.user.posts.get(author=self.user, text=text)
        self.assertEqual(post.text, text,
                         msg='Пользователь не может созадать пост в (/new/)')
        return text, post

    def test_new_post_unauthorized(self):
        """
        Неавторизованный посетитель не может опубликовать пост (его
        редиректит на страницу входа)
        """
        self.tearDown()
        response = self.client.get('/new/')
        target = '/auth/login/?next=/new/'
        self.assertRedirects(response, target,
                             status_code=302,
                             target_status_code=200,
                             msg_prefix='Проверить переход на страницу логина',
                             fetch_redirect_response=True)

    def test_is_newpost_visible(self):
        """
        После публикации поста новая запись появляется на главной
        странице сайта (index), на персональной странице пользователя (
        profile), и на отдельной странице поста (post)
        """
        text, post = self.test_new_post_user()

        response = self.client.get('/')
        self.assertContains(response, text, count=None, status_code=200,
                            msg_prefix='Записи нет на главной', html=True)
        response = self.client.get(f'/{self.user}/')
        self.assertContains(response, text, count=None, status_code=200,
                            msg_prefix='Записи нет в профиле', html=True)
        response = self.client.get(f'/{self.user}/{post.pk}/')
        self.assertContains(response, text, count=None, status_code=200,
                            msg_prefix='Записи нет на станице поста',
                            html=False)

    def test_user_can_edit_post(self):
        """
        Авторизованный пользователь может отредактировать свой пост и его
        содержимое изменится на всех связанных страницах
        """
        text, post = self.test_new_post_user()
        text += ' edited data!'
        edit_path = f'/{self.user}/{post.pk}/edit'

        self.client.post(edit_path, data={'author': self.user, 'text': text},
                         follow=True)

        response = self.client.get('/')
        self.assertContains(response, text, count=None, status_code=200,
                            msg_prefix='Редактированной записи нет на главной',
                            html=True)
        response = self.client.get(f'/{self.user}/')
        self.assertContains(response, text, count=None, status_code=200,
                            msg_prefix='Редактированной записи нет в профиле',
                            html=True)
        response = self.client.get(f'/{self.user}/{post.pk}/')
        self.assertContains(response, text, count=None, status_code=200,
                            msg_prefix='Редактированной записи нет на '
                                       'станице поста',
                            html=False)

    def tearDown(self):
        self.client.logout()
