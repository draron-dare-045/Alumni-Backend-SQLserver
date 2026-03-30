# Alumni Management System — Backend

A high-performance Django-based backend designed to manage university alumni records. This project integrates a Django 4.2+ application with a Microsoft SQL Server 2022 instance running inside a Docker container.

> This README is written for Ubuntu users onboarding a project cloned from https://github.com/draron-dare-045/Alumni-Backend-SQLserver.git. It includes explicit commands to allow another human or AI pair programmer to execute it end-to-end.

---

## 🚀 Architecture Overview

| Layer | Technology |
|---|---|
| Backend | Django (Python 3.9+) |
| API Layer | Django REST Framework (DRF) |
| Database | Microsoft SQL Server 2022 (Linux-based Docker image) |
| Connectivity | `mssql-django` & `pyodbc` (ODBC Driver 18) |
| Infrastructure | Docker Desktop / Engine on Ubuntu |

---

## 🛠️ Getting Started

### 1. Database Infrastructure (Docker)

To ensure a clean, isolated setup, we use a single containerized SQL Server instance.

> **Critical Note on Port Management:** Ensure no other SQL Server instances are running on port `1433`. If you previously had multiple containers (e.g., on `1434`), stop them before proceeding to avoid **Error 4060** (Database not found).

```bash
# 1. Kill any existing SQL containers to free up port 1433
docker stop alumni_db_container && docker rm alumni_db_container

# 2. Start the fresh SQL Server Container
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=@Ar0n2006" \
    -p 1433:1433 --name alumni_db_container \
    --restart always \
    -d mcr.microsoft.com/mssql/server:2022-latest
```

---

### 2. Schema and Data Restoration

Wait ~15 seconds for the server to initialize, then copy the local `.sql` scripts into the container to build the relational structure.

**Create the Database:**

```bash
docker exec -it alumni_db_container /opt/mssql-tools18/bin/sqlcmd \
    -S localhost -U sa -P @Ar0n2006 -C -Q "CREATE DATABASE Alumnidb;"
```

**Import Schema & Seed Data:**

```bash
# Copy files to container
docker cp Tables+Constraints.sql alumni_db_container:/Tables+Constraints.sql
docker cp AlumniDataInsert.sql alumni_db_container:/AlumniDataInsert.sql

# Execute Schema Script
docker exec -it alumni_db_container /opt/mssql-tools18/bin/sqlcmd \
    -S localhost -U sa -P @Ar0n2006 -C -d Alumnidb -i /Tables+Constraints.sql

# Execute Data Seed Script
docker exec -it alumni_db_container /opt/mssql-tools18/bin/sqlcmd \
    -S localhost -U sa -P @Ar0n2006 -C -d Alumnidb -i /AlumniDataInsert.sql
```

---

## 🔌 Django — SQL Server Integration

This project follows a **Database-First** development workflow. We reverse-engineer the SQL Server schema into Django models using the `inspectdb` utility.

```bash
# Map existing SQL Server tables to Python classes
python manage.py inspectdb > alumni_app/models.py
```

### Database Configuration (`settings.py`)

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'Alumnidb',
        'USER': 'sa',
        'PASSWORD': '@Ar0n2006',
        'HOST': '127.0.0.1',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'Encrypt=no;TrustServerCertificate=yes',
        },
    }
}
```

---

## 🔍 Troubleshooting & Lessons Learned

### Common Issues & Solutions

1. **ODBC Driver Not Found (Windows)**
   - Download and install [Microsoft ODBC Driver 18 for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
   - Ensure the driver name in `settings.py` matches: `'ODBC Driver 18 for SQL Server'`

2. **Docker Container Not Starting**
   - Ensure Docker Desktop is running
   - Check port 1433 is not in use: `netstat -ano | findstr :1433`
   - Remove old containers: `docker rm alumni_db_container`

3. **Database Connection Fails**
   - Wait 30+ seconds after starting container for SQL Server initialization
   - Verify password and credentials match Docker run command
   - Check firewall allows port 1433

4. **Import Errors in Python**
   - Ensure all packages installed: `pip install -r requirements.txt`
   - Use virtual environment: `python -m venv venv` then `venv\Scripts\activate`

### New Features Added
- **Chapters Management**: Added support for local and international alumni chapters
- **Automated Setup**: Use `setup.ps1` script for Windows setup
- **Enhanced Alumni Serializer**: Includes chapter information

### API Endpoints for Chapters
- `GET /api/admin/chapters/` - List all chapters
- `POST /api/admin/chapters/` - Create new chapter

### 1. Port Conflict & Error 4060

**Issue:** Multiple containers running on different ports (`1433` vs `1434`) led to login failures because Django was hitting a container instance that did not contain the `Alumnidb` database.

**Fix:** Standardized on port `1433` and used the following command to force the correct database context:

```sql
ALTER LOGIN sa WITH DEFAULT_DATABASE = Alumnidb;
```

### 2. Identity Insert Errors

**Issue:** `Msg 544` occurred when trying to manually insert Primary Keys into tables with `IDENTITY` columns.

**Fix:** Wrapped insert statements with `SET IDENTITY_INSERT` toggled on and off:

```sql
SET IDENTITY_INSERT [TableName] ON;
-- your INSERT statements here
SET IDENTITY_INSERT [TableName] OFF;
```

---

## 📡 API Endpoints (REST)

| Endpoint | Method | Description |
|---|---|---|
| `/api/alumni/` | `GET` | Lists all registered alumni records |

---

## 🛡️ Security & Environment

> **Important:** The credentials shown in this README are for local development only. Follow the guidance below before deploying to any shared or production environment.

- **Environment Variables:** Move credentials like `MSSQL_SA_PASSWORD` and Django's `SECRET_KEY` to a `.env` file and add it to `.gitignore` to prevent accidental exposure.
- **ODBC Security:** `TrustServerCertificate=yes` is acceptable for local development. Production deployments **must** use valid SSL/TLS certificates and set `Encrypt=yes`.

---

## 📝 Deploying to Ubuntu (Recommended)

This section is explicitly written for Ubuntu developers and automated AI assistants to follow step-by-step.

### Prerequisites

1. Ubuntu 20.04+ (or equivalent 64-bit Linux)
2. Docker & Docker Compose installed
   - `sudo apt update && sudo apt install -y docker.io docker-compose`
   - `sudo usermod -aG docker $USER` (log out/in thereafter)
3. Python 3.12+, `pip`, and `venv`
   - `sudo apt install -y python3 python3-venv python3-pip`
4. Git installed
   - `sudo apt install -y git`

### Clone repos

```bash
cd ~/projects
git clone https://github.com/draron-dare-045/Alumni-Backend-SQLserver.git
git clone https://github.com/draron-dare-045/Alumni-system.git
```

### Backend setup (Alumni-Backend-SQLserver)

```bash
cd ~/projects/Alumni-Backend-SQLserver
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Start SQL Server in Docker

```bash
# cleanup existing container (if exists)
docker rm -f alumni_db_container 2>/dev/null || true

docker run -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=@Ar0n2006' \
  -p 1433:1433 --name alumni_db_container --restart always \
  -d mcr.microsoft.com/mssql/server:2022-latest

# wait for SQL Server to be ready
sleep 30

# create database
docker exec alumni_db_container /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P '@Ar0n2006' -C -Q 'CREATE DATABASE Alumnidb;'

# apply schema and data

docker cp Tables+Constraints.sql alumni_db_container:/Tables+Constraints.sql
docker cp AlumniDataInsert.sql alumni_db_container:/AlumniDataInsert.sql

docker exec -it alumni_db_container /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P '@Ar0n2006' -C -d Alumnidb -i /Tables+Constraints.sql

docker exec -it alumni_db_container /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P '@Ar0n2006' -C -d Alumnidb -i /AlumniDataInsert.sql
```

### Django configuration check

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Browse: `http://localhost:8000/api/alumni/` (should return JSON)

---

## Frontend setup (Alumni-system)

```bash
cd ~/projects/Alumni-system
npm install
npm run build
npm run dev
```

Then open: `http://localhost:3000`

### Frontend plain page troubleshooting

If page content appears unstyled:

1. Ensure the correct Next.js process is running from this repo.
2. Hard refresh browser: `Ctrl+F5` (or `Cmd+Shift+R`).
3. Check network tab for style file status (`/_next/static/css/app/layout.css`).
4. Run `npm run build` then `npm run dev` to regenerate assets.

---

## Local development workflow for AI/pair programmers

1. Ensure backend and frontend are in separate directories.
2. Start backend first, then frontend.
3. Run - `curl -s http://localhost:8000/api/alumni/ | head` and ensure valid JSON.
4. Run - `curl -s http://localhost:3000 | grep -q "bg-gradient-to-br"` proof of Tailwind CSS classes in HTML.
5. If this fails, stop servers, delete `.next` folder and rerun `npm run build`.

## Project health checks

- `docker ps` states `alumni_db_container` running and exposing port 1433.
- `python manage.py runserver` shows no errors.
- `npm run dev` shows CSS file path and Next.js route loaded.

## 📝 License

This project is licensed under the [MIT License](LICENSE).