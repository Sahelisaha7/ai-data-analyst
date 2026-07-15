# Docker Deployment Guide

Deploy your AI Data Analyst project using Docker.

## Prerequisites

1. **Install Docker Desktop**
   - Windows: https://www.docker.com/products/docker-desktop
   - Mac: https://www.docker.com/products/docker-desktop
   - Linux: https://docs.docker.com/install/

2. **Verify Installation**
   ```bash
   docker --version
   docker-compose --version
   ```

## Quick Start (2 methods)

### Method 1: Using Docker Compose (Easiest)

**Step 1: Build the image**
```bash
docker-compose build
```

**Step 2: Run the container**
```bash
docker-compose up
```

The app will start in the container!

---

### Method 2: Using Docker Commands

**Step 1: Build the Docker image**
```bash
docker build -t ai-data-analyst .
```

**Step 2: Run the container**
```bash
docker run -it \
  -e ANTHROPIC_API_KEY=sk-ant-your-key-here \
  ai-data-analyst
```

---

## Advanced Commands

### View running containers
```bash
docker ps
```

### View container logs
```bash
docker logs ai-data-analyst
```

### Stop the container
```bash
docker stop ai-data-analyst
```

### Remove the container
```bash
docker rm ai-data-analyst
```

### Remove the image
```bash
docker rmi ai-data-analyst
```

---

## Deploy to Cloud

### Option A: Deploy to Railway (Free)

1. Create account: https://railway.app
2. Connect GitHub repo
3. Create new project
4. Select "Docker"
5. Railway auto-deploys!

### Option B: Deploy to Render (Free)

1. Create account: https://render.com
2. Connect GitHub repo
3. Create new service
4. Select "Docker"
5. Set environment variables
6. Deploy!

### Option C: Deploy to AWS (Paid)

1. Create ECR repository
2. Push Docker image:
   ```bash
   docker tag ai-data-analyst:latest your-registry/ai-data-analyst:latest
   docker push your-registry/ai-data-analyst:latest
   ```
3. Deploy using ECS/EKS

---

## Environment Variables

Create `.env.docker` for production:
```
ANTHROPIC_API_KEY=sk-ant-your-production-key
```

Then run:
```bash
docker run --env-file .env.docker ai-data-analyst
```

---

## Troubleshooting

### "Docker command not found"
- Restart terminal after Docker installation
- Or restart your computer

### "Port already in use"
```bash
docker run -p 8001:8000 ai-data-analyst
```

### "Permission denied"
On Linux, add user to docker group:
```bash
sudo usermod -aG docker $USER
```

### Check image size
```bash
docker images
```

---

## File Structure

```
ai-data-analyst/
├── Dockerfile              ← Docker configuration
├── docker-compose.yml      ← Container orchestration
├── .dockerignore           ← Exclude files from image
├── main.py
├── amazon.db
├── customers.csv
├── products.csv
├── orders.csv
├── order_items.csv
├── requirements.txt
└── .env
```

---

## Security Notes

⚠️ **Never commit .env to GitHub!**

```bash
# In .gitignore
.env
.env.*.local
```

✅ Use GitHub Secrets for production keys:
- Settings → Secrets → New repository secret
- Add: ANTHROPIC_API_KEY

---

## Next Steps

1. Build: `docker-compose build`
2. Run: `docker-compose up`
3. Test the app
4. Deploy to Railway/Render/AWS

---

## Quick Commands Cheatsheet

```bash
# Build
docker build -t ai-data-analyst .

# Run interactive
docker run -it ai-data-analyst

# Run with env vars
docker run -e ANTHROPIC_API_KEY=sk-ant-xxx ai-data-analyst

# Run in background
docker run -d ai-data-analyst

# View logs
docker logs ai-data-analyst

# List images
docker images

# List containers
docker ps -a

# Remove image
docker rmi ai-data-analyst
```

---

## Support

- Docker Docs: https://docs.docker.com
- Docker Hub: https://hub.docker.com
- Railway: https://railway.app/docs
- Render: https://render.com/docs
