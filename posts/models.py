from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Название группы',
                             max_length=200,
                             unique=True,
                             help_text='Название группы '
                                       '(не более 200 символов)')
    slug = models.SlugField('Cсылка',
                            max_length=200,
                            unique=True,
                            help_text='https://myblog.com/groups/ "cсылка на'
                                      ' Вашу группу" (не более 200 символов)')
    description = models.TextField('Описание группы',
                                   help_text='Опишите Вашу группу тут')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              related_name='posts', blank=True, null=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return self.text
