# Portfolio sayt — Django + admin panel + Telegram

Saytdagi **hamma matn, rasm va havola** admin panel orqali o'zgartiriladi.
Kod ochish shart emas.

---

## 1. Lokalda ishga tushirish (Ubuntu)

Loyiha papkasida terminal ochib, quyidagilarni **bittalab** bajaring:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py boshlangich
python manage.py createsuperuser
python manage.py runserver
```

Tayyor:

| Manzil | Nima |
|---|---|
| http://127.0.0.1:8000/ | Sayt |
| http://127.0.0.1:8000/boshqaruv-panel/ | Admin panel |

`createsuperuser` ishga tushganda username, email va parol so'raydi.
**Parol kamida 10 ta belgi bo'lsin** va boshqa hech qayerda ishlatilmagan bo'lsin.

Keyingi safar ishga tushirish uchun faqat:

```bash
source .venv/bin/activate && python manage.py runserver
```

---

## 2. Admin panelda nima qayerda

| Bo'lim | Nimani o'zgartiradi |
|---|---|
| **Sayt sozlamalari** | Logo matni, profil rasmi, favicon, CV fayli, footer |
| **Menyu (Nav)** | Navbardagi har bir so'z, tartibi, ko'k tugma qaysi biri |
| **Hero (bosh ekran)** | Katta sarlavha, tavsif, tugma matni va havolasi |
| **Men haqimda — sarlavha** | Bo'lim sarlavhasi |
| **Men haqimda — qatorlar** | Ism, manzil, o'qish va h.k. Xohlagancha qator qo'shasiz |
| **Loyihalar — sarlavha** | Bo'lim sarlavhasi va bo'sh holat matni |
| **Loyihalar** | Loyiha qo'shish: nom, tavsif, **rasm yuklash**, sayt havolasi, GitHub havolasi, texnologiyalar |
| **Aloqa** | Email, telefon, GitHub, Telegram, forma yozuvlari |
| **Kelgan xabarlar** | Formadан kelgan xabarlar (faqat o'qish) |

Loyiha qo'shganda **Rasm** maydonida "Choose file" bosib kompyuteringizdan
rasm tanlaysiz. **Sayt havolasi** ixtiyoriy — agar loyiha veb-sayt bo'lsa
to'ldirasiz, bo'lmasa bo'sh qoldirasiz.

---

## 3. Telegram botni ulash

### 3.1 Token va chat ID olish

1. Telegramda **@BotFather** ga kiring → `/mybots` → botingizni tanlang →
   **API Token** → nusxa oling.
2. **@userinfobot** ga `/start` yozing → chiqqan `Id` raqamini nusxa oling.

### 3.2 `.env` fayliga yozish

```
TELEGRAM_BOT_TOKEN=8123456789:AAH...
TELEGRAM_CHAT_ID=123456789
TELEGRAM_WEBHOOK_SECRET=uzun-tasodifiy-satr
```

Serverni qayta ishga tushiring. Endi saytdagi aloqa formasi to'ldirilganda
xabar botingizga keladi.

### 3.3 Bot buyruqlarga javob berishi uchun (ixtiyoriy)

Bu faqat sayt internetda joylashgandan keyin ishlaydi:

```bash
curl -F "url=https://SIZNING-SAYT.onrender.com/telegram/webhook/SECRET/" \
  https://api.telegram.org/botTOKEN/setWebhook
```

Shundan keyin bot `/start` va `/xabarlar` buyruqlarini tushunadi.

---

## 4. Rasmlar haqida — muhim

Render'ning bepul tarifida disk **vaqtinchalik**. Ya'ni siz admin orqali
yuklagan rasmlar keyingi deploy'da **o'chib ketadi**.

Yechimi — Cloudinary (bepul):

1. cloudinary.com da ro'yxatdan o'ting
2. Dashboard'dan `CLOUDINARY_URL` ni nusxa oling
3. Render'da environment variable sifatida qo'shing

`CLOUDINARY_URL` to'ldirilgan bo'lsa, loyiha avtomatik o'sha yerga saqlaydi.
Bo'sh bo'lsa — lokal diskka (lokal ishlash uchun yetarli).

---

## 5. Render'ga deploy

1. Loyihani GitHub'ga yuklang (`.env` YUKLANMAYDI — `.gitignore` da)
2. Render → New → Blueprint → repozitoriyni tanlang (`render.yaml` o'zi o'qiladi)
3. Environment bo'limida qo'lda qo'shing:
   `CLOUDINARY_URL`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`,
   `TELEGRAM_WEBHOOK_SECRET`, `ALLOWED_HOSTS`
4. Deploy tugagach, Render Shell'da:
   ```bash
   python manage.py boshlangich
   python manage.py createsuperuser
   ```

**Eslatma:** bepul tarifda sayt 15 daqiqa harakatsizlikdan keyin uxlaydi,
birinchi ochilish ~30 soniya kutadi. cron-job.org da har 10 daqiqada
saytga ping qo'ysangiz, uyg'oq turadi.

---

## 6. Xavfsizlik

- `.env` fayli hech qachon GitHub'ga tushmasin (`.gitignore` da bor)
- Admin manzili `/admin` emas — `.env` dagi `ADMIN_URL` orqali boshqariladi
- `DEBUG=False` production'da (`render.yaml` da shunday)
- Aloqa formasida honeypot va daqiqasiga 3 ta so'rov cheklovi bor

**Lokalda `DEBUG=False` qilmang** — HTTPS'ga majburiy yo'naltirish yoqiladi
va `127.0.0.1` ochilmay qoladi.

---

## 7. Loyiha tuzilishi

```
config/          Django sozlamalari va URL'lar
core/
  models.py      Barcha modellar (admin paneldagi bo'limlar shu yerdan)
  admin.py       Admin panel ko'rinishi
  views.py       Bosh sahifa, forma, Telegram webhook
  forms.py       Aloqa formasi (honeypot bilan)
  telegram.py    Telegram API bilan ishlash
  management/commands/boshlangich.py   Boshlang'ich menyu va matnlar
templates/       HTML shablonlar
static/css/      Dizayn
static/js/       Mobil menyu, scroll effektlari
```

Dizaynni o'zgartirmoqchi bo'lsangiz — `static/css/style.css` faylining eng
tepasidagi rang o'zgaruvchilarini almashtiring, butun sayt bo'ylab qo'llanadi.
