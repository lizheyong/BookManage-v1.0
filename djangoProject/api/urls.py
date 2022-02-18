from django.urls import path
from . import views

urlpatterns = [
    # 登陆 POST
    path('login', views.LoginView.as_view()),
    # 管理员获取用户列表 GET 管理员新增用户 POST
    path('users',views.UserInfoView.as_view()),
    # 注册 POST，获取用户信息，删改 GET PUT DELETE
    path('user', views.UserDetailInfoView.as_view()),
    # 用户修改密码
    path('user/password',views.ChangePasswordView.as_view()),
    # 书籍列表 GET
    path('books', views.BookInfoView.as_view()),
    # 新增书籍 POST,书籍详情 GET PUT DELETE
    path('book', views.BookDetailInfoView.as_view()),
    # 借书
    path('book/borrow', views.BorrowView.as_view()),
    # 还书
    path('book/return', views.ReturnView.as_view()),
    # 某书目所有借还记录
    path('book/records', views.BookRecordsView.as_view()),
    # 某书目借还状态
    path('book/status', views.BookStatusView.as_view()),
    # 某用户所有借书记录
    path('user/books', views.UserBooksView.as_view()),
    # 通过记录查询借还状态
    path('book/record', views.BookRecordView.as_view()),
]