# Generated by Django 5.0.6 on 2024-06-10 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_caprateformula'),
    ]

    operations = [
        migrations.RenameField(
            model_name='caprateformula',
            old_name='insurance',
            new_name='mo_insurance',
        ),
        migrations.RenameField(
            model_name='caprateformula',
            old_name='mgmt_fee_rate',
            new_name='mo_mgmt_fee_rate',
        ),
        migrations.AddField(
            model_name='caprateformula',
            name='mo_hoa',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='caprateformula',
            name='mo_leasing_fee',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='caprateformula',
            name='mo_maintance_as_rate',
            field=models.DecimalField(decimal_places=4, default=0.08, max_digits=5),
        ),
        migrations.AddField(
            model_name='caprateformula',
            name='mo_utilities',
            field=models.IntegerField(default=0),
        ),
    ]
