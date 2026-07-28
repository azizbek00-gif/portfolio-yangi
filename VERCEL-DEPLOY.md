# Vercel'ga deploy — bosqichma-bosqich

Vercel serverli emas (serverless). Shuning uchun:
- Baza tashqarida bo'ladi (Neon Postgres — bepul)
- Rasmlar Cloudinary'da (Vercel'da disk yo'q)
- Sayt HECH QACHON uxlamaydi — Telegram bot ham doim tayyor

---

## 1. Neon baza yaratish (bepul Postgres)

1. https://neon.tech ga kiring (GitHub bilan)
2. "Create project" → nom bering → region: Europe (Frankfurt)
3. Dashboard'da "Connection string" ni nusxa oling.
   **MUHIM:** "Pooled connection" (yoki "Connection pooling") variantini tanlang —
   Vercel serverless uchun aynan shu kerak. Host nomida `-pooler` bo'ladi:
   `postgresql://user:parol@ep-xxx-pooler.eu-central-1.aws.neon.tech/dbname?sslmode=require`
4. Bu satrni saqlab qo'ying — Vercel'ga `DATABASE_URL` sifatida beramiz.

   Eslatma: migratsiya (5-qadam) uchun lokalda ODDIY (pooler'siz) satrni
   ishlatgan ma'qul, Vercel'da esa pooled satrni. Ikkalasi ham Neon
   dashboard'da ko'rsatilgan.

## 2. Cloudinary (rasmlar uchun)

1. https://cloudinary.com → bepul ro'yxatdan o'ting
2. Dashboard'dan `CLOUDINARY_URL` ni nusxa oling
   (`cloudinary://api_key:api_secret@cloud_name`)

## 3. GitHub'ga yuklash

Loyihani yangi (yoki mavjud) repozitoriyga yuklang:

```bash
cd ~/portfolio
git init
git add .
git commit -m "Portfolio: admin panel + Telegram + Vercel"
git branch -M main
git remote add origin https://github.com/azizbek00-gif/YANGI-REPO.git
git push -u origin main
```

`.env` YUKLANMAYDI (`.gitignore` da bor) — bu to'g'ri.

## 4. Vercel'ga ulash

1. https://vercel.com → "Add New" → "Project" → GitHub repongizni tanlang
2. Framework Preset: **Other** (Vercel Django'ni o'zi tanimaydi, `vercel.json` bor)
3. "Environment Variables" bo'limida quyidagilarni qo'shing:

   | Nomi | Qiymati |
   |---|---|
   | `SECRET_KEY` | uzun tasodifiy satr (50+ belgi) |
   | `DEBUG` | `False` |
   | `DATABASE_URL` | Neon connection string |
   | `CLOUDINARY_URL` | Cloudinary'dan |
   | `ADMIN_URL` | `boshqaruv-panel/` |
   | `TELEGRAM_BOT_TOKEN` | yangi tokeningiz |
   | `TELEGRAM_CHAT_ID` | 8631335073 |
   | `TELEGRAM_WEBHOOK_SECRET` | tasodifiy maxfiy satr |

4. "Deploy" bosing.

## 5. Baza migratsiyasi va superuser

Vercel'da terminal yo'q. Migratsiyani lokaldan Neon bazasiga bajarasiz:

```bash
cd ~/portfolio
source .venv/bin/activate
# .env dagi DATABASE_URL ni vaqtincha Neon satriga o'zgartiring, keyin:
python manage.py migrate
python manage.py boshlangich
python manage.py createsuperuser
# tugagach .env dagi DATABASE_URL ni yana bo'sh qilib qo'ying (lokal SQLite uchun)
```

Endi https://SIZNING-SAYT.vercel.app/boshqaruv-panel/ orqali admin'ga kirasiz.

## 6. Telegram webhook (bot doim ishlashi uchun)

Sayt tayyor bo'lgach, brauzerda bu manzilni oching (TOKEN va SECRET ni almashtiring):

```
https://api.telegram.org/botTOKEN/setWebhook?url=https://SIZNING-SAYT.vercel.app/telegram/webhook/SECRET/
```

`{"ok":true,"result":true,...}` chiqsa — bot ulandi.
Endi saytdagi forma to'ldirilsa, xabar botga keladi. Bot `/start` va
`/xabarlar` buyruqlarini ham tushunadi.

---

## Muhim eslatmalar

- **SQLite Vercel'da ishlamaydi** — shuning uchun Neon majburiy.
- **Har deploy'dan keyin migratsiya kerak bo'lsa** — lokaldan Neon'ga
  `python manage.py migrate` qilasiz (yuqoridagi 5-qadamdek).
- **Rasm yuklash faqat Cloudinary bilan ishlaydi** Vercel'da.
- Domenni keyin Vercel Settings → Domains dan o'zgartirishingiz mumkin.
