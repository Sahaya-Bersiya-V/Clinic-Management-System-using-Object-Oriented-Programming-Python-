---
description: Enforce Team Lead Git Workflow: Sync task branch, pull dev, push task, merge, and push dev. Use this when ready to deploy changes.
---
1. Switch to task branch
   `git checkout team_lead_task`
2. Pull latest task branch changes
   `git pull origin team_lead_task`
3. Pull development into task branch to resolve conflicts locally
   `git pull origin development`
4. Push task branch to remote
   `git push origin team_lead_task`
5. Switch to development branch
   `git checkout development`
6. Pull latest development branch changes
   `git pull origin development`
7. Merge task branch into development
   `git merge team_lead_task`
8. Push development branch to remote
   `git push origin development`
