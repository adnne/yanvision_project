# Generated by Django 4.1.1 on 2022-09-06 17:01

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogtagindexpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], use_json_field=False),
        ),
    ]
