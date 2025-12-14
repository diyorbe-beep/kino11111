# Admin Panelga Kirish Yo'llari

## 🎯 Frontend Admin Panel (React)

### URL
- **Development:** `http://localhost:5173/admin`
- **Production:** `http://your-domain.com/admin`

### Kirish Qadamlar:

1. **Login qiling:**
   - `/login` sahifasiga o'ting
   - Username va password kiriting

2. **Admin huquqlari kerak:**
   - Foydalanuvchi `is_staff=True` bo'lishi kerak
   - Agar `is_staff=False` bo'lsa, admin panelga kirish mumkin emas

3. **Navbar'da "Admin Panel" linki:**
   - Login qilgandan keyin, agar `is_staff=True` bo'lsa, navbar'da "Admin Panel" linki ko'rinadi
   - Yoki to'g'ridan-to'g'ri `/admin` URL ga o'ting

### Funksiyalar:
- ✅ Kino qo'shish (Create)
- ✅ Kino ko'rish (Read)
- ✅ Kino tahrirlash (Update)
- ✅ Kino o'chirish (Delete)
- ✅ CSV import
- ✅ Genres bilan ishlash

---

## 🔧 Django Admin Panel

### URL
- **Development:** `http://localhost:8000/admin/`
- **Production:** `http://your-domain.com/admin/`

### Kirish Qadamlar:

1. **Superuser yoki Staff user bo'lishi kerak**

2. **Login qiling:**
   - Username va password kiriting

### Funksiyalar:
- ✅ Barcha modellarni boshqarish
- ✅ Users, Movies, Genres, Categories, Comments, Ratings
- ✅ Advanced filtering va search
- ✅ Bulk actions

---

## 👤 Superuser Yaratish

### 1-usul: Django Management Command

```bash
# Docker orqali
docker-compose exec backend python manage.py createsuperuser

# Yoki to'g'ridan-to'g'ri
cd JustHD
python manage.py createsuperuser
```

**So'raladigan ma'lumotlar:**
- Username
- Email (optional)
- Password (2 marta)

### 2-usul: Django Shell

```bash
# Django shell ga kirish
python manage.py shell

# Shell ichida:
from apps.users.models import User
user = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='your-secure-password'
)
print(f"Superuser yaratildi: {user.username}")
```

### 3-usul: Environment Variables (Management Command)

Agar `.env` faylida quyidagi o'zgaruvchilar bo'lsa:

```bash
SUPERUSER_USERNAME=admin
SUPERUSER_EMAIL=admin@example.com
SUPERUSER_PASSWORD=secure-password-123
```

Keyin management command ishlatish:

```bash
python manage.py create_superuser
```

**Eslatma:** Bu command mavjud emas, lekin yaratish mumkin.

---

## 🔐 Staff User Yaratish (Admin emas, lekin admin panelga kirish mumkin)

### Django Shell orqali:

```bash
python manage.py shell
```

```python
from apps.users.models import User

# Yangi user yaratish
user = User.objects.create_user(
    username='staff_user',
    email='staff@example.com',
    password='password123'
)

# Staff qilish
user.is_staff = True
user.save()

print(f"Staff user yaratildi: {user.username}")
```

### Yoki mavjud userni staff qilish:

```python
from apps.users.models import User

user = User.objects.get(username='existing_user')
user.is_staff = True
user.save()
```

---

## ✅ Tekshirish

### Frontend Admin Panel uchun:

1. Login qiling
2. Browser console'da tekshiring:
   ```javascript
   // Console'da
   localStorage.getItem('access_token')
   ```
3. API request yuborib tekshiring:
   ```javascript
   fetch('http://localhost:8000/api/v1/auth/profile/', {
     headers: {
       'Authorization': 'Bearer ' + localStorage.getItem('access_token')
     }
   })
   .then(r => r.json())
   .then(data => console.log('is_staff:', data.data?.is_staff))
   ```

### Django Admin Panel uchun:

1. `/admin/` ga o'ting
2. Login qiling
3. Agar superuser bo'lsa, barcha modellar ko'rinadi

---

## 🚨 Muammolar va Yechimlar

### Muammo: "Admin Panel" linki ko'rinmayapti

**Yechim:**
1. Foydalanuvchi `is_staff=True` bo'lishi kerak
2. Login qiling va `/admin` ga to'g'ridan-to'g'ri o'ting
3. Agar hali ham ishlamasa, user ma'lumotlarini tekshiring:
   ```python
   from apps.users.models import User
   user = User.objects.get(username='your_username')
   print(f"is_staff: {user.is_staff}")
   print(f"is_superuser: {user.is_superuser}")
   ```

### Muammo: Frontend Admin Panel "/" ga redirect qiladi

**Yechim:**
- `AdminPanel.jsx` da `isAdmin()` tekshiruvi mavjud
- Agar `is_staff=False` bo'lsa, avtomatik "/" ga redirect qiladi
- User'ni staff qiling

### Muammo: Django Admin Panel login qilmayapti

**Yechim:**
1. Superuser yoki staff user bo'lishi kerak
2. Password to'g'ri ekanligini tekshiring
3. User active bo'lishi kerak (`is_active=True`)

---

## 📝 Qo'shimcha Ma'lumot

### Frontend Admin Panel Protection:

```javascript
// AdminPanel.jsx
useEffect(() => {
  if (!user || !isAdmin()) {
    navigate('/');
    return;
  }
  loadData();
}, [user, isAdmin, navigate]);
```

### Backend Admin API Protection:

```python
# admin_views.py
permission_classes = [IsAdminUser]

# IsAdminUser permission
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
```

---

## 🎯 Tezkor Kirish

1. **Superuser yaratish:**
   ```bash
   python manage.py createsuperuser
   ```

2. **Frontend'da login qiling:**
   - `/login` ga o'ting
   - Superuser credentials bilan login qiling

3. **Admin Panel'ga o'ting:**
   - Navbar'da "Admin Panel" linkini bosing
   - Yoki `/admin` ga to'g'ridan-to'g'ri o'ting

---

**Eslatma:** Production'da `is_staff=True` bo'lgan foydalanuvchilarni ehtiyotkorlik bilan boshqaring!

