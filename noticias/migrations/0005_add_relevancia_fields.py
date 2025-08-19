# Generated manually to add relevancia fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0004_add_destaque_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticia',
            name='relevancia_score',
            field=models.FloatField(default=0.0, verbose_name='Score de Relevância'),
        ),
        migrations.AddField(
            model_name='noticia',
            name='palavras_chave',
            field=models.TextField(blank=True, verbose_name='Palavras-chave Extraídas'),
        ),
    ]
