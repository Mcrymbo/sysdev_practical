# Edible Oil Tonnage Calculator

Django web application for calculating edible oil tonnage using Volume Correction Factors (VCF).

## Setup

### Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for development)

### Installation
1. **Activate environment**
    ```bash
    pipenv shell
    ```

2. **Install dependencies**
   ```bash
   pipenv install
   ```

3. **Configure database**

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Import VCF data**
   ```bash
   python manage.py import_vcf vcftable.sql --clear
   ```

6. **Create superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

7. **Run server**
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000` to use the application.

## Usage

- **Home**: Enter volume, density, and temperature to calculate tonnage
- **History**: View and search calculation history
- **Admin**: Manage VCF data at `/admin`

## Formula

```
Tonnage (MT) = (Volume × Density × VCF) ÷ 1000
``` 