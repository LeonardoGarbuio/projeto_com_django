# Generated manually to fix categoria field issue

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticia',
            name='categoria',
            field=models.CharField(
                max_length=20,
                default='geral',
                verbose_name='Categoria'
            ),
        ),
    ]
