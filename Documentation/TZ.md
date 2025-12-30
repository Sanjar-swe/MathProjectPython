# TZ - Matematika Test Bot

## 1. Proekt Arxitekturası

- **Backend:** Python, Django.
- **Bot:** Aiogram yaki basqa framework (Django proekti ishinde integraciya qılınadı).
- **Database:** PostgreSQL.
- **Baylanıs:**
    - **Bot -> Database:** Django ORM (Async).
    - **Admin Frontend -> Backend:** Django REST Framework (DRF) API.

---

## 2. Database Tiykarǵı Modelleri (Django ORM)

*Barlıq maǵlıwmatlar PostgreSQL bazasında saqlanadı.*

### 2.1. `BotUser` (Oqıwshılar)

- `telegram_id` (BigInteger, unique, index) - Telegram ID.
- `full_name` (Char) - Oqıwshınıń F.I.O.
- `username` (Char, null) - Telegram username.
- `created_at` (DateTime) - Dizimnen ótken waqtı.

### 2.2. `Question` (Sorawlar bazası)

- `text` (TextField) - Soraw teksti.
- `image` (ImageField, null/blank) - Soraw súwreti (eger bolsa).
- `option_a` (Char) - A variantı.
- `option_b` (Char) - B variantı.
- `option_c` (Char) - C variantı.
- `option_d` (Char) - D variantı.
- `correct_answer` (Char) - Durıs juwap gilti ('a', 'b', 'c', 'd').
- `is_active` (Boolean, default=True) - Sorawdı waqtınsha óshiriw ushın.

### 2.3. `TestAttempt` (Test nátiyjeleri)

- `user` (ForeignKey -> BotUser) - Test tapsırǵan oqıwshı.
- `score` (Integer) - Durıs juwaplar sanı.
- `total_questions` (Integer, default=10) - Jıynalǵan ball (max 10).
- `created_at` (DateTime) - Test tapsırılǵan waqıt.

### 2.4. `AttemptDetail` (Analiz ushın)

- `attempt` (ForeignKey -> TestAttempt) - Qaysı testke tiyisli ekeni.
- `question` (ForeignKey -> Question) - Qaysı soraw.
- `user_answer` (Char) - Oqıwshı belgilegen variant.
- `is_correct` (Boolean) - Durıs pa, joq pa.

---

## 3. Telegram Bot (Aiogram + Django ORM)

*Bot Django menen bir serverde isleydi. Maǵlıwmatlardı alıw ushın `sync_to_async` yamasa Django-nıń async metodlarınan paydalanıw kerek.*

### 3.1. Start & Registraciya

1. **Komanda:** `/start`.
2. **Tekseriw:** `BotUser` modelinen `telegram_id` boyınsha izleydi.
3. **Logika:**
    - Eger paydalanıwshı joq bolsa: *"Assalawma aleykum! Testti baslaw ushın atı-familiyańızdı kiritin"* dep soraydı.
    - Kelgen xabardı `full_name` qılıp bazasǵa saqlaydı (`BotUser.objects.create(...)`).
    - Keyin Bas menyu shıǵadı.
    - Eger paydalanıwshı bar bolsa, tuwrıdan-tuwrı Bas menyu shıǵadı.

### 3.2. Test Processi

1. **Túyme:** "🎯 Test baslaw".
2. **Soraw tańlaw:** Bazadan `Question` modelinen `is_active=True` bolǵan 10 sorawdı random aladı.
3. **State (FSM):** Paydalanıwshı test rejimine ótedi. Sorawlar gezekpe-gezek beriledi.
    - Súwret bolsa súwret penen, bolmasa tek tekst.
    - Juwaplar Inline Button (A, B, C, D) túrinde shıǵadı.
4. **Process:** Hár juwaptan keyin bot onı yadında saqlaydı.
5. **Juwmaqlaw:** 10-soraw pitkennen soń:
    - Nátiyje esaplanadı.
    - `TestAttempt` hám `AttemptDetail` modellerine nátiyjeler jazıladı.

### 3.3. Nátiyje hám Qatelerdi kórsetiw

1. Oqıwshıǵa ball kórsetiledi: *"Siz 10 sorawdan 7 win durıs taptıńız"*.
2. Qáte qılǵan sorawları dizim etip shıǵarıladı:
    - Format: *Soraw teksti... (Siz: A ❌, Durıs: B ✅)*.
    - Eger sorawda súwret bolsa, qáteler diziminde súwret qayta jiberilmeydi (tek tekst hám variantlar).

### 3.4. Statistika (Bot ishinde)

1. **Túyme:** "📊 Meniń nátiyjelerim".
2. Sońǵı 10 test nátiyjesi tekst túrinde jiberiledi.

---

## 4. Admin Panel API (DRF)

*Bólek Frontend (React/Vue) ushın API-lar. Adminler usı API arqalı sorawlardı basqaradı.*

### 4.1. Autentifikaciya

- **Login:** JWT Token (Access + Refresh).

### 4.2. Sorawlardı basqarıw (Questions CRUD)

- `GET /api/admin/questions/` - Barlıq sorawlar dizimi (Pagination, Search, Filter).
- `POST /api/admin/questions/` - Jańa soraw qosıw (Súwret júklew imkaniyatı menen).
- `PUT /api/admin/questions/{id}/` - Sorawdı ózgertiw.
- `DELETE /api/admin/questions/{id}/` - Sorawdı óshiriw.

### 4.3. Excel Import

- `POST /api/admin/import-questions/` - Excel fayl (.xlsx) qabıl etedi.
- **Logika:** Backend exceldi oqıp, sorawlardı parslap, bazasǵa jazıwı kerek.

### 4.4. Paydalanıwshılar hám Statistika

- `GET /api/admin/users/` - Bot paydalanıwshıları dizimi.
- `GET /api/admin/dashboard/` - Statistika ushın maǵlıwmatlar:
    - Ulıwma oqıwshılar sanı.
    - Ulıwma test tapsırılǵan sanı.
    - Top 10 oqıwshı (Reyting).
    - Eń qıyın sorawlar (eń kóp qate qılınǵan sorawlar statistikası).
- `GET /api/attempts/` - Nátiykeler dizimi.

---

## 5. Programmistke Eslestpeler (Development Notes)

1. **Aiogram & Django:**
    - Bot `management/commands/runbot.py` sıyaqlı arnawlı komanda arqalı iske túsiwi kerek.
    - `os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")` - bot iske túskende Django settingleri júkleniwi shárt.
    - Database query-lerdi async funkciyalar ishinde isletkende `sync_to_async` wrapperinen paydalanıw yamasa Django 4.2+ async ORM interfeysin qollanıw kerek.
2. **Media Files:**
    - Admin panelden júklengen súwretler `media/` papkasına túsedi.
3. **Deploy:**
    - Gunicorn (Backend API ushın).
    - Systemd service yamasa Docker container.
    - Nginx (Reverse proxy hám media fayllardı kórsetiw ushın).
