# Generated by Django 3.2.8 on 2022-02-12 07:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=20, verbose_name='书名')),
                ('book_place', models.CharField(max_length=20, verbose_name='位置')),
                ('book_author', models.CharField(max_length=20, verbose_name='作者')),
                ('book_introduce', models.CharField(max_length=200, verbose_name='简介')),
                ('book_price', models.FloatField(verbose_name='价格')),
                ('is_available', models.BooleanField(default=True, verbose_name='是否可借')),
            ],
            options={
                'verbose_name': '图书',
                'verbose_name_plural': '图书',
                'db_table': 'tb_books',
            },
        ),
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_time', models.DateTimeField(default=datetime.datetime(2022, 2, 12, 7, 38, 21, 939553), verbose_name='借出时间')),
                ('return_ddl', models.DateTimeField(default=datetime.datetime(2022, 2, 12, 7, 38, 21, 939574), verbose_name='归还期限')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.book', verbose_name='所借书籍')),
            ],
            options={
                'verbose_name': '借阅关系',
                'verbose_name_plural': '借阅关系',
                'db_table': 'tb_borrows',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=10, verbose_name='用户名')),
                ('user_password', models.CharField(max_length=15, verbose_name='密码')),
                ('user_email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('user_nickname', models.CharField(max_length=10, verbose_name='昵称')),
                ('is_admin', models.BooleanField(default=False)),
                ('borrowed_books', models.ManyToManyField(through='api.Borrow', to='api.Book', verbose_name='借阅书籍')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'tb_users',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('action', models.CharField(max_length=30, verbose_name='操作')),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.book', verbose_name='相关书籍')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user', verbose_name='用户')),
            ],
            options={
                'verbose_name': '日志',
                'verbose_name_plural': '日志',
                'db_table': 'tb_logs',
            },
        ),
        migrations.AddField(
            model_name='borrow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user', verbose_name='借阅者'),
        ),
    ]
