from django.test import TestCase
from django.urls import reverse

from .factories import PostFactory, UserFactory, reset_factory_random, \
    get_random_url


class UsersTest(TestCase):
    """
    После регистрации пользователя создается его
    персональная cтраница (profile)
    """

    def setUp(self):
        reset_factory_random()

    def test_profile_exist(self):
        self.users = UserFactory.build_batch(10)
        for user in self.users:
            url = reverse('profile', args=[user.username])
            response = self.client.get(url)
            with self.subTest(f'Профиль пользователя {user.username}'
                              'появился до создания учетной записи!'):
                self.assertEqual(response.status_code, 404)

    def test_profile_create(self):
        self.users = UserFactory.create_batch(10)
        for user in self.users:
            url = reverse('profile', args=[user.username])
            response = self.client.get(url)
            with self.subTest(f'Страница профиля пользователя {user.username}'
                              ' не создается при создании учетной записи!'):
                self.assertEqual(response.status_code, 200)


class NewPostTest(TestCase):
    """
    1) Авторизованный пользователь может опубликовать пост (new),
    2) Неавторизованный посетитель не может опубликовать пост (его
    редиректит на страницу входа)
    """

    def setUp(self):
        self.user = UserFactory.create()
        self.records = PostFactory.build_batch(15, author=self.user)
        self.url = reverse('new_post')
        self.login_target = reverse('login') + '?next=' + self.url
        self.index_target = reverse('index')

    def test_user_new_post(self):
        self.client.force_login(self.user)

        for record in self.records:
            response = self.client.post(self.url, {'text': record.text},
                                        follow=True)
            with self.subTest(f'После создания поста, должно редиректить'
                              f' на главную {self.index_target}'):
                self.assertRedirects(response, self.index_target,
                                     status_code=302,
                                     target_status_code=200,
                                     fetch_redirect_response=True)

        post = self.user.posts.filter(author=self.user).last()
        with self.subTest(f'Посты не попадают в базу данных из {self.url}'):
            self.assertEqual(post.text, self.records[-1].text)

    def test_unauthorized_new_post(self):
        response = self.client.get(self.url)
        with self.subTest('Проверить редирект на страницу логина '
                          f'{self.login_target} для неавторизованного'
                          f' пользователя со страницы {self.url}'):
            self.assertRedirects(response, self.login_target,
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
        self.user = UserFactory.create()
        self.record = PostFactory.build(author=self.user)
        self.index_url = reverse('index')
        self.new_url = reverse('new_post')
        self.client.force_login(self.user)

    def test_already_exist(self):
        response = self.client.get(self.index_url)
        with self.subTest('Исходная база не пустая, '
                          f'на главной {self.index_url} есть записи!'):
            self.assertEqual(len(response.context['page']), 0)

    def test_new_post_main_visible(self):
        self.client.post(self.new_url, {'text': self.record.text})
        response = self.client.get(self.index_url)
        with self.subTest(f'Записи нет на главной {self.index_url} после'
                          ' публикации'):
            self.assertEqual(response.context['page'][0].text,
                             self.record.text)

    def test_new_post_profile_visible(self):
        url = reverse('profile', args=[self.user])
        self.client.post(self.new_url, {'text': self.record.text})
        response = self.client.get(url)
        with self.subTest(f'Записи нет в профиле {url} после публикации'):
            self.assertEqual(response.context['page'][0].text,
                             self.record.text)

    def test_new_post_own_page_visible(self):
        url = reverse('post_detail', args=[self.user, 1])
        self.client.post(self.new_url, {'text': self.record.text})
        response = self.client.get(url)
        with self.subTest(f'Записи нет на странице поста {url} '
                          'после публикации'):
            self.assertEqual(response.context['post'].text,
                             self.record.text)


class UserCanEditPostTest(TestCase):
    """
    Авторизованный пользователь может отредактировать свой пост и его
    содержимое изменится на всех связанных страницах
    """

    def setUp(self):
        reset_factory_random()
        self.user = UserFactory.create()
        self.client.force_login(self.user)
        self.record = PostFactory(author=self.user)
        self.new_url = reverse('new_post')
        self.add_text = '+ edited text 0001'
        self.changed_text = self.record.text + self.add_text
        self.edit_url = reverse('post_edit', args=[self.user, self.record.pk])

    def test_edit_post_to_main(self):
        url = reverse('index')
        self.client.post(self.edit_url, {'text': self.changed_text})
        response = self.client.get(url)
        with self.subTest(f'Редактированной записи нет на главной {url}'):
            self.assertEqual(response.context['page'][0].text,
                             self.changed_text)

    def test_edit_post_to_profile(self):
        url = reverse('profile', args=[self.user])
        self.client.post(self.edit_url, {'text': self.changed_text})
        response = self.client.get(url)
        with self.subTest(f'Редактированной записи нет в профиле {url}'):
            self.assertEqual(response.context['page'][0].text,
                             self.changed_text)

    def test_edit_post_to_postpage(self):
        self.client.post(self.edit_url, {'text': self.changed_text})
        url = reverse('post_detail', args=[self.user, self.record.pk])
        response = self.client.get(url)
        with self.subTest(f'Редактированной записи нет на странице'
                          f' поста {url}'):
            self.assertEqual(response.context['post'].text,
                             self.changed_text)


class HTTPErrorsTest(TestCase):
    """
    Сервер возвращает коды ошибки, если страница не найдена.
    """
    def setUp(self):
        self.url = get_random_url()
        self.response = self.client.get(self.url)

    def test_error404(self):
        with self.subTest(f'Открытие неизвестной станицы {self.url} не '
                          f'возвращает ошибку 404'):
            self.assertEqual(self.response.status_code, 404)
