from django.shortcuts import render

# Create your views here.
from LibraryAPP.forms import IssueBookForm
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from .forms import IssueBookForm
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def index(request):
    return render(request, "index.html")

@login_required(login_url = '/admin_login')
def add_book(request):
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']
        image = request.FILES.get('image')  # รับไฟล์รูปภาพ

        books = Book.objects.create(
            name=name,
            author=author,
            isbn=isbn,
            category=category,
            image=image  # เพิ่มรูปภาพ
        )
        books.save()
        alert = True
        return render(request, "add_book.html", {'alert':alert})
    
    return render(request, "add_book.html")
def edit_book(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == "POST":
        book.name = request.POST.get("name")
        book.author = request.POST.get("author")
        book.isbn = request.POST.get("isbn")
        book.category = request.POST.get("category")

        if "image" in request.FILES:
            book.image = request.FILES["image"]

        book.save()

        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "error": "Invalid request"})

@login_required(login_url = '/admin_login')
def view_books(request):
    books = Book.objects.all()
    return render(request, "view_books.html", {'books':books})

@login_required(login_url = '/admin_login')
def view_students(request):
    students = Student.objects.all()
    return render(request, "view_students.html", {'students':students})

@login_required(login_url = '/student_login')
def profile(request):
    return render(request, "profile.html")


@login_required(login_url='/admin_login')
def view_issued_history(request):
    # 1. ตรวจสอบสิทธิ์: อนุญาตเฉพาะผู้ดูแลระบบ (Superuser) เท่านั้น
    if not request.user.is_superuser:
        return HttpResponse("Permission Denied. Only Admin can view this page.")

    # 2. ดึงรายการ IssuedBook ทั้งหมดออกมา 
    # ใช้ select_related เพื่อดึงข้อมูล Student, Book และ User มาพร้อมกัน
    issued_records = IssuedBook.objects.all().select_related('student', 'book', 'student__user').order_by('-issue_date')
    
    # 3. จัดเตรียมข้อมูล
    details = []
    for record in issued_records:
        
        # จัดการกรณีที่ Student หรือ Book ถูกลบ
        student_name = record.student.user.get_full_name() or record.student.user.username if record.student else "Student ถูกลบ"
        student_info = f"{record.student.branch} ({record.student.roll_no})" if record.student else "N/A"
        book_title = record.book.name if record.book else "หนังสือถูกลบ"

        details.append({
            'student_name': student_name,
            'student_info': student_info,
            'book_title': book_title,
            'issue_date': record.issue_date,
            'expiry_date': record.expiry_date,
            # แสดง '-' ถ้า return_date เป็น None
            'return_date': record.return_date if record.return_date else "-", 
            'status': record.status,
        })
        
    return render(request, 'admin_issued_view.html', {'details': details})

@login_required(login_url = '/student_login')
def edit_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']

        student.user.email = email
        student.phone = phone
        student.branch = branch
        student.classroom = classroom
        student.roll_no = roll_no
        student.user.save()
        student.save()
        alert = True
        return render(request, "edit_profile.html", {'alert':alert})
    return render(request, "edit_profile.html")

def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect("/view_books")

def delete_student(request, myid):
    students = Student.objects.filter(id=myid)
    students.delete()
    return redirect("/view_students")

def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "change_password.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "change_password.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "change_password.html")

def student_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            passnotmatch = True
            return render(request, "student_registration.html", {'passnotmatch':passnotmatch})
        if User.objects.filter(username=username).exists():
            username_exists = True
            return render(request, "student_registration.html", {'username_exists': username_exists})
        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        student = Student.objects.create(user=user, phone=phone, branch=branch, classroom=classroom,roll_no=roll_no, image=image)
        user.save()
        student.save()
        
        alert = True
        return render(request, "student_registration.html", {'alert':alert})
    
    return render(request, "student_registration.html")

@login_required(login_url='/student_login')
def book_list(request):
    books = Book.objects.all()
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return render(request, "error_student_not_found.html")
    issued_items = IssuedBook.objects.filter(student=student).values('book_id', 'status')
    book_status_map = {}
    for item in issued_items:
        book_status_map[item['book_id']] = item['status'] 
    books_with_status = []
    for book in books:
        status = book_status_map.get(book.id, "can_request") 
        books_with_status.append({
            'book': book,
            'status': status
        })
    return render(request, "bookAll.html", {"books_with_status": books_with_status})

# ฟังก์ชัน request_book ยังคงเหมือนเดิม
@login_required(login_url='/student_login')
def request_book(request, book_id):
    student = get_object_or_404(Student, user=request.user)
    book = get_object_or_404(Book, id=book_id)
    if IssuedBook.objects.filter(student=student, book=book, status__in=["pending", "approved"]).exists():
        return redirect("book_list") 
    IssuedBook.objects.create(
        student=student,
        book=book,
        issue_date=date.today(), # ใช้ date.today() แทน datetime.today().date() เพื่อความชัดเจน
        status="pending"
    )
    return redirect("book_list")

# Admin 
@login_required(login_url='/admin/login/')
def manage_requests(request):
    requests = IssuedBook.objects.filter(status="pending")
    return render(request, "admin_manage_requests.html", {"requests": requests})

# Admin อนุมัติคำขอยืม
@login_required(login_url='/admin/login/')
def approve_request(request, request_id):
    issued = get_object_or_404(IssuedBook, id=request_id)
    issued.status = "approved"
    issued.save()
    return redirect("manage_requests")

# Admin ปฏิเสธคำขอยืม
@login_required(login_url='/admin/login/')
def reject_request(request, request_id):
    issued = get_object_or_404(IssuedBook, id=request_id)
    issued.status = "rejected"
    issued.save()
    return redirect("manage_requests")

@login_required(login_url='/student_login')
def student_issued_books(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        # หากผู้ใช้ไม่มี Student object (เช่น เป็น Admin) ให้ปฏิเสธการเข้าถึง
        return render(request, "error_student_not_found.html")
    
    # 2. ดึงรายการ IssuedBook ทั้งหมดของนักเรียนคนนี้ 
    # ใช้ select_related เพื่อดึงข้อมูล Book มาด้วย
    issued_records = IssuedBook.objects.filter(student=student).select_related('book').order_by('-issue_date')

    details = []
    for record in issued_records:
        book_title = record.book.name if record.book else "หนังสือถูกลบ"
        book_author = record.book.author if record.book else "N/A"

        details.append({
            'book_title': book_title,
            'book_author': book_author,
            'issue_date': record.issue_date,
            'expiry_date': record.expiry_date,
            'return_date': record.return_date if record.return_date else "-",
            'status': record.status,
        })
    return render(request, 'student_issued_books.html', {'details': details})


def student_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a student!!")
            else:
                return redirect("/profile")
        else:
            alert = True
            return render(request, "student_login.html", {'alert':alert})
    return render(request, "student_login.html")

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/add_book")
            else:
                return HttpResponse("You are not an admin.")
        else:
            alert = True
            return render(request, "admin_login.html", {'alert':alert})
    return render(request, "admin_login.html")

def Logout(request):
    logout(request)
    return redirect ("/")


