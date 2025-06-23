## ⚙️ Setup Instructions

## Full dockerised setup

### 1. Download all assets into /data folder 

### 2. Run 

```bash
docker compose up --build
```

## Local setup: run DB in docker + python venv locally 

### 1. Clone the repo and install dependencies

```bash
git clone <repo-url>
cd AdPlayground
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set up .env && download assets at /data folder

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

## Seed Cassandra
```bash
docker exec -it adplayground-app-1 sh -c "python scripts/cassandra_seeders/mysql_to_cassandra.py"
```

## Generate CSV Reports
```bash
docker exec -it adplayground-app-1 sh -c "python scripts/reporting/cassandra_report_runner.py"
```