git clone https://github.com/jaruvitgiant/LibraryOnline.git

cd OnlineLibrary

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

สร้างไฟล์ .env ขึ้นมาในรับดับกับ manage.py เเล้วใส่

SECRET_KEY=ใส่ของตัวเอง >>> อยู่ในไฟล์ seting
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1


python manage.py migrate

python manage.py runserver