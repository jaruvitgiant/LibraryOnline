# OnlineLibrary Setup Guide

## 1. Clone the Repository

```bash
git clone https://github.com/jaruvitgiant/LibraryOnline.git
cd OnlineLibrary
```

## 2. Create and Activate Virtual Environment

```bash
python -m venv venv
# สำหรับ Windows
venv\Scripts\activate
# สำหรับ macOS/Linux
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. สร้างไฟล์ `.env` ในโฟลเดอร์เดียวกับ `manage.py` และเพิ่มข้อมูลดังนี้

```
SECRET_KEY=ใส่ของตัวเอง (ดูในไฟล์ settings.py)
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 5. รันคำสั่ง Migrate

```bash
python manage.py migrate
```

## 6. Start the Development Server

```bash
python manage.py runserver
```