from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("add_book/", views.add_book, name="add_book"),
    path("edit_book/<int:id>/", views.edit_book, name="edit_book"),
    path('student_issued_books/', views.student_issued_books, name='student_issued_books'),
     path('admin/issued_history/', views.view_issued_history, name='view_issued_history'),

    path("view_books/", views.view_books, name="view_books"),
    path("view_students/", views.view_students, name="view_students"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),

    path("student_registration/", views.student_registration, name="student_registration"),
    path("change_password/", views.change_password, name="change_password"),
    path("student_login/", views.student_login, name="student_login"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("logout/", views.Logout, name="logout"),

    path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),
    path("delete_student/<int:myid>/", views.delete_student, name="delete_student"),

    #ส่งคำขอยืมหนังสือ
    path("books/", views.book_list, name="book_list"),
    path("books/request/<int:book_id>/", views.request_book, name="request_book"),

    path("admin/requests/", views.manage_requests, name="manage_requests"),
    path("admin/requests/approve/<int:request_id>/", views.approve_request, name="approve_request"),
    path("admin/requests/reject/<int:request_id>/", views.reject_request, name="reject_request"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
