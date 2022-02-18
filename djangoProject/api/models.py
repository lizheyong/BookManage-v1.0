from django.db import models
from datetime import datetime

"""用户模型类"""
class User(models.Model):

    user_name = models.CharField(max_length=10, verbose_name='用户名')
    user_password = models.CharField(max_length=15, verbose_name='密码')
    user_email = models.EmailField(verbose_name='邮箱')
    user_nickname = models.CharField(max_length=10,  verbose_name='昵称')
    borrowed_books = models.ManyToManyField('Book', verbose_name='借阅书籍', through='Borrow')
    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

"""书籍模型类"""
class Book(models.Model):

    book_name = models.CharField(max_length=20, verbose_name='书名')
    book_place =  models.CharField(max_length=20, verbose_name='位置')
    book_author = models.CharField(max_length=20, verbose_name='作者')
    book_introduce = models.CharField(max_length=200, verbose_name='简介')
    book_price = models.FloatField(verbose_name='价格')
    is_available = models.BooleanField(default=True, verbose_name='是否可借')

    class Meta:
        db_table = 'tb_books'  # 指明数据库表名
        verbose_name = '图书'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

"""借书记录模型类"""
class Borrow(models.Model):

    user = models.ForeignKey(User, verbose_name='借阅者', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name='所借书籍', on_delete=models.CASCADE)
    borrow_time = models.DateTimeField(verbose_name='借出时间', default=datetime.now())
    return_ddl = models.DateTimeField(verbose_name='归还期限', default=datetime.now())

    class Meta:
        db_table = 'tb_borrows'
        verbose_name = '借阅关系'
        verbose_name_plural = verbose_name

"""日志模型类"""
class Log(models.Model):

    time = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name='相关书籍', on_delete=models.CASCADE, null=True)
    action = models.CharField(verbose_name='操作', max_length=30)
    record_id = models.IntegerField(verbose_name='记录id',null=True)

    class Meta:
        db_table = 'tb_logs'
        verbose_name = '日志'
        verbose_name_plural = verbose_name