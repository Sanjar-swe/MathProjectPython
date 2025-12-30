# Proyekt hújjetleri: Matematika Test Boti

## 1. Texnikalıq Tapsırma (TT) hám Arxitektura

### 1.1 Proyekt Túsindirmesi
**Maqset**: Oqıwshılardı matematika páninen test synawdan ótkeriw ushın Telegram bot jaratıw, sonday-aq sorawlardı basqarıw hám statistikanı kóriw ushın Admin Panel jaratıw.

### 1.2 Sistema Arxitekturası
- **Backend Freymvorki**: Python, Django 6.0
- **Bot Freymvorki**: Aiogram 3.23 (asinxron)
- **Maǵlıwmatlar Bazası**: PostgreSQL (Production) / SQLite (Dev)
- **API**: Django REST Framework (DRF)
- **Baylanıs**: 
    - Bot <-> MB: Django ORM (`sync_to_async` arqalı asinxron)
    - Admin Frontend <-> Backend: JSON API

### 1.3 Maǵlıwmatlar Bazası Modelleri
**2.1 `BotUser` (Oqıwshılar)**
- `telegram_id` (BigInteger, unikal): Paydalanıwshınıń Telegram ID si.
- `full_name` (Char): Paydalanıwshınıń tolıq atı-jóni.
- `username` (Char): Telegram username.

**2.2 `Question` (Sorawlar Bazası)**
- `text` (TextField): Soraw teksti.
- `image` (ImageField): Qosımsha súwret.
- `option_a`...`option_d` (Char): Juwap variantları.
- `correct_answer` (Char): Durıs juwap kilti ('a', 'b', 'c', 'd').
- `is_active` (Boolean): Sorawlardı jasırıw (soft-delete) ushın.

**2.3 `TestAttempt` (Nátiyjeler)**
- `user` (FK): Oqıwshı.
- `score` (Int): Durıs juwaplar sanı.
- `total_questions` (Int): Jámı sorawlar (10).

**2.4 `AttemptDetail` (Analitika)**
- Analitika ushın hár bir juwap (durıs/qáte/ótkerilgen) haqqında maǵlıwmat saqlaydı.

---

## 2. Islep Shıǵıw Logikası

### 2.1 Telegram Bot Logikası (Aiogram)
1.  **Start**: `/start` paydalanıwshınıń bar-joǵın tekseredi. Eger joq bolsa, tolıq atı-jónin soraydı hám dizimge aladı.
2.  **Test Process**:
    - Paydalanıwshı "🎯 Start Test" túymesin basadı.
    - Sistema 10 tosınnan (random) aktiv sorawdı aladı.
    - Sorawlar birme-bir kórsetiledi.
    - **Navigaciya**: Juwap beriw ushın A, B, C, D variantları.
3.  **Juwmaqlaw**:
    - 10 sorawdan keyin nátiyje esaplanadı.
    - Paydalanıwshıǵa nátiyje kórsetiledi: "7/10 durıs".
    - Qáte juwaplar durıs juwapları menen birge kórsetiledi.

### 2.2 Admin API (DRF)
- **Autentifikaciya**: JWT (Access + Refresh tokenleri).
- **Sorawlar CRUD**: Sorawlardı tolıq basqarıw.
- **Excel Import**: .xlsx fayllardan kóp sorawlardı júklew.
- **Dashboard**: Ulıwma paydalanıwshılar, ótiw kórsetkishleri hám eń jaqsı oqıwshılar statistikası.

---

## 3. Qáwipsizlik hám Anti-Cheat (Aldawǵa qarsı) Ilajları

### 3.1 Qáwipsizlik Funkciyaları
- **SQL Injection Qorǵaw**: Sorawlardı avtomat túrde tazalaytuǵın Django ORM qollanıladı.
- **Rate Limiting (DDoS Qorǵaw)**: 
    - Anonim API sorawları: kúnine 100.
    - Autentifikaciyadan ótken API sorawları: kúnine 1000.
- **Qáwipsizlik Headerleri**: Production (`DEBUG=False`) rejiminde qatań headerler qosıladı:
    - `SECURE_SSL_REDIRECT`: HTTPS ti májbúrleydi.
    - `SESSION_COOKIE_SECURE`: Cookie tek HTTPS arqalı jiberiledi.
    - `XSS_FILTER` & `CONTENT_TYPE_NOSNIFF`: Brauzer qorǵawları.
- **Orta ózgeriwshileri**: Qupıya maǵlıwmatlar (`SECRET_KEY`, `DB_PASSWORD`) `.env` faylında saqlanadı hám kodqa qosılmaydı.

### 3.2 Anti-Cheat hám Pútinlik
- **Tosınnan saylaw (Randomization)**: Hár bir test bazadan 10 *tosınnan* soraw aladı.
- **Waqıt sheklewleri**: (Keleshekte qosılıwı múmkin) Bot baslanıw waqtın qadaǵalaydı.
- **Bir TG ID - Bir akkaunt**: `telegram_id` tekseriwi arqalı qayta dizimnen ótiwdiń aldın aladı.

---

## 4. Paydalanıwshı Qollanbaları

### 4.1 Oqıwshı Qollanbası
1.  **Botı tabıw**: Telegram-da bot siltemesin ashıń.
2.  **Dizimnen ótiw**: `/start` túymesin basıń. Birinshi ret bolsa, tolıq atı-jónińizdi kiritin (mısalı, "Ivanov Ivan").
3.  **Testti baslaw**: "🎯 Start Test" túymesin basıń.
4.  **Test tapsırıw**: Sizge 10 soraw beriledi.
    - Sorawdı (hám bar bolsa súwretti) oqıń.
    - Durıs varianttı (A, B, C yamasa D) tańlań.
5.  **Nátiyjelerdi kóriw**: Sońǵı sorawdan keyin birden nátiyjeńiz hám qáteler dizimi kórsetiledi.

### 4.2 Muǵallim (Admin) Qollanbası
1.  **Panelge kiriw**: `https://example.uz/admin/` (yamasa sizdiń frontend URL) saytına ótiń.
2.  **Login**: Administrator maǵlıwmatları menen kiriń.
3.  **Sorawlardı basqarıw**:
    - **Excel Júklew**: Kóp sorawlardı júklew ushın "Import" funkciyasın qollanıń. Format: `Text | A | B | C | D | Correct Key`.
    - **Qolda qosıw**: "Add Question" túymesin basıp, maǵlıwmatlardı toldırıń hám súwret júkleń.
4.  **Monitoring**: Oqıwshılar reytingi hám qıyın sorawlardı kóriw ushın "Dashboard" bólimine ótiń.

---

## 5. Texnologiyalar Tańlaw Tiykarlaması

### Nelikte bul stek?

1.  **Python & Django**:
    - **Artıqmashlıqları**: Tez islep shıǵıw ("batteries included"), ornatılǵan qáwipsiz Admin Panel, kúshli ORM, úlken ekosistema.
    - **Sáykesligi**: Quramalı maǵlıwmatlar modellerin (Paydalanıwshılar, Testler, Sorawlar, Analitika) qáwipsiz basqarıw ushın oǵada qolaylı.

2.  **Aiogram (Async)**:
    - **Artıqmashlıqları**: Joqarı ónimdarlı asinxron bot freymvorki. Sinxron alternativlerge qaraǵanda mıńlaǵan bir waqıttaǵı paydalanıwshılardı qabıllay aladı.
    - **Integraciya**: Django ORM menen sync-to-async adapterleri arqalı jaqsı isleydi.

3.  **PostgreSQL**:
    - **Artıqmashlıqları**: Isenimli, qatań tiplastırılǵan, MySQL-ge qaraǵanda quramalı sorawlardı jaqsıraq orynlaydı. Django production ushın standart.

4.  **Docker**:
    - **Artıqmashlıqları**: "Bir ret jaz, hár jerde islet". Islep shıǵıw ortalıǵınıń production menen birdey bolıwın támiyinleydi hám VPS-te ornatıwdı ańsatlasıradı.

5.  **Nginx**:
    - **Artıqmashlıqları**: Joqarı ónimdarlı keri proksi. SSL (HTTPS) hám statikalıq fayllardı nátiyjeli basqarıp, Python-nıń júklemesin azaytadı.

---
*Hújjet jaratılǵan sáne: 2025-12-30*
