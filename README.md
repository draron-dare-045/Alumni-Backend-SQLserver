# Alumni Management System — Backend

A high-performance Django-based backend designed to manage university alumni records. This project integrates a Django 4.2+ application with a Microsoft SQL Server 2022 instance running inside a Docker container.

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

## 📝 License

This project is licensed under the [MIT License](LICENSE).