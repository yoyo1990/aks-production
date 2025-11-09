# 📝 הסבר על קובץ .htpasswd

## 🔍 מה יש בקובץ:
admin:$1$salt123$8KKKZ3JJbQY5B.J8sNhVa0

## 📋 פירוט:
- שם משתמש: arad
- סיסמה מוצפנת של: arad1980

## 🔑 לכניסה השתמש ב:
- Username: arad  
- Password: arad1980

## 💻 איך זה עובד:
1. הדפדפן שולח: arad:arad1980
2. Nginx מצפין את arad1980 
3. משווה לhash בקובץ
4. אם תואם = כניסה מותרת ✅