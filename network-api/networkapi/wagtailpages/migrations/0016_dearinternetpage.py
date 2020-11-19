# Generated by Django 2.2.16 on 2020-11-19 22:03

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtailmetadata.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('wagtailcore', '0052_pagelogentry'),
        ('wagtailpages', '0015_auto_20201116_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='DearInternetPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro_text_1', models.CharField(help_text='Intro text 1', max_length=500)),
                ('intro_text_1_en', models.CharField(help_text='Intro text 1', max_length=500, null=True)),
                ('intro_text_1_de', models.CharField(help_text='Intro text 1', max_length=500, null=True)),
                ('intro_text_1_pt', models.CharField(help_text='Intro text 1', max_length=500, null=True)),
                ('intro_text_1_es', models.CharField(help_text='Intro text 1', max_length=500, null=True)),
                ('intro_text_1_fr', models.CharField(help_text='Intro text 1', max_length=500, null=True)),
                ('intro_text_1_fy_NL', models.CharField(help_text='Intro text 1', max_length=500, null=True)),
                ('intro_text_1_nl', models.CharField(help_text='Intro text 1', max_length=500, null=True)),
                ('intro_text_1_pl', models.CharField(help_text='Intro text 1', max_length=500, null=True)),
                ('intro_text_2', models.CharField(help_text='Intro text 2', max_length=500)),
                ('intro_text_2_en', models.CharField(help_text='Intro text 2', max_length=500, null=True)),
                ('intro_text_2_de', models.CharField(help_text='Intro text 2', max_length=500, null=True)),
                ('intro_text_2_pt', models.CharField(help_text='Intro text 2', max_length=500, null=True)),
                ('intro_text_2_es', models.CharField(help_text='Intro text 2', max_length=500, null=True)),
                ('intro_text_2_fr', models.CharField(help_text='Intro text 2', max_length=500, null=True)),
                ('intro_text_2_fy_NL', models.CharField(help_text='Intro text 2', max_length=500, null=True)),
                ('intro_text_2_nl', models.CharField(help_text='Intro text 2', max_length=500, null=True)),
                ('intro_text_2_pl', models.CharField(help_text='Intro text 2', max_length=500, null=True)),
                ('intro_text_3', models.CharField(help_text='Intro text 3', max_length=500)),
                ('intro_text_3_en', models.CharField(help_text='Intro text 3', max_length=500, null=True)),
                ('intro_text_3_de', models.CharField(help_text='Intro text 3', max_length=500, null=True)),
                ('intro_text_3_pt', models.CharField(help_text='Intro text 3', max_length=500, null=True)),
                ('intro_text_3_es', models.CharField(help_text='Intro text 3', max_length=500, null=True)),
                ('intro_text_3_fr', models.CharField(help_text='Intro text 3', max_length=500, null=True)),
                ('intro_text_3_fy_NL', models.CharField(help_text='Intro text 3', max_length=500, null=True)),
                ('intro_text_3_nl', models.CharField(help_text='Intro text 3', max_length=500, null=True)),
                ('intro_text_3_pl', models.CharField(help_text='Intro text 3', max_length=500, null=True)),
                ('intro_text_4', models.CharField(help_text='Intro text 4', max_length=500)),
                ('intro_text_4_en', models.CharField(help_text='Intro text 4', max_length=500, null=True)),
                ('intro_text_4_de', models.CharField(help_text='Intro text 4', max_length=500, null=True)),
                ('intro_text_4_pt', models.CharField(help_text='Intro text 4', max_length=500, null=True)),
                ('intro_text_4_es', models.CharField(help_text='Intro text 4', max_length=500, null=True)),
                ('intro_text_4_fr', models.CharField(help_text='Intro text 4', max_length=500, null=True)),
                ('intro_text_4_fy_NL', models.CharField(help_text='Intro text 4', max_length=500, null=True)),
                ('intro_text_4_nl', models.CharField(help_text='Intro text 4', max_length=500, null=True)),
                ('intro_text_4_pl', models.CharField(help_text='Intro text 4', max_length=500, null=True)),
                ('letters', wagtail.core.fields.StreamField([('letters', wagtail.core.blocks.StructBlock([('author', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link'])), ('author_photo', wagtail.images.blocks.ImageChooserBlock(required=False)), ('letter', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'ol', 'ul'], help_text='Main letter content')), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('video_url', wagtail.core.blocks.URLBlock(help_text='Video url to link out to', required=False))]))])),
                ('letters_en', wagtail.core.fields.StreamField([('letters', wagtail.core.blocks.StructBlock([('author', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link'])), ('author_photo', wagtail.images.blocks.ImageChooserBlock(required=False)), ('letter', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'ol', 'ul'], help_text='Main letter content')), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('video_url', wagtail.core.blocks.URLBlock(help_text='Video url to link out to', required=False))]))], null=True)),
                ('letters_de', wagtail.core.fields.StreamField([('letters', wagtail.core.blocks.StructBlock([('author', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link'])), ('author_photo', wagtail.images.blocks.ImageChooserBlock(required=False)), ('letter', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'ol', 'ul'], help_text='Main letter content')), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('video_url', wagtail.core.blocks.URLBlock(help_text='Video url to link out to', required=False))]))], null=True)),
                ('letters_pt', wagtail.core.fields.StreamField([('letters', wagtail.core.blocks.StructBlock([('author', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link'])), ('author_photo', wagtail.images.blocks.ImageChooserBlock(required=False)), ('letter', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'ol', 'ul'], help_text='Main letter content')), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('video_url', wagtail.core.blocks.URLBlock(help_text='Video url to link out to', required=False))]))], null=True)),
                ('letters_es', wagtail.core.fields.StreamField([('letters', wagtail.core.blocks.StructBlock([('author', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link'])), ('author_photo', wagtail.images.blocks.ImageChooserBlock(required=False)), ('letter', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'ol', 'ul'], help_text='Main letter content')), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('video_url', wagtail.core.blocks.URLBlock(help_text='Video url to link out to', required=False))]))], null=True)),
                ('letters_fr', wagtail.core.fields.StreamField([('letters', wagtail.core.blocks.StructBlock([('author', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link'])), ('author_photo', wagtail.images.blocks.ImageChooserBlock(required=False)), ('letter', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'ol', 'ul'], help_text='Main letter content')), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('video_url', wagtail.core.blocks.URLBlock(help_text='Video url to link out to', required=False))]))], null=True)),
                ('letters_fy_NL', wagtail.core.fields.StreamField([('letters', wagtail.core.blocks.StructBlock([('author', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link'])), ('author_photo', wagtail.images.blocks.ImageChooserBlock(required=False)), ('letter', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'ol', 'ul'], help_text='Main letter content')), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('video_url', wagtail.core.blocks.URLBlock(help_text='Video url to link out to', required=False))]))], null=True)),
                ('letters_nl', wagtail.core.fields.StreamField([('letters', wagtail.core.blocks.StructBlock([('author', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link'])), ('author_photo', wagtail.images.blocks.ImageChooserBlock(required=False)), ('letter', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'ol', 'ul'], help_text='Main letter content')), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('video_url', wagtail.core.blocks.URLBlock(help_text='Video url to link out to', required=False))]))], null=True)),
                ('letters_pl', wagtail.core.fields.StreamField([('letters', wagtail.core.blocks.StructBlock([('author', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link'])), ('author_photo', wagtail.images.blocks.ImageChooserBlock(required=False)), ('letter', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'ol', 'ul'], help_text='Main letter content')), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('video_url', wagtail.core.blocks.URLBlock(help_text='Video url to link out to', required=False))]))], null=True)),
                ('search_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Search image')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtailmetadata.models.MetadataMixin, 'wagtailcore.page', models.Model),
        ),
    ]
