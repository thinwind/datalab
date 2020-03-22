# Generated by Django 3.0.4 on 2020-03-22 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssemblyLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='新生产线', max_length=200)),
                ('imput_params', models.TextField(blank=True)),
                ('output_params', models.TextField(blank=True)),
                ('description', models.TextField(blank=True, default='新生产线')),
                ('status', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'assembly_line',
            },
        ),
        migrations.CreateModel(
            name='CompoundMachine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='新复合生产机', max_length=200)),
                ('input_params', models.TextField(blank=True)),
                ('output_params', models.TextField(blank=True)),
                ('description', models.TextField(blank=True, default='新复合生产机')),
                ('status', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='compound_machies', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'compound_machine',
            },
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='新生产机', max_length=200)),
                ('input_params', models.TextField(blank=True)),
                ('engine', models.CharField(max_length=100)),
                ('output_params', models.TextField(blank=True)),
                ('description', models.TextField(blank=True, default='新生产机')),
                ('status', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='machies', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'al_machine',
            },
        ),
        migrations.CreateModel(
            name='MachineGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postion', models.IntegerField()),
                ('compound_machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assemblyline.CompoundMachine')),
                ('sub_machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assemblyline.Machine')),
            ],
            options={
                'db_table': 'machine_group',
            },
        ),
        migrations.AddField(
            model_name='compoundmachine',
            name='sub_machines',
            field=models.ManyToManyField(related_name='compound_machies', through='assemblyline.MachineGroup', to='assemblyline.Machine'),
        ),
        migrations.CreateModel(
            name='AssemblyLineMachine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postion', models.IntegerField()),
                ('assembly_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assemblyline.AssemblyLine')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assemblyline.Machine')),
            ],
            options={
                'db_table': 'al_assembly_line_machine',
            },
        ),
        migrations.CreateModel(
            name='AssemblyLineCompoundMachine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postion', models.IntegerField()),
                ('assembly_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assemblyline.AssemblyLine')),
                ('compound_machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assemblyline.CompoundMachine')),
            ],
            options={
                'db_table': 'al_assembly_line_compound_machine',
            },
        ),
        migrations.AddField(
            model_name='assemblyline',
            name='compound_machines',
            field=models.ManyToManyField(related_name='assembly_lines', through='assemblyline.AssemblyLineCompoundMachine', to='assemblyline.CompoundMachine'),
        ),
        migrations.AddField(
            model_name='assemblyline',
            name='machines',
            field=models.ManyToManyField(related_name='assembly_lines', through='assemblyline.AssemblyLineMachine', to='assemblyline.Machine'),
        ),
        migrations.AddField(
            model_name='assemblyline',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='assembly_lines', to=settings.AUTH_USER_MODEL),
        ),
    ]