# Generated manually to remove categoria field

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0005_add_relevancia_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noticia',
            name='categoria',
        ),
    ]
