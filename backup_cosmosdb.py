import os
import json
import logging
from datetime import datetime
from pymongo import MongoClient

# ====== CONFIGURATION ======
COSMOSDB_URI = "mongodb://<username>:<password>@<cosmosdb-endpoint>:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@<username>@"
DATABASE_NAME = "<your_database_name>"
BACKUP_ROOT = "/mnt/backup"
# ==========================

def get_today_dir():
    today = datetime.now().strftime("%m-%d-%Y")
    return os.path.join(BACKUP_ROOT, today)

def setup_logging(backup_dir):
    log_path = os.path.join(backup_dir, "log.txt")
    logging.basicConfig(
        filename=log_path,
        filemode='w',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    return log_path

def main():
    backup_dir = get_today_dir()
    os.makedirs(backup_dir, exist_ok=True)
    setup_logging(backup_dir)
    logging.info(f"Starting backup for database: {DATABASE_NAME}")
    try:
        client = MongoClient(COSMOSDB_URI)
        db = client[DATABASE_NAME]
        collections = db.list_collection_names()
        logging.info(f"Found collections: {collections}")
        for coll_name in collections:
            try:
                coll = db[coll_name]
                docs = list(coll.find({}))
                # Convert ObjectId to string
                for doc in docs:
                    if '_id' in doc:
                        doc['_id'] = str(doc['_id'])
                out_path = os.path.join(backup_dir, f"{coll_name}.json")
                with open(out_path, 'w', encoding='utf-8') as f:
                    json.dump(docs, f, ensure_ascii=False, indent=2)
                logging.info(f"Exported {len(docs)} documents from {coll_name} to {out_path}")
            except Exception as e:
                logging.error(f"Failed to export collection {coll_name}: {e}")
        logging.info("Backup completed successfully.")
    except Exception as e:
        logging.error(f"Backup failed: {e}")

if __name__ == "__main__":
    main() 