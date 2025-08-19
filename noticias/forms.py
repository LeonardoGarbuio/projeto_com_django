from django import forms
from .models import Noticia

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'resumo', 'conteudo', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título da notícia'
            }),
            'resumo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Digite um resumo da notícia (máximo 500 caracteres)',
                'maxlength': '500'
            }),
            'conteudo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Digite o conteúdo completo da notícia'
            }),
            'imagem': forms.FileInput(attrs={
                'class': 'form-control',
                'required': 'required'
            })
        }
        labels = {
            'titulo': 'Título',
            'resumo': 'Resumo',
            'conteudo': 'Conteúdo',
            'imagem': 'Imagem de destaque para a notícia *'
        }
        help_texts = {
            'titulo': 'Digite um título atrativo e descritivo para a notícia',
            'resumo': 'Breve descrição que aparecerá na listagem de notícias (máximo 500 caracteres)',
            'conteudo': 'Conteúdo completo da notícia',
            'imagem': 'Imagem de destaque para a notícia (obrigatória)'
        }
