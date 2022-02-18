from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book, User, Borrow, Log
from .serializers import UserModelSerializer, UserListSerializer, ChangePasswordSerializer, \
    UserPutSerializer, BookListSerializer, BookPostSerializer, BookPutSerializer, BorrowPostSerializer, RegisterSerializer
from .utils.jwt_auth import creat_token
from datetime import datetime, timedelta
import api

"""用户列表"""
class UserInfoView(APIView):

    authentication_classes = [api.extensions.auth.AdminAuthentication]

    def get(self,request):

        users = User.objects.all()
        serializer = UserListSerializer(instance=users,many=True)
        return Response({'code':1001,'msg':'获取用户列表成功','data':serializer.data},status=status.HTTP_200_OK)

    # 管理员添加用户
    def post(self,request):

        data_dict = request.data
        serializer = UserModelSerializer(data=data_dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

"""用户详情视，注册"""
class UserDetailInfoView(APIView):

    authentication_classes = [api.extensions.auth.NoPostAdminAuthentication]

    def get(self, request):

        user_id = request.query_params.get('user_id')
        your_id = request.user.get("id")
        admin = User.objects.get(id=your_id).is_admin
        if user_id != str(your_id) and admin == False:
            return Response({'code': 1000, 'msg': '您无权查看其他用户信息!'}, status=status.HTTP_204_NO_CONTENT)
        user = User.objects.filter(id=user_id)
        if not user:
            return Response({'code': 1001, 'msg': '用户不存在'}, status=status.HTTP_204_NO_CONTENT)
        user_object = user.first()
        data = {'username':user_object.user_name,
                'nickename':user_object.user_nickname,
                'email':user_object.user_email
               }
        return Response({'code':1001,'msg':'获取用户信息成功','data':data},status=status.HTTP_200_OK)

    def post(self,request):
        data_dict = request.data
        serializer = RegisterSerializer(data=data_dict)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        same_user_email = User.objects.filter(user_email=email)
        if same_user_email:
            return Response({'code':1000, 'msg':'该邮箱已被注册'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            user_id = User.objects.filter(user_email=email).first().id
            Log.objects.create(user_id=user_id, action='注册')
        return Response({'code':1001,'msg':'注册成功','data':{'user_id':user_id}}, status=status.HTTP_201_CREATED)

    def put(self, request):

        user_id = request.data.get('user_id')
        nickname = request.data.get('nickname')
        email = request.data.get('email')
        # 根据id筛选用户列表
        user = User.objects.filter(id=user_id)
        if not user:
            return Response({'code': 1001, 'msg': '用户不存在或id不正确'}, status=status.HTTP_204_NO_CONTENT)
        # 从token的payload中获取当前登陆id
        your_id = request.user.get('id')
        # 这里设定是只能改自己的信息，包括管理员也是
        if user_id != str(your_id):
            return Response({'code': 1001, 'msg': '您不能更改其他用户的信息'}, status=status.HTTP_204_NO_CONTENT)
        # 判断邮箱是否改变，改变后的是否已被注册
        user_object = user.first()
        if email != user_object.user_email:
            same_email = User.objects.filter(user_email=email)
            if same_email:
                return Response({'code': 1001, 'msg': '该邮箱已被注册'}, status=status.HTTP_204_NO_CONTENT)
        # 用序列化器存入更改的信息
        data_dict = {
            'user_nickname':nickname,
            'user_email':email
        }
        serializer = UserPutSerializer(instance=user_object, data=data_dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'code':1000, 'msg':'修改用户信息成功'}, status=status.HTTP_201_CREATED)

    def delete(self, request):

        user_id = request.query_params.get('user_id')
        your_id = request.user.get("id")
        admin = User.objects.get(id=your_id).is_admin
        if user_id != str(your_id) and admin == False:
            return Response({'code':1000, 'msg':'您无权删除其他用户!'}, status=status.HTTP_204_NO_CONTENT)
        User.objects.get(id=user_id).delete()
        return Response({'code':1000, 'msg':'删除用户成功'}, status=status.HTTP_204_NO_CONTENT)

"""书籍列表"""
class BookInfoView(APIView):

    def get(self,request):

        books = Book.objects.all()
        serializer = BookListSerializer(instance=books,many=True)
        return Response({'code':1001,'msg':'获取书籍列表成功','data':serializer.data},status=status.HTTP_200_OK)

"""书籍详情"""
class BookDetailInfoView(APIView):

    authentication_classes = [api.extensions.auth.NoGetAdminAuthentication]

    def post(self,request):

        data_dict = request.data
        serializer = BookPostSerializer(data=data_dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        book_id = serializer.data.get('book_id')
        return Response({'code':1001,'msg':'添加书籍成功','data':{'book_id':book_id}},status=status.HTTP_201_CREATED)

    def get(self,request):
        book_id = request.query_params.get('book_id')
        book = Book.objects.filter(id=book_id)
        if not book:
            return Response({'code': 1000, 'msg': '书目不存在'}, status=status.HTTP_204_NO_CONTENT)
        serializer = BookPutSerializer(instance=book)
        return Response({'code': 1001, 'msg': '获得书籍信息成功', 'data':serializer.data}, status=status.HTTP_200_OK)

    def put(self,request):

        book_id = request.data.get('book_id')
        book = Book.objects.filter(id=book_id)
        if not book:
            return Response({'code': 1000, 'msg': '书目不存在'}, status=status.HTTP_204_NO_CONTENT)
        data_dict = request.data
        del data_dict['book_id']
        book_object = book.first()
        serializer = BookPutSerializer(instance=book_object,data=data_dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'code': 1001, 'msg': '更改书籍信息成功', 'data':serializer.data}, status=status.HTTP_201_CREATED)

    def delete(self,request):

        book_id = request.query_params.get('book_id')
        book = Book.objects.filter(id=book_id)
        if not book:
            return Response({'code': 1000, 'msg': '书目不存在'}, status=status.HTTP_204_NO_CONTENT)
        book_object = book.first()
        serializer = BookPutSerializer(instance=book_object)
        Book.objects.get(id=book_id).delete()
        return Response({'code': 1001, 'msg': '删除书籍信息成功', 'data': serializer.data}, status=status.HTTP_204_NO_CONTENT)

"""登陆"""
class LoginView(APIView):

    authentication_classes = []

    def post(self, request):

        user_name = request.data.get('username')
        user_password = request.data.get('password')
        user_object = User.objects.filter(user_name=user_name, user_password=user_password).first()
        if not user_object:
            return Response({'code': 1000, 'msg': '用户名或密码名错误'}, status=status.HTTP_400_BAD_REQUEST)
        Log.objects.create(user_id=user_object.id, action='登录')
        token = creat_token({'id': user_object.id, 'name': user_object.user_name,'is_admin':user_object.is_admin})
        return Response({'code': 1001, 'msg': '登陆成功', 'token':token,'data':{'user_id':user_object.id}}, status=status.HTTP_200_OK)

"""改密码"""
class ChangePasswordView(APIView):

    def post(self,request):

        user_id = request.data.get('user_id')
        old_password = request.data.get('old_password')
        password = request.data.get('password')

        user = User.objects.filter(id=user_id)
        if not user:
            return Response({'code': 1001, 'msg': '用户不存在'}, status=status.HTTP_204_NO_CONTENT)
        user_object = user.first()
        if old_password != user_object.user_password:
            return Response({'code': 1001, 'msg': '原始密码错误'}, status=status.HTTP_204_NO_CONTENT)

        serializer = ChangePasswordSerializer(instance=user_object, data={'user_password':password})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        Log.objects.create(user_id=user_object.id, action='修改密码')
        return Response({'code': 1000, 'msg': '密码修改成功'}, status=status.HTTP_200_OK)

"""借书"""
class BorrowView(APIView):

    def post(self, request):

        user_id = request.data.get('user_id')
        user = User.objects.filter(id=user_id)
        if not user:
            return Response({'code': 1001, 'msg': '用户不存在'}, status=status.HTTP_204_NO_CONTENT)

        book_id = request.data.get('book_id')
        book = Book.objects.filter(id=book_id)
        if not book:
            return Response({'code': 1001, 'msg': '书籍不存在'}, status=status.HTTP_204_NO_CONTENT)

        book = book.first()
        if (book.is_available == False):
            return Response({'code': 1001, 'msg': '书籍已被借出'}, status=status.HTTP_204_NO_CONTENT)

        borrow_time = datetime.now()
        return_ddl = borrow_time + timedelta(days=90)
        Borrow.objects.create(user_id=user_id, book_id=book_id, borrow_time=borrow_time, return_ddl=return_ddl)
        book.is_available = False
        book.save()
        Log.objects.create(user_id=user_id, book_id=book_id, action='借书', record_id=book.borrow_set.all().first().id)
        borrow_object = Borrow.objects.get(user_id=user_id, book_id=book_id)
        serializer = BorrowPostSerializer(instance=borrow_object)

        return Response({'code': 1000, 'msg': '借书成功','data':serializer.data}, status=status.HTTP_200_OK)

"""还书"""
class ReturnView(APIView):

    def post(self, request):

        borrow_id = request.data.get('record_id')
        user_id = request.data.get('user_id')
        user = User.objects.filter(id=user_id)
        if not user:
            return Response({'code': 1001, 'msg': '用户不存在'}, status=status.HTTP_204_NO_CONTENT)
        borrow_entries = Borrow.objects.filter(id=borrow_id,user_id=user_id)
        if borrow_entries:
            borrow_entry = borrow_entries.first()
            borrow_entry.borrow_time = borrow_entry.borrow_time.replace(tzinfo=None)
            delta = -(borrow_entry.borrow_time - datetime.now())  # 负天数不足一天算一天
            exceed_days = delta.days - 90
            if exceed_days > 0:
                fine = exceed_days * 0.5
                return Response({'code': 1001, 'msg': '已逾期 {} 天，需缴纳罚金 {} 元！'.format(exceed_days, fine)},
                                status=status.HTTP_200_OK)
            book_id = borrow_entry.book_id
            book = Book.objects.get(id=book_id)
            book.is_available = True
            book.save()
            Log.objects.create(user_id=user_id, book_id=book_id, action='还书',record_id=book.borrow_set.all().first().id)
            borrow_entry.delete()
            data = {
                'borrow_date':borrow_entry.borrow_time,
                'return_date':datetime.now()
            }
            return Response({'code': 1000, 'msg': '还书成功', 'data':data}, status=status.HTTP_200_OK)
        else:
            return Response({'code': 1001, 'msg': '借书记录不存在'}, status=status.HTTP_204_NO_CONTENT)

"""指定书目所有借还记录"""
class BookRecordsView(APIView):

    authentication_classes = [api.extensions.auth.AdminAuthentication]

    def get(self,request):

        book_id = request.query_params.get('book_id')
        book_obj = Book.objects.filter(id=book_id)
        if not book_obj:
            return Response({'code': 1000, 'msg': '该书目不存在!'}, status=status.HTTP_204_NO_CONTENT)
        records = Log.objects.filter(book_id=book_id, action='借书')
        data_list = []
        for record in records:
            if not Log.objects.filter(record_id=record.record_id, action='还书').first():
                data = {
                    'record_id': record.record_id,
                    'user_id': record.user_id,
                    'username': User.objects.get(id=record.user_id).user_name,
                    'borrow_date': record.time,
                    'return_date': 'null'
                }
            else:
                data = {
                    'record_id': record.record_id,
                    'user_id': record.user_id,
                    'username': User.objects.get(id=record.user_id).user_name,
                    'borrow_date': record.time,
                    'return_date': Log.objects.filter(record_id=record.record_id, action='还书').first().time
                }
            data_list.append(data)

        return Response({'code':1000, 'msg':'获取该书目所有借还记录成功!', 'data':data_list}, status=status.HTTP_200_OK)

"""指定书目借还状态"""
class BookStatusView(APIView):

    def get(self,request):

        book_id = request.query_params.get('book_id')
        book_obj = Book.objects.filter(id=book_id)
        if not book_obj:
            return Response({'code': 1000, 'msg': '该书目不存在!'}, status=status.HTTP_204_NO_CONTENT)
        available = Book.objects.get(id=book_id).is_available
        if available == False:
            borrow_object = Borrow.objects.get(book_id=book_id)
            data = {
                'user_id':borrow_object.user_id,
                'borrow_date':borrow_object.borrow_time,
                'return_date':borrow_object.return_ddl
            }
            return Response({'code': 1000, 'msg': '该书目已被借出!', 'data': data}, status=status.HTTP_200_OK)

        return Response({'code':1001, 'msg':'该书可借！!'}, status=status.HTTP_200_OK)

"""指定用户的所有借书记录"""
class UserBooksView(APIView):

    def get(self,request):
        user_id = request.query_params.get('user_id')
        your_id = request.user.get("id")
        admin = User.objects.get(id=your_id).is_admin
        if user_id != str(your_id) and admin == False:
            return Response({'code':1000, 'msg':'您无权查看其他用户借书记录!'}, status=status.HTTP_204_NO_CONTENT)
        if not User.objects.filter(id=user_id):
            return Response({'code':1000, 'msg':'该用户不存在!'}, status=status.HTTP_204_NO_CONTENT)
        records = Log.objects.filter(user_id=user_id, action='借书')
        data_list = []
        for record in records:
            if not Log.objects.filter(record_id=record.record_id, action='还书').first():
                data = {
                    'record_id': record.record_id,
                    'book_id': record.book_id,
                    'name': Book.objects.get(id=record.book_id).book_name,
                    'borrow_date': record.time,
                    'return_date': 'null'
                }
            else:
                data = {
                    'record_id': record.record_id,
                    'book_id': record.book_id,
                    'name': Book.objects.get(id=record.book_id).book_name,
                    'borrow_date': record.time,
                    'return_date': Log.objects.filter(record_id=record.record_id, action='还书').first().time
                }
            data_list.append(data)

        return Response({'code':1001, 'msg':'获取该用户所有借还记录成功!', 'data':data_list}, status=status.HTTP_200_OK)
        pass

"""通过记录查询书目借还状态"""
class BookRecordView(APIView):

    authentication_classes = [api.extensions.auth.AdminAuthentication]

    def get(self,request):
        record_id = request.query_params.get('record_id')
        log = Log.objects.filter(record_id=record_id)
        if not log:
            return Response({'code':1000, 'msg':'记录不存在!'}, status=status.HTTP_204_NO_CONTENT)
        if log.last().action == '还书':
            return Response({'code': 1001, 'msg': '该书可以借!'}, status=status.HTTP_200_OK)
        record = log.first()
        data = {
            'book_id': record.book_id,
            'user_id': record.user_id,
            'borrow_date': record.time,
            'return_date': Borrow.objects.get(id=record.record_id).return_ddl
        }
        return Response({'code':1000, 'msg':'该书已被借出!', 'data':data}, status=status.HTTP_200_OK)