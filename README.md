# Alumni Management System - Backend

A high-performance Django-based backend designed to manage university alumni records. This project integrates a **Django 5.x** application with a **Microsoft SQL Server 2022** instance running inside a **Docker** container.

## 🚀 Architecture Overview

* **Backend:** Django (Python 3.x)
* **Database:** Microsoft SQL Server 2022 (Linux-based Docker image)
* **Connectivity:** `django-mssql-backend` & `pyodbc`
* **Infrastructure:** Docker Desktop / Engine on Ubuntu

---

## 🛠️ Getting Started

### 1. Database Infrastructure (Docker)

The database is hosted in a containerized environment to ensure a clean, isolated setup.

```bash
# Start the SQL Server Container
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=@Ar0n2006" \
    -p 1433:1433 --name alumni_db_container \
    --restart always \
    -d mcr.microsoft.com/mssql/server:2022-latest
```

### 2. Schema and Data Restoration

We use raw SQL scripts to build the relational structure and populate the initial seed data.

#### Create the Database:

```bash
docker exec -it alumni_db_container /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P @Ar0n2006 -C -Q "CREATE DATABASE Alumnidb;"
```

#### Import Schema & Constraints:

```bash
docker exec -it alumni_db_container /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P @Ar0n2006 -C -i /Tables+Constraints.sql
```

#### Seed Alumni Data:

(Note: Ensure IDENTITY_INSERT is toggled if your script includes manual IDs)

```bash
docker exec -it alumni_db_container /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P @Ar0n2006 -C -i /AlumniDataInsert.sql
```

---

## 📂 Project Structure

* **alumni_system/** - Core Django configuration and settings.
* **alumni_app/** - Application logic and auto-generated database models.
* **manage.py** - Django administrative task runner.
* **\*.sql** - Database migration and seeding scripts.

---

## 🔌 Django - SQL Server Integration

This project uses Database-First development. We map the existing SQL Server tables to Python classes using Django's inspection utility:

```bash
python manage.py inspectdb > alumni_app/models.py
```

### Database Configuration (settings.py)

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
            'extra_params': 'TrustServerCertificate=yes',
        },
    }
}
```

---

## 🛡️ Security & Environment

* **Environment Variables:** Credentials like MSSQL_SA_PASSWORD should be stored in a `.env` file and excluded from version control via `.gitignore`.
* **Database Access:** Remote connections are restricted by the Docker port mapping; use local port 1433 for development.

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
