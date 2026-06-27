# 🌸 SakuraStream

> **Where Every Petal Tells an Anime Story**

A production-ready anime discovery platform built with Django, featuring a stunning dark luxury UI with sakura aesthetics.

---

## 🚀 Quick Start (Docker)

```bash
# 1. Clone & enter directory
git clone <repo-url> sakurastream && cd sakurastream

# 2. Copy environment variables
cp .env.example .env  # edit as needed

# 3. Start everything
docker-compose up -d

# 4. Create superuser
docker-compose exec web python manage.py createsuperuser

# 5. Fetch initial anime data
docker-compose exec web python manage.py shell -c "from apps.anime.tasks import fetch_top_anime; fetch_top_anime()"

# 6. Visit http://localhost
```

---

## 🛠️ Local Dev (Without Docker)

```bash
# Requirements: Python 3.11+, PostgreSQL, Redis

pip install -r requirements.txt

# Edit .env for local DB
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# In separate terminal - Celery worker
celery -A sakurastream worker -l info

# In separate terminal - Celery beat
celery -A sakurastream beat -l info
```

---

## 📁 Project Structure

```
sakurastream/
├── sakurastream/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── celery.py
├── apps/
│   ├── anime/             # Anime models, views, tasks
│   ├── characters/        # Character models & views
│   ├── users/             # Custom user + auth
│   ├── watchlist/         # Watchlist system
│   ├── community/         # Reviews & comments
│   ├── recommendations/   # AI recommendation engine
│   └── notifications/     # Notification system
├── templates/             # Django HTML templates
├── static/                # CSS, JS, images
├── media/                 # User uploads
├── nginx/                 # Nginx config
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## ✨ Features

| Feature | Status |
|---|---|
| Anime Database | ✅ |
| Auto-fetch from Jikan API | ✅ (every 6h) |
| Auto-fetch from AniList API | ✅ |
| Advanced Search & Filters | ✅ |
| User Authentication | ✅ |
| Watchlist System | ✅ |
| Review & Rating System | ✅ |
| Character Database | ✅ |
| AI Recommendations | ✅ |
| Achievement System | ✅ |
| Admin Dashboard | ✅ |
| REST API | ✅ |
| PWA Ready | ✅ |
| Celery Task Queue | ✅ |
| Redis Cache | ✅ |
| Docker Deploy | ✅ |

---

## 🎨 Tech Stack

- **Backend**: Django 4.2, DRF, Celery, Redis
- **Database**: PostgreSQL
- **Frontend**: Tailwind CSS, Alpine.js, Three.js particles
- **Effects**: Falling sakura petals, mouse glow, glass cards, neon borders
- **Deploy**: Docker, Nginx, Gunicorn

---

## 🔑 Admin

Visit `/admin/` after creating a superuser. The admin dashboard lets you:
- Add/edit/delete anime with poster uploads
- Manage characters, voice actors
- Manage users, reviews, collections
- View analytics

---

## 📡 API Endpoints

```
GET /api/anime/              # List anime (paginated, filterable)
GET /api/anime/<slug>/       # Anime detail
GET /api/genres/             # All genres
GET /api/characters/         # Characters list
```

---

## 🌸 Color Palette

| Name | Hex |
|---|---|
| Sakura Pink | `#FF77C8` |
| Neon Purple | `#A855F7` |
| Lavender | `#C084FC` |
| Midnight | `#0B0B14` |
| Moon White | `#F8FAFC` |
