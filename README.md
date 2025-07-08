# CosmosDB MongoDB API AKS Scheduled Backup Solution

## Overview
- Daily scheduled backup of CosmosDB (MongoDB API) database, each collection exported as a separate JSON file, organized by MM-DD-YYYY directory.
- Backup files and logs are persisted in Azure File storage.

## Directory Structure
```
/mnt/backup/MM-DD-YYYY/
  |- collection1.json
  |- collection2.json
  |- ...
  |- log.txt
```

## Main Files
- `backup_cosmosdb.py`: Backup script, CosmosDB connection info must be filled in.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Container image build file.
- `cosmosdb-backup-cronjob.yaml`: K8s CronJob configuration.
- `azurefile-pv-pvc.yaml`: Azure File persistent volume and claim.

## Usage
1. Edit `backup_cosmosdb.py` and fill in your CosmosDB connection info.
2. Build and push the image:
   ```
   docker build -t <your-registry>/backup-cosmosdb:latest .
   docker push <your-registry>/backup-cosmosdb:latest
   ```
3. Create Azure File storage, K8s Secret (`azure-secret`), PV/PVC (see `azurefile-pv-pvc.yaml`).
4. Deploy the CronJob (see `cosmosdb-backup-cronjob.yaml`), ensure PVC name matches.
5. Check backup files and logs under /mnt/backup.

## Notes
- Connection info is hardcoded in the script; for production, consider using K8s Secret.
- Backup directories and files will be overwritten if they already exist.
- The log file log.txt records details of each backup run.
- Azure File storage and related secrets must be prepared in advance.

## Dependencies
- Python 3.11+
- pymongo

## Restore
- For restore, use a Python script or mongoimport tool. Clear the target database before importing each collection's JSON file. 