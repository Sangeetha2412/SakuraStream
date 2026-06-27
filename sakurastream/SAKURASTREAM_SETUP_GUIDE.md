# 🌸 SakuraStream — Complete Setup Guide

> **"Where Every Petal Tells an Anime Story"**
> Step-by-step instructions to get SakuraStream running on your machine.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Extract the Project](#extract-the-project)
3. [Choose Your Setup Method](#choose-your-setup-method)
4. [Method A — Docker (Recommended)](#method-a--docker-recommended)
5. [Method B — Local Development (No Docker)](#method-b--local-development-no-docker)
6. [Configure Environment Variables](#configure-environment-variables)
7. [First Run — Database & Admin](#first-run--database--admin)
8. [Fetch Anime Data](#fetch-anime-data)
9. [Verify Everything Works](#verify-everything-works)
10. [Project Structure Explained](#project-structure-explained)
11. [Admin Dashboard Guide](#admin-dashboard-guide)
12. [API Reference](#api-reference)
13. [Common Errors & Fixes](#common-errors--fixes)
14. [Production Deployment Notes](#production-deployment-notes)

---

## ✅ Prerequisites

Before you begin, install the following on your machine:

### For Docker Setup (Easiest)
| Tool | Version | Download |
|---|---|---|
| Docker Desktop | Latest | https://www.docker.com/products/docker-desktop |
| Docker Compose | Included with Docker Desktop | — |
| Git (optional) | Any | https://git-scm.com |

> **Windows users:** Install Docker Desktop and enable WSL2 integration when prompted.

### For Local Dev Setup
| Tool | Version | Download |
|---|---|---|
| Python | 3.11 or higher | https://www.python.org/downloads |
| PostgreSQL | 14 or higher | https://www.postgresql.org/download |
| Redis | 7.x | https://redis.io/download (Linux/Mac) or use Redis Cloud |
| pip | Included with Python | — |

> **Windows Redis:** Use https://github.com/tporadowski/redis/releases or run Redis via WSL2.

---

## 📦 Extract the Project

```bash
# Unzip the downloaded file
unzip SakuraStream.zip

# Enter the project directory
cd sakurastream

# Confirm the structure looks right
ls -la
```

You should see:
```
sakurastream/
├── apps/
├── sakurastream/
├── templates/
├── static/
├── nginx/
├── .env
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🤔 Choose Your Setup Method

| | Docker (Method A) | Local Dev (Method B) |
|---|---|---|
| **Difficulty** | ⭐ Easy | ⭐⭐ Medium |
| **Requires** | Docker only | Python + PostgreSQL + Redis |
| **Best for** | Running the app | Active development |
| **Speed** | 1 command | Several steps |

---

## Method A — Docker (Recommended)

This is the fastest way. Docker handles the database, Redis, Celery, and Nginx automatically.

### Step 1 — Verify Docker is running

```bash
docker --version
# Should print: Docker version 24.x.x

docker-compose --version
# Should print: Docker Compose version 2.x.x
```

If Docker is not running, open Docker Desktop and wait for it to say "Running".

### Step 2 — Configure your .env file

The `.env` file is already pre-filled with working defaults. You can leave it as-is for local testing.

```bash
# Open the .env file in any text editor
# On Mac/Linux:
nano .env
# On Windows:
notepad .env
```

The default `.env` contents (no changes needed for local testing):
```env
SECRET_KEY=sakura-change-this-in-production-supersecretkey-xyz123abc
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

DB_NAME=sakurastream
DB_USER=sakura
DB_PASSWORD=sakura123
DB_HOST=db
DB_PORT=5432

REDIS_URL=redis://redis:6379/0

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
SITE_URL=http://localhost
```

### Step 3 — Build and start all services

```bash
docker-compose up -d --build
```

This will:
- Build the Django app image
- Start PostgreSQL database
- Start Redis cache
- Start Celery worker (background tasks)
- Start Celery Beat (scheduled tasks)
- Start Nginx (web server)

> First build takes 3–5 minutes. Subsequent starts take ~10 seconds.

Watch the logs to confirm everything started:
```bash
docker-compose logs -f web
# Press Ctrl+C to stop watching logs
```

You should see:
```
web_1   | [INFO] Starting gunicorn 21.2.0
web_1   | [INFO] Listening at: http://0.0.0.0:8000
```

### Step 4 — Run database migrations

```bash
docker-compose exec web python manage.py migrate
```

Expected output:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying users.0001_initial... OK
  Applying anime.0001_initial... OK
  ...
```

### Step 5 — Create an admin account

```bash
docker-compose exec web python manage.py createsuperuser
```

You'll be prompted:
```
Username: admin
Email address: admin@sakurastream.com
Password: (type a strong password)
Password (again): (repeat)
Superuser created successfully.
```

### Step 6 — Fetch anime data

```bash
docker-compose exec web python manage.py shell -c "
from apps.anime.tasks import fetch_top_anime
fetch_top_anime()
print('Done! Anime data is being fetched.')
"
```

> This fetches the top 100 anime from Jikan API (MyAnimeList). Takes ~30 seconds.

### Step 7 — Visit the site

Open your browser and go to:

| URL | What it is |
|---|---|
| http://localhost | Main website |
| http://localhost/admin/ | Admin dashboard |
| http://localhost/api/ | REST API |

---

## Method B — Local Development (No Docker)

Use this if you want to develop and edit code actively.

### Step 1 — Install Python 3.11+

```bash
python --version
# Must show Python 3.11.x or higher

# If not installed, download from https://www.python.org/downloads
```

### Step 2 — Create a virtual environment

```bash
# Inside the sakurastream folder
python -m venv venv

# Activate it:
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Your terminal prompt should now show (venv)
```

### Step 3 — Install all Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> This installs ~35 packages including Django, Celery, scikit-learn, etc. Takes 1–3 minutes.

### Step 4 — Set up PostgreSQL

Open pgAdmin or the psql terminal:

```sql
-- Open psql:
psql -U postgres

-- Run these commands:
CREATE DATABASE sakurastream;
CREATE USER sakura WITH PASSWORD 'sakura123';
GRANT ALL PRIVILEGES ON DATABASE sakurastream TO sakura;
ALTER USER sakura CREATEDB;
\q
```

### Step 5 — Set up Redis

**Mac (Homebrew):**
```bash
brew install redis
brew services start redis
```

**Ubuntu/Debian:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

**Windows:** Download from https://github.com/tporadowski/redis/releases and run `redis-server.exe`

Verify Redis works:
```bash
redis-cli ping
# Should return: PONG
```

### Step 6 — Configure environment variables

Edit the `.env` file and change `DB_HOST` from `db` to `localhost`:

```env
SECRET_KEY=sakura-change-this-in-production-supersecretkey-xyz123abc
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=sakurastream
DB_USER=sakura
DB_PASSWORD=sakura123
DB_HOST=localhost          ← Change this from 'db' to 'localhost'
DB_PORT=5432

REDIS_URL=redis://localhost:6379/0    ← Change 'redis' to 'localhost'

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
SITE_URL=http://localhost:8000
```

### Step 7 — Run migrations

```bash
python manage.py migrate
```

### Step 8 — Create superuser

```bash
python manage.py createsuperuser
```

### Step 9 — Collect static files

```bash
python manage.py collectstatic --noinput
```

### Step 10 — Start the development server

Open **3 separate terminal windows** (all with venv activated):

**Terminal 1 — Django web server:**
```bash
python manage.py runserver
```

**Terminal 2 — Celery worker (background jobs):**
```bash
celery -A sakurastream worker -l info
```

**Terminal 3 — Celery Beat (scheduled tasks every 6h):**
```bash
celery -A sakurastream beat -l info
```

### Step 11 — Fetch initial anime data

In a **4th terminal** (or while server is running):
```bash
python manage.py shell -c "
from apps.anime.tasks import fetch_top_anime
fetch_top_anime()
print('Fetching anime...')
"
```

### Step 12 — Visit the site

Open: **http://localhost:8000**

---

## ⚙️ Configure Environment Variables

Here is every variable in `.env` explained:

```env
# ─────────────────────────────────────────────
# DJANGO CORE
# ─────────────────────────────────────────────

# A long random string for security. CHANGE THIS IN PRODUCTION.
SECRET_KEY=sakura-change-this-in-production-supersecretkey-xyz123abc

# Set to False in production!
DEBUG=True

# Comma-separated list of domains your site is served from
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# ─────────────────────────────────────────────
# DATABASE (PostgreSQL)
# ─────────────────────────────────────────────

DB_NAME=sakurastream         # Database name
DB_USER=sakura               # Database username
DB_PASSWORD=sakura123        # Database password
DB_HOST=db                   # 'db' for Docker, 'localhost' for local dev
DB_PORT=5432                 # Default PostgreSQL port

# ─────────────────────────────────────────────
# REDIS (Cache + Celery broker)
# ─────────────────────────────────────────────

# 'redis' for Docker, 'localhost' for local dev
REDIS_URL=redis://redis:6379/0

# ─────────────────────────────────────────────
# EMAIL
# ─────────────────────────────────────────────

# console = prints emails to terminal (good for dev)
# smtp = real email sending (for production)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Uncomment and fill these for real email sending:
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
# DEFAULT_FROM_EMAIL=noreply@sakurastream.com

# ─────────────────────────────────────────────
# SITE
# ─────────────────────────────────────────────

SITE_URL=http://localhost    # Your site's base URL
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 🗃️ First Run — Database & Admin

### Running migrations

Migrations create all database tables. Run this once:

```bash
# Docker:
docker-compose exec web python manage.py migrate

# Local:
python manage.py migrate
```

If you add new models later, run:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating a superuser (admin account)

```bash
# Docker:
docker-compose exec web python manage.py createsuperuser

# Local:
python manage.py createsuperuser
```

Fill in username, email, and password when prompted.

### Accessing the Admin Dashboard

Go to: **http://localhost/admin/** (Docker) or **http://localhost:8000/admin/** (local)

Log in with the superuser credentials you just created.

---

## 🎌 Fetch Anime Data

SakuraStream fetches data from **Jikan API** (free MyAnimeList API — no key needed).

### Option 1 — Fetch top anime manually (recommended first run)

```bash
# Docker:
docker-compose exec web python manage.py shell -c "
from apps.anime.tasks import fetch_top_anime
fetch_top_anime()
"

# Local:
python manage.py shell -c "
from apps.anime.tasks import fetch_top_anime
fetch_top_anime()
"
```

### Option 2 — Fetch seasonal anime

```bash
docker-compose exec web python manage.py shell -c "
from apps.anime.tasks import fetch_seasonal_anime
fetch_seasonal_anime()
"
```

### Option 3 — Fetch trending anime

```bash
docker-compose exec web python manage.py shell -c "
from apps.anime.tasks import fetch_trending_anime
fetch_trending_anime()
"
```

### Option 4 — Fetch upcoming anime

```bash
docker-compose exec web python manage.py shell -c "
from apps.anime.tasks import fetch_upcoming_anime
fetch_upcoming_anime()
"
```

### Automatic fetching (Celery Beat)

Once Celery Beat is running, it **automatically** fetches new data every 6 hours. No manual action needed after the first seed.

---

## ✅ Verify Everything Works

Go through this checklist:

```
□ http://localhost        → Homepage loads with sakura petal animation
□ http://localhost/anime/ → Anime grid shows (after fetching data)
□ http://localhost/admin/ → Admin panel loads, you can log in
□ http://localhost/api/anime/ → JSON response with anime list
□ http://localhost/users/register/ → Registration form loads
□ http://localhost/trending/ → Trending page loads
□ http://localhost/seasonal/ → Seasonal page loads
```

### Check Docker container status

```bash
docker-compose ps
```

All services should show "Up":
```
NAME                    STATUS
sakurastream_web_1      Up
sakurastream_db_1       Up (healthy)
sakurastream_redis_1    Up
sakurastream_celery_1   Up
sakurastream_nginx_1    Up
```

### Check logs

```bash
# All services
docker-compose logs

# Just the web app
docker-compose logs web

# Celery tasks
docker-compose logs celery

# Follow live (like tail -f)
docker-compose logs -f web
```

---

## 📁 Project Structure Explained

```
sakurastream/
│
├── sakurastream/              ← Django project configuration
│   ├── __init__.py            ← Loads Celery on startup
│   ├── settings.py            ← All settings (DB, email, cache, etc.)
│   ├── urls.py                ← Root URL routing
│   ├── celery.py              ← Celery task queue config
│   └── wsgi.py                ← WSGI server entry point
│
├── apps/                      ← All Django apps live here
│   │
│   ├── anime/                 ← Core anime app
│   │   ├── models.py          ← Anime, Genre, Studio, Collection models
│   │   ├── views.py           ← Home, list, detail, search views
│   │   ├── urls.py            ← URL patterns for anime pages
│   │   ├── api_urls.py        ← REST API URL patterns
│   │   ├── serializers.py     ← DRF serializers for the API
│   │   ├── tasks.py           ← Celery tasks: fetch from Jikan API
│   │   ├── admin.py           ← Custom admin panel configuration
│   │   └── sitemaps.py        ← SEO sitemap generation
│   │
│   ├── characters/            ← Anime characters
│   │   ├── models.py          ← Character, VoiceActor, AnimeCharacter
│   │   ├── views.py           ← Character list & detail pages
│   │   └── urls.py
│   │
│   ├── users/                 ← Custom user system
│   │   ├── models.py          ← User (with XP/levels), Achievement
│   │   ├── views.py           ← Register, login, logout, profile
│   │   ├── forms.py           ← Login, register, profile edit forms
│   │   └── urls.py
│   │
│   ├── watchlist/             ← User watchlist tracker
│   │   ├── models.py          ← WatchlistEntry (status, progress, score)
│   │   ├── views.py           ← Watchlist page, toggle, update progress
│   │   └── urls.py
│   │
│   ├── community/             ← Reviews & discussions
│   │   ├── models.py          ← Review, Comment, Discussion
│   │   ├── views.py           ← Submit review, like review
│   │   └── urls.py
│   │
│   ├── recommendations/       ← Recommendation engine
│   │   ├── engine.py          ← Genre-based + collaborative filtering
│   │   └── views.py           ← Personalized recommendations API
│   │
│   └── notifications/         ← User notifications
│       ├── models.py          ← Notification model
│       └── views.py           ← List & mark-read endpoints
│
├── templates/                 ← HTML templates
│   ├── base.html              ← Master layout (nav, footer, petals, JS)
│   ├── partials/
│   │   ├── anime_card.html    ← Reusable anime card component
│   │   └── section_header.html← Reusable section title
│   ├── anime/
│   │   ├── home.html          ← Homepage with all sections
│   │   ├── list.html          ← Browse + filter page
│   │   ├── detail.html        ← Full anime detail page
│   │   ├── trending.html
│   │   ├── seasonal.html
│   │   ├── upcoming.html
│   │   ├── genre.html
│   │   └── collection.html
│   ├── characters/
│   │   ├── list.html
│   │   └── detail.html
│   ├── users/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   └── edit_profile.html
│   ├── watchlist/
│   │   └── list.html
│   └── community/
│       └── home.html
│
├── static/                    ← Static assets served by Nginx/Whitenoise
│   ├── images/                ← Fallback images
│   ├── css/                   ← Custom CSS (base is in base.html)
│   ├── js/                    ← Custom JS
│   └── manifest.json          ← PWA manifest
│
├── media/                     ← User-uploaded files (posters, avatars)
├── nginx/
│   └── nginx.conf             ← Nginx reverse proxy config
│
├── .env                       ← Environment variables (never commit this!)
├── Dockerfile                 ← Docker image definition
├── docker-compose.yml         ← Multi-container orchestration
├── manage.py                  ← Django management CLI
└── requirements.txt           ← Python dependencies
```

---

## 🔐 Admin Dashboard Guide

Go to **http://localhost/admin/**

### What you can manage:

**Anime section:**
- Add anime manually with title, synopsis, poster URL, genres
- Upload poster and banner images
- Mark anime as Featured, Trending, or Editor's Pick
- Set MAL ID to link with Jikan API data

**Genres & Studios:**
- Add/edit genres with custom colors and icons
- Manage animation studios

**Collections:**
- Create curated anime collections
- Mark collections as Featured (shows on homepage)

**Users:**
- View all registered users
- See XP, level, join date
- Manage staff/admin permissions

**Reviews & Community:**
- Moderate user reviews
- Delete inappropriate content

**Achievements:**
- Create achievement badges
- Set rarity (common/rare/legendary) and XP rewards

### Making anime appear on the homepage

1. Go to **Admin → Anime → Anime**
2. Click on any anime
3. Check **Is featured** → saves to Featured spotlight
4. Check **Is trending** → appears in Trending section
5. Check **Is editor pick** → appears in Editor's Picks

---

## 📡 API Reference

The REST API is available at `/api/`

### List anime
```
GET /api/anime/
GET /api/anime/?status=airing
GET /api/anime/?search=naruto
GET /api/anime/?season=spring&season_year=2024
GET /api/anime/?ordering=-score
GET /api/anime/?page=2
```

### Anime detail
```
GET /api/anime/{slug}/
```

### Genres
```
GET /api/genres/
```

### Example response (`/api/anime/`)
```json
{
  "count": 500,
  "next": "http://localhost/api/anime/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Fullmetal Alchemist: Brotherhood",
      "title_english": "Fullmetal Alchemist: Brotherhood",
      "slug": "fullmetal-alchemist-brotherhood",
      "poster_url": "https://cdn.myanimelist.net/...",
      "anime_type": "tv",
      "status": "finished",
      "score": "9.10",
      "popularity": 3,
      "episodes": 64,
      "season": "spring",
      "season_year": 2009,
      "genres": [
        {"id": 1, "name": "Action", "slug": "action", "color": "#FF77C8"}
      ]
    }
  ]
}
```

---

## 🔧 Common Errors & Fixes

### ❌ `docker-compose: command not found`
```bash
# Use the newer syntax:
docker compose up -d   # (space, not hyphen)
```

### ❌ `Port 80 already in use`
Something else is using port 80 (e.g. Apache, another nginx). Stop it or change the port in `docker-compose.yml`:
```yaml
nginx:
  ports:
    - "8080:80"    # Change 80 to 8080
```
Then visit http://localhost:8080

### ❌ `relation "anime_anime" does not exist`
Migrations haven't run yet:
```bash
docker-compose exec web python manage.py migrate
```

### ❌ `No anime showing on homepage`
Data hasn't been fetched yet. Run:
```bash
docker-compose exec web python manage.py shell -c "from apps.anime.tasks import fetch_top_anime; fetch_top_anime()"
```

### ❌ `ModuleNotFoundError: No module named 'decouple'`
Virtual environment not activated (local dev):
```bash
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### ❌ `could not connect to server: Connection refused (PostgreSQL)`
PostgreSQL is not running. Start it:
```bash
# Mac:
brew services start postgresql@15

# Ubuntu:
sudo systemctl start postgresql

# Or with Docker, make sure the db container is up:
docker-compose up -d db
```

### ❌ `CSRF verification failed`
Your browser cookie is stale. Clear cookies and reload, or open an incognito window.

### ❌ Images not showing (broken image icons)
The poster images come from external URLs (MyAnimeList CDN). If they're broken, the anime was fetched without image data. Re-run fetch tasks or check your internet connection during the fetch.

### ❌ Celery tasks not running
```bash
# Check if Celery is running:
docker-compose ps celery

# Restart Celery:
docker-compose restart celery celery-beat

# View Celery logs:
docker-compose logs celery
```

---

## 🚀 Production Deployment Notes

When deploying to a live server (VPS, cloud, etc.), make these changes:

### 1. Update `.env` for production

```env
SECRET_KEY=generate-a-real-secret-key-here-use-python-secrets-module
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

SITE_URL=https://yourdomain.com
```

Generate a proper secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 2. Set up HTTPS

Edit `nginx/nginx.conf` to add SSL certificates (Let's Encrypt recommended):
```bash
# On your server, install certbot:
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 3. Use stronger database password

In `.env`:
```env
DB_PASSWORD=use-a-very-long-random-password-here
```

### 4. Set up email (for password reset, verification)

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### 5. Deploy

```bash
git push to your server
docker-compose -f docker-compose.yml up -d --build
docker-compose exec web python manage.py migrate
```

---

## 🎨 Customization Quick Reference

### Change the site name
Edit `sakurastream/settings.py`:
```python
SITE_NAME = 'YourSiteName'
SITE_TAGLINE = 'Your custom tagline'
```

### Change colors
Edit `templates/base.html` in the Tailwind config block:
```javascript
colors: {
    sakura: '#FF77C8',    // ← change this
    neon: '#A855F7',      // ← and this
}
```

### Add a new page
1. Add a view in the relevant app's `views.py`
2. Add a URL in `urls.py`
3. Create a template in `templates/`

### Disable auto-fetch (save API calls)
In `sakurastream/settings.py`, comment out the CELERY_BEAT_SCHEDULE entries.

---

## 📞 Quick Reference Commands

```bash
# ── DOCKER ──────────────────────────────────
docker-compose up -d              # Start all services
docker-compose down               # Stop all services
docker-compose restart web        # Restart just the web app
docker-compose logs -f            # Watch live logs
docker-compose exec web bash      # Open shell inside container

# ── DJANGO ──────────────────────────────────
python manage.py migrate          # Apply database migrations
python manage.py makemigrations   # Create new migration files
python manage.py createsuperuser  # Create admin account
python manage.py collectstatic    # Collect static files
python manage.py shell            # Open Django Python shell
python manage.py runserver        # Start dev server

# ── CELERY ──────────────────────────────────
celery -A sakurastream worker -l info        # Start worker
celery -A sakurastream beat -l info          # Start scheduler
celery -A sakurastream inspect active        # See active tasks

# ── DATA FETCHING ────────────────────────────
# Run inside: docker-compose exec web python manage.py shell -c "..."
from apps.anime.tasks import fetch_top_anime; fetch_top_anime()
from apps.anime.tasks import fetch_trending_anime; fetch_trending_anime()
from apps.anime.tasks import fetch_seasonal_anime; fetch_seasonal_anime()
from apps.anime.tasks import fetch_upcoming_anime; fetch_upcoming_anime()
```

---

*Built with 🌸 by SakuraStream — Where Every Petal Tells an Anime Story*
