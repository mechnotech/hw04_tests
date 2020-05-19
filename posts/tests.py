from django.test import Client, TestCase

from .factories import UserFactory, PostFactory, reset_factory_random


class UsersTest(TestCase):
    """
    После регистрации пользователя создается его
    персональная cтраница (profile)
    """

    def setUp(self):
        self.client = Client()

    def test_profile(self):
        reset_factory_random()
        self.users = UserFactory.build_batch(10)
        for user in self.users:
            response = self.client.get(f'/{user.username}/')
            with self.subTest(f'Профиль пользователя {user.username}'
                              f'появился до создания учетной записи!'):
                self.assertEqual(response.status_code, 404)

        reset_factory_random()
        self.users = UserFactory.create_batch(10)
        for user in self.users:
            response = self.client.get(f'/{user.username}/')
            with self.subTest(f'Страница профиля пользователя {user.username}'
                              f' не создается при создании учетной записи!'):
                self.assertEqual(response.status_code, 200)


class UserNewPostTest(TestCase):
    """
    1) Авторизованный пользователь может опубликовать пост (new),
    2) Неавторизованный посетитель не может опубликовать пост (его
    редиректит на страницу входа)
    """

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create()
        self.records = PostFactory.build_batch(15, author=self.user)

    def test_user_new_post(self):
        self.client.force_login(self.user)
        for record in self.records:
            response = self.client.post('/new/',
                                        data={'author': self.user,
                                              'text': record.text},
                                        follow=True)
            with self.subTest('Ошибка темплейта или формы /new/'):
                self.assertEqual(response.status_code, 200)
        post = self.user.posts.filter(author=self.user).last()
        with self.subTest('Пост не попадает в базу данных (/new/)'):
            self.assertEqual(post.text, self.records[-1].text)

    def test_unauthorized_new_post(self):
        response = self.client.get('/new/')
        target = '/auth/login/?next=/new/'
        with self.subTest(
                f'Проверить редирект на страницу логина для неавторизованного '
                f'пользователя {self.user.username} со страницы /new/'):
            self.assertRedirects(response, target,
                                 status_code=302,
                                 target_status_code=200,
                                 fetch_redirect_response=True)


class NewPostVisibleTest(TestCase):
    """
    После публикации поста новая запись появляется на главной
    транице сайта (index), на персональной странице пользователя (
    profile), и на отдельной странице поста (post)
    """

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create()
        self.record = PostFactory.build(author=self.user)

    def test_new_post_main_visible(self):
        response = self.client.get('/')
        with self.subTest('Запись появилась на главной до публикации!'):
            self.assertNotContains(response, self.record.text, status_code=200,
                                   html=True)
        self.client.force_login(self.user)
        self.client.post('/new/', data={'author': self.user,
                                        'text': self.record.text})
        response = self.client.get('/')
        with self.subTest('Записи нет на главной странице'):
            self.assertContains(response, self.record.text, status_code=200,
                                html=True)

    def test_new_post_profile_visible(self):
        response = self.client.get(f'/{self.user}/')
        with self.subTest('Запись появилась в профиле до публикации!'):
            self.assertNotContains(response, self.record.text, status_code=200,
                                   html=True)
        self.client.force_login(self.user)
        self.client.post('/new/', data={'author': self.user,
                                        'text': self.record.text})
        response = self.client.get(f'/{self.user}/')
        with self.subTest('Записи нет в профиле'):
            self.assertContains(response, self.record.text, status_code=200,
                                html=True)

    def test_new_post_own_page_visible(self):
        url = f'/{self.user}/1/'
        response = self.client.get(url)
        with self.subTest(f'Запись появляется до публикации! {url}'):
            self.assertNotContains(response, self.record.text, status_code=404,
                                   html=True)
        self.client.force_login(self.user)
        self.client.post('/new/', data={'author': self.user,
                                        'text': self.record.text})
        response = self.client.get(url)
        with self.subTest(f'Записи нет на странице поста {url}'):
            self.assertContains(response, self.record.text, status_code=200)


class UserCanEditPostTest(TestCase):
    """
    Авторизованный пользователь может отредактировать свой пост и его
    содержимое изменится на всех связанных страницах
    """

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create()
        self.client.force_login(self.user)
        self.record = PostFactory(author=self.user)
        self.client.post('/new/', data={'author': self.user,
                                        'text': self.record.text})
        self.add_text = '+ edited text 0001'

    def test_edit_post_to_main(self):
        text = self.record.text + self.add_text
        edit_path = f'/{self.user}/{self.record.pk}/edit'
        self.client.post(edit_path, data={'author': self.user, 'text': text})

        with self.subTest('Редактированной записи нет на главной'):
            response = self.client.get('/')
            self.assertContains(response, self.add_text, status_code=200)

    def test_edit_post_to_profile(self):
        text = self.record.text + self.add_text
        edit_path = f'/{self.user}/{self.record.pk}/edit'
        self.client.post(edit_path, data={'author': self.user, 'text': text})

        with self.subTest('Редактированной записи нет в профиле'):
            response = self.client.get(f'/{self.user}/')
            self.assertContains(response, self.add_text, status_code=200)

    def test_edit_post_to_postpage(self):
        text = self.record.text + self.add_text
        edit_path = f'/{self.user}/{self.record.pk}/edit'
        self.client.post(edit_path, data={'author': self.user, 'text': text})

        with self.subTest('Редактированной записи нет на странице поста'):
            response = self.client.get(f'/{self.user}/{self.record.pk}/')
            self.assertContains(response, self.add_text, status_code=200)
