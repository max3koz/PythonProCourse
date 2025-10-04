#!/bin/bash

# === Setting ===
MONGO_URI="mongodb://localhost:27017"
BACKUP_DIR="/var/backups/mongodb"
DATE=$(date +%F)
TARGET_DIR="$BACKUP_DIR/mongodump-$DATE"
LOG_FILE="$BACKUP_DIR/backup.log"

# === Create folder ===
mkdir -p "$TARGET_DIR"

# === Create backup ===
echo "[$(date)] Starting backup..." >> "$LOG_FILE"
mongodump --uri="$MONGO_URI" --out="$TARGET_DIR" >> "$LOG_FILE" 2>&1

# === Compression ===
tar -czf "$TARGET_DIR.tar.gz" -C "$BACKUP_DIR" "mongodump-$DATE"
rm -rf "$TARGET_DIR"

# === Logging completion ===
echo "[$(date)] Backup completed: $TARGET_DIR.tar.gz" >> "$LOG_FILE"
