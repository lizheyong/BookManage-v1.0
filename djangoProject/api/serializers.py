from rest_framework import serializers
from api.models import Book, User, Borrow

"""用户序列化器"""
class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

"""登陆序列化器"""
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","password","email","nickname"]

    username = serializers.CharField( source='user_name')
    password = serializers.CharField(max_length=15, source='user_password')
    email = serializers.EmailField(source='user_email')
    nickname = serializers.CharField(max_length=10, source='user_nickname')

"""用户列表序列化器"""
class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id","username"]

    username = serializers.CharField(read_only=True, source='user_name')

"""用户更改信息序列化器"""
class UserPutSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("user_nickname","user_email")

"""改密码序列化器"""
class ChangePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("user_password",)

"""书籍列表序列化器"""
class BookListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ["book_id","name"]

    book_id = serializers.IntegerField(read_only=True, source='id')
    name = serializers.CharField(read_only=True, source='book_name')

"""新增书籍序列化器"""
class BookPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ["name","place","author","introduction","price","book_id"]

    name = serializers.CharField(max_length=20, source='book_name')
    place =  serializers.CharField(max_length=20,  source='book_place')
    author = serializers.CharField(max_length=20,  source='book_author')
    introduction = serializers.CharField(max_length=200,  source='book_introduce')
    price = serializers.FloatField( source='book_price')
    book_id = serializers.IntegerField(read_only=True, source='id')

"""更改书籍信息序列化器"""
class BookPutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ["name","place","author","introduction","price"]

    name = serializers.CharField(max_length=20, source='book_name')
    place =  serializers.CharField(max_length=20,  source='book_place')
    author = serializers.CharField(max_length=20,  source='book_author')
    introduction = serializers.CharField(max_length=200,  source='book_introduce')
    price = serializers.FloatField( source='book_price')

"""借书post序列化器"""
class BorrowPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrow
        fields = ["record_id","borrow_date"]

    record_id = serializers.IntegerField(read_only=True, source='id')
    borrow_date = serializers.DateTimeField(source='borrow_time')