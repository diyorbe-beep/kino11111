# Admin Login Paroli

## 🔍 Mavjud Admin Parolini Tekshirish

Agar superuser allaqachon yaratilgan bo'lsa, uni tekshirish:

### 1-usul: Django Shell

```bash
cd JustHD
python manage.py shell
```

Shell ichida:
```python
from apps.users.models import User

# Barcha superuserlarni ko'rish
superusers = User.objects.filter(is_superuser=True)
for user in superusers:
    print(f"Username: {user.username}, Email: {user.email}, is_staff: {user.is_staff}")

# Yoki faqat staff userlarni
staff_users = User.objects.filter(is_staff=True)
for user in staff_users:
    print(f"Username: {user.username}, Email: {user.email}")
```

### 2-usul: Django Admin Panel

1. `/admin/` ga o'ting
2. Login qilishga harakat qiling
3. Agar login qila olsangiz, parol to'g'ri

---

## 🆕 Superuser Yaratish

Agar superuser yo'q bo'lsa, yarating:

### 1-usul: Django Management Command (Eng Oson)

```bash
cd JustHD
python manage.py createsuperuser
```

**So'raladigan ma'lumotlar:**
- Username: `admin` (yoki boshqa)
- Email: `admin@example.com` (optional)
- Password: `admin123` (yoki boshqa kuchli parol)
- Password (again): parolni qayta kiriting

### 2-usul: Django Shell

```bash
cd JustHD
python manage.py shell
```

Shell ichida:
```python
from apps.users.models import User

# Superuser yaratish
admin = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123'  # O'zgartiring!
)

# Staff qilish (admin panel uchun)
admin.is_staff = True
admin.save()

print(f"✅ Superuser yaratildi!")
print(f"Username: {admin.username}")
print(f"Password: admin123")  # O'zgartiring!
```

### 3-usul: Mavjud Userni Admin Qilish

```bash
cd JustHD
python manage.py shell
```

```python
from apps.users.models import User

# Mavjud userni topish
user = User.objects.get(username='your_username')  # O'zgartiring

# Admin qilish
user.is_superuser = True
user.is_staff = True
user.set_password('new_password')  # Parolni o'zgartirish
user.save()

print(f"✅ User admin qilindi: {user.username}")
```

---

## 🔐 Default Admin Credentials

**Eslatma:** Loyihada default admin credentials yo'q. Har doim o'zingiz yaratishingiz kerak.

Agar test uchun tezkor admin yaratmoqchi bo'lsangiz:

```bash
cd JustHD
python manage.py shell
```

```python
from apps.users.models import User

# Tezkor admin yaratish
admin = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123'
)
admin.is_staff = True
admin.save()

print("✅ Admin yaratildi!")
print("Username: admin")
print("Password: admin123")
print("URL: http://localhost:5173/admin/login")
```

---

## 📝 Admin Login Qadamlar

1. **Superuser yarating** (yuqoridagi usullardan biri)

2. **Admin login sahifasiga o'ting:**
   - URL: `http://localhost:5173/admin/login`
   - Yoki to'g'ridan-to'g'ri `/admin/login` ga o'ting

3. **Credentials kiriting:**
   - Username: `admin` (yoki yaratgan usernameniz)
   - Password: `admin123` (yoki yaratgan parolingiz)

4. **"Login as Admin" tugmasini bosing**

5. **Agar `is_staff=True` bo'lsa, admin panelga o'tasiz**

---

## ⚠️ Xavfsizlik Eslatmasi

Production'da:
- Kuchli parol ishlating (kamida 12 belgi, harflar, raqamlar, belgilar)
- Default parollarni o'zgartiring
- `admin` username o'rniga boshqa username ishlating

---

## 🆘 Muammo Bo'lsa

### Parolni unutdingizmi?

Parolni qayta tiklash:

```python
from apps.users.models import User

user = User.objects.get(username='admin')
user.set_password('yangi_parol')
user.save()
print("✅ Parol o'zgartirildi!")
```

### User topilmayaptimi?

```python
from apps.users.models import User

# Barcha userlarni ko'rish
users = User.objects.all()
for user in users:
    print(f"Username: {user.username}, is_staff: {user.is_staff}, is_superuser: {user.is_superuser}")
```

---

**Eslatma:** Agar hali superuser yaratmagan bo'lsangiz, yuqoridagi usullardan birini ishlatib yarating!


