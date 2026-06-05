#!/bin/bash

# CONFIG
HOST="sftp.example.com"
USER="your_username"
PORT=22
LOCAL_DIR="/path/to/local/files"
REMOTE_DIR="/path/to/remote/files"
KEY="/path/to/private_key"
LOG_FILE="/var/log/sftp_transfer.log"

# Start log
echo "===== SFTP Transfer Started: $(date) =====" >>"$LOG_FILE"

# Run SFTP batch commands
sftp -i "$KEY" -P "$PORT" "$USER@$HOST" >>"$LOG_FILE" 2>&1 <<EOF
cd $REMOTE_DIR
lcd $LOCAL_DIR
mput *
bye
EOF

# Check result
if [ $? -eq 0 ]; then
  echo "Transfer successful: $(date)" >>"$LOG_FILE"
else
  echo "Transfer FAILED: $(date)" >>"$LOG_FILE"
fi

echo "===== SFTP Transfer Ended: $(date) =====" >>"$LOG_FILE"
