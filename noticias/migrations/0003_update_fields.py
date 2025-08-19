# Generated manually to update model fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0002_add_categoria_temp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='resumo',
            field=models.TextField(max_length=500, verbose_name='Resumo'),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='imagem',
            field=models.ImageField(blank=False, null=False, upload_to='noticias/', verbose_name='Imagem da Notícia'),
        ),
    ]
