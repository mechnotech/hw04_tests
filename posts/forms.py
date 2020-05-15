from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text']
        help_texts = {
            'group': 'Выбор группы (необязательно)',
            'text': 'Ваш текст',
        }
