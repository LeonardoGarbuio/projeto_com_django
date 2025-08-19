# Generated manually to add destaque field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0003_update_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticia',
            name='destaque',
            field=models.BooleanField(default=False, verbose_name='Notícia em Destaque'),
        ),
    ]
