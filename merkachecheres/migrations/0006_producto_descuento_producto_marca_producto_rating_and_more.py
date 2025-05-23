# Generated by Django 5.1.1 on 2025-04-03 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merkachecheres', '0005_remove_producto_imagen_imagenproducto'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='descuento',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='marca',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='rating',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='stock',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
