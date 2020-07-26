from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')
        help_texts = {
            'group': 'Выбор группы (необязательно)',
            'text': 'Ваш текст',
            'image': 'Загрузите картинку (необязательно)',
        }
