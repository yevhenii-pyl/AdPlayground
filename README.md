## ⚙️ Setup Instructions

### 1. Clone the repo and install dependencies

```bash
git clone <repo-url>
cd AdPlayground
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set up .env

### 3. Start the MySQL database

```bash 
docker compose up --build -d
```

### 3.1. Fix ad_events table 
```bash
python /scripts/utils/fix_events.py
```

This dataset may be broken, so we have to clean it up first. 


### 4. Run the seeders

```bash
python scripts/run_seeders.py
```

### 5. Verify in MySQL

```bash
mysql -u root -p -h {MYSQL_HOST} -P 3306 {MYSQL_DB}
```

## RDBMS sreenshots are available at assets folder