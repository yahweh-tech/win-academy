# WIN PROFESSIONAL ACADEMY

[![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)
[![Status](https://img.shields.io/badge/HealthCheck-%2Fhealth%2F-brightgreen)](http://localhost:8000/health/)

> **Official Tagline:** *"A Complete Guidelines for Higher Education & Job Service"*  
> **Managing Entity:** Run by **Win Educational Trust** (Reg. No. `379/2006`)  
> **Official Helplines:** `63817 06581` &nbsp;|&nbsp; `86681 8494`  
> **Admissions & Guidance Scope:** Medical, Paramedical, Engineering, Agriculture, Law, Arts & Science (Tamil Nadu, India & Abroad)  
> **Specialized Coaching:** Engineering Mathematics, UG/PG TRB Mathematics, CSIR-NET Mathematical Sciences, GATE Mathematics, IIT-JAM Mathematics

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Features & Architecture](#features--architecture)
4. [Local Development Setup](#local-development-setup)
5. [Database Migrations & Data Seeding](#database-migrations--data-seeding)
6. [Creating Administrator Account](#creating-administrator-account)
7. [Running Automated Tests](#running-automated-tests)
8. [Object Storage Configuration (Cloudflare R2 / AWS S3 / Backblaze B2)](#object-storage-configuration)
9. [Django Admin Portal & Study Material Uploads](#django-admin-portal)
10. [Docker & Docker Compose](#docker--docker-compose)
11. [Render Deployment Guide](#render-deployment-guide)
12. [Connecting a Custom Domain](#connecting-a-custom-domain)
13. [Operational Health Check & Monitoring](#operational-health-check)
14. [Security Best Practices](#security-best-practices)

---

## 1. Project Overview

**WIN PROFESSIONAL ACADEMY** is a production-grade educational web application and administration platform. It provides public visitors with comprehensive information on academic admissions across Tamil Nadu and premier institutions worldwide, alongside course registration, downloadable study materials, and student achievement showcases. 

For the academy owner and staff, it provides a centralized administration portal to manage courses, upload PDF notes, notebooks, and reference books to persistent cloud object storage, and process incoming student inquiries and admission applications in real time.

---

## 2. Technology Stack

- **Backend**: Python 3.14 / 3.12, Django 5.1 (Monolithic Architecture)
- **Database**: PostgreSQL 16 (Production / Render / Docker) & SQLite (Local fallback)
- **Persistent Storage**: S3-Compatible Object Storage (Cloudflare R2 / AWS S3 / Backblaze B2) via `django-storages` and `boto3`
- **Static Assets**: WhiteNoise with Brotli / Gzip compression and hash manifests
- **WSGI Production Server**: Gunicorn with multi-worker concurrency
- **Containerization**: Multi-stage production `Dockerfile` & `docker-compose.yml`
- **Deployment Platform**: Render (`render.yaml` blueprint with managed PostgreSQL and automated health checks)
- **Styling**: Vanilla CSS Design System with Outfit & Plus Jakarta Sans typography, Navy/Red/Gold brand identity

---

## 3. Features & Architecture

```
                                +---------------------------+
                                |  Public Visitors / Mobile |
                                +-------------+-------------+
                                              |
                                              v
                               +-----------------------------+
                               |  Gunicorn + WhiteNoise WSGI |
                               +--------------+--------------+
                                              |
                                              v
                              +-------------------------------+
                              |    Django Core Monolith       |
                              |  - Public Catalog & Pages     |
                              |  - Admission Application Form |
                              |  - Contact Enquiries Form     |
                              |  - Branded Django Admin       |
                              +-------+---------------+-------+
                                      |               |
                    +-----------------+               +------------------+
                    v                                                    v
         +--------------------+                                +-------------------+
         | PostgreSQL 16 DB   |                                | S3 Object Storage |
         | - Courses & Schema |                                | (Cloudflare R2/S3)|
         | - Inquiries & Apps |                                | - PDF Study Notes |
         | - Results & Toppers|                                | - Books/Notebooks |
         +--------------------+                                +-------------------+
```

- **Public Pages**:
  - `Home`: Brand showcase, Trust & Reg badge, Admission Guidance streams (Medical, Paramedical, Engineering, Agriculture, Law, Arts & Science), 5 Core Mathematics courses, Results preview, Quick enrollment card.
  - `Courses`: Filterable courses catalog with keyword search and category filters.
  - `Course Details`: In-depth syllabus breakdown, key highlights, downloadable study materials, and direct registration modal.
  - `About Us`: Win Educational Trust history (Reg. No. 379/2006), mission, vision, and guidance services.
  - `Results`: Student Hall of Fame filterable by competitive examination (CSIR-NET, GATE, TRB, JAM).
  - `Contact`: Validated contact form storing submissions directly in PostgreSQL, interactive helpline dials.
  - `Admissions Open`: Dedicated application form capturing student details, stream preference, and qualifications.
- **Admin Management**:
  - Course creation, syllabus updating, and inline study material file attachments.
  - Admission application lifecycle management (`PENDING` -> `CONTACTED` -> `ADMITTED` -> `CLOSED`).
  - Contact enquiry resolution tracking.
  - Dynamic branding and phone number updates without code changes.

---

## 4. Local Development Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.12 and 3.14)
- Git
- PostgreSQL (optional for local dev, SQLite is used by default)

### 1. Clone the repository
```bash
git clone <repository-url>
cd "win academy"
```

### 2. Create and activate a virtual environment
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create local environment file
```bash
cp .env.example .env
```

---

## 5. Database Migrations & Data Seeding

Apply Django migrations and seed the initial academy branding, the 5 Mathematics courses, 6 guidance streams, sample study materials, and verified results:

```bash
# Apply migrations
python manage.py migrate

# Seed official academy data
python manage.py seed_academy_data
```

Output:
```text
Seeding WIN PROFESSIONAL ACADEMY database...
[OK] Academy profile & branding seeded.
[OK] Course categories created.
[OK] 5 Mathematics courses and study material references seeded.
[OK] 6 Admission guidance streams seeded.
[OK] Student results & achievements seeded.
[SUCCESS] WIN PROFESSIONAL ACADEMY database seeding completed successfully!
```

---

## 6. Creating Administrator Account

To access the Django Admin portal (`http://127.0.0.1:8000/admin/`):

```bash
python manage.py createsuperuser
```
Follow the prompt to set your username, email, and password.

---

## 7. Running Automated Tests

Run the comprehensive test suite verifying models, views, forms, security validators, and health check:

```bash
python manage.py test
```

---

## 8. Object Storage Configuration

In production environments (like Render), files stored on local disks are ephemeral and will be wiped upon restarting or redeploying. To ensure all uploaded PDF notes, notebooks, and reference books remain permanently accessible, configure an S3-compatible object storage provider.

### Recommended Provider: Cloudflare R2 (Generous Free Tier)
- **Free Tier Allowance**: 10 GB storage per month, 1,000,000 Class A operations, 10,000,000 Class B operations, and **$0 egress fees**.
- **Setup Steps**:
  1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com/) and navigate to **R2**.
  2. Click **Create Bucket** and name it `win-academy-media`.
  3. Under **Manage R2 API Tokens**, click **Create API Token** with `Object Read & Write` permissions.
  4. Copy the **Access Key ID**, **Secret Access Key**, and the **Endpoint URL** (e.g. `https://<account_id>.r2.cloudflarestorage.com`).
  5. In your `.env` or Render environment variables, configure:
     ```env
     USE_S3_STORAGE=True
     STORAGE_ENDPOINT_URL=https://<account_id>.r2.cloudflarestorage.com
     STORAGE_ACCESS_KEY=<your_access_key_id>
     STORAGE_SECRET_KEY=<your_secret_access_key>
     STORAGE_BUCKET_NAME=win-academy-media
     STORAGE_REGION=auto
     ```

### Alternative: AWS S3 or Backblaze B2
Set `USE_S3_STORAGE=True` and provide the corresponding standard `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`, `STORAGE_BUCKET_NAME`, and `STORAGE_REGION` (e.g., `ap-south-1` for AWS Mumbai).

---

## 9. Django Admin Portal

1. Start the server:
   ```bash
   python manage.py runserver
   ```
2. Navigate to `http://127.0.0.1:8000/admin/` and sign in.
3. **Managing Courses & Materials**:
   - Go to **Courses** -> **Add Course** or edit an existing one.
   - Attach syllabus topics, audience level, and batch modes.
   - Use the **Course Materials** inline section to upload PDF notes, formula compendiums, or books directly.
4. **Processing Admissions & Inquiries**:
   - View incoming submissions in **Admission & Guidance Applications**.
   - Update statuses from `Pending Review` -> `Counselor Contacted` -> `Admission Confirmed`.
   - Manage incoming contact queries with one-click **Mark as Resolved** action.
5. **Editing Academy Profile & Helplines**:
   - Edit the singleton **Academy Profile & Branding** to change phone numbers (`63817 06581`, `86681 8494`), official address, mission, vision, or registration details at any time.

---

## 10. Docker & Docker Compose

### Run with Docker Compose (PostgreSQL 16 + Django Web Service)
```bash
# Build and start services in background
docker compose up --build -d

# View service logs
docker compose logs -f

# Stop services
docker compose down
```
Access the application at `http://localhost:8000`.

### Manual Single Container Build
```bash
docker build -t win-academy:latest .
docker run -p 8000:8000 -e SECRET_KEY="prod-key" -e DEBUG="False" win-academy:latest
```

---

## 11. Render Deployment Guide

This repository includes a native `render.yaml` Blueprint that provisions both the **Web Service** and a **Managed PostgreSQL Database**.

### Option A: 1-Click Render Blueprint Deployment (Recommended)
1. Push this codebase to a private or public GitHub repository.
2. In the [Render Dashboard](https://dashboard.render.com/), click **New +** -> **Blueprint**.
3. Connect your GitHub repository.
4. Render will automatically detect `render.yaml` and configure:
   - Web Service (`win-professional-academy`)
   - PostgreSQL Database (`win-academy-db`)
   - Pre-deploy migrations (`python manage.py migrate && python manage.py seed_academy_data`)
   - Gunicorn startup command with health check `/health/`
5. Click **Apply**. Render will build and deploy the application automatically.

### Option B: Manual Web Service Setup on Render
1. Create a **PostgreSQL Database** on Render:
   - Name: `win-academy-db`
   - Copy the **Internal Database URL**.
2. Create a **Web Service**:
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --no-input`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 3 --threads 2 config.wsgi:application`
   - Health Check Path: `/health/`
3. Add Environment Variables:
   - `DEBUG`: `False`
   - `SECRET_KEY`: *(Generate a secure random string)*
   - `DATABASE_URL`: *(Paste Render PostgreSQL URL)*
   - `ALLOWED_HOSTS`: `.onrender.com,yourcustomdomain.com`
   - `CSRF_TRUSTED_ORIGINS`: `https://*.onrender.com,https://yourcustomdomain.com`
   - `USE_S3_STORAGE`: `True` *(when object storage credentials are ready)*
   - `STORAGE_ENDPOINT_URL`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`, `STORAGE_BUCKET_NAME`

---

## 12. Connecting a Custom Domain

When the academy is ready to connect their official custom domain (e.g. `winacademy.edu.in`):

1. **In Render Dashboard**:
   - Go to your Web Service -> **Settings** -> **Custom Domains**.
   - Add `winacademy.edu.in` and `www.winacademy.edu.in`.
2. **In Domain DNS Registrar (e.g., GoDaddy, Namecheap, Cloudflare)**:
   - Add a `CNAME` record: `www` pointing to `<your-app-name>.onrender.com`
   - Add an `A` / `ALIAS` record: `@` pointing to Render's IP address (provided in Render dashboard).
3. **Update Environment Variables**:
   - Add `winacademy.edu.in,www.winacademy.edu.in` to `ALLOWED_HOSTS`.
   - Add `https://winacademy.edu.in,https://www.winacademy.edu.in` to `CSRF_TRUSTED_ORIGINS`.
4. Render automatically provisions free, auto-renewing Let's Encrypt SSL certificates for HTTPS.

---

## 13. Operational Health Check & Monitoring

The system exposes a public health endpoint at `/health/` designed for uptime monitors, Render health probes, and Docker container healthchecks.

### Request:
```http
GET /health/
```

### Healthy Response (HTTP 200):
```json
{
  "status": "ok",
  "database": "connected",
  "academy": "WIN PROFESSIONAL ACADEMY",
  "trust": "Win Educational Trust (Reg. No. 379/2006)",
  "tagline": "A Complete Guidelines for Higher Education & Job Service"
}
```

---

## 14. Security Best Practices

- **Zero Hardcoded Secrets**: All credentials, keys, and tokens are read exclusively through environment variables.
- **CSRF & XSS Protection**: Enabled on all forms with hidden honeypot validation to eliminate automated spam bots.
- **File Upload Security**: Strict validation of MIME types and extensions (`.pdf`, `.docx`, `.png`, `.jpg`), maximum file size limits (50MB), and sanitized slug-based storage paths.
- **Production Headers**: Auto-configured HSTS, X-Frame-Options (`DENY`), Content-Type-No-Sniff, and Secure Cookies when `DEBUG=False`.

---

## License & Handover

Developed for **WIN PROFESSIONAL ACADEMY**  
Managed by **Win Educational Trust (Reg. No. 379/2006)**  
Official Helplines: `63817 06581` / `86681 8494`
