---
description: Deploy the latest code to the Oracle Cloud VM
---
1. Push local changes to GitHub
```powershell
git add .
git commit -m "chore: update for deploy"
git push origin main
```
2. Sync config/secrets (optional but recommended)
// turbo
```powershell
scp -i ssh-key-2026-01-16.key -o StrictHostKeyChecking=no access_keys.txt ubuntu@163.176.169.206:~/dashboard/
```
3. Connect to VM, pull changes, install dependencies, and restart service
// turbo
```powershell
ssh -i ssh-key-2026-01-16.key -o StrictHostKeyChecking=no ubuntu@163.176.169.206 "cd dashboard && git pull && source venv/bin/activate && pip install -r requirements.txt && sudo systemctl restart dashboard"
```
