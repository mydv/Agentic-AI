# Agentic-AI
This repo will implement an agentic AI to resolve certain payment incidents if any

#Step 1
Enter logs from different applications to Kubernetes containers

#Step 2
Read from Kubernetes containers and provide the logs to AI Agent to analyse the logs

#Step 3
Provide fix for the issue and resolve the error generated - if no risk, else create an incident put a comment on it for developer to understand the issue better and fix in code base

# 🧠 Log Intelligence Pipeline

A modular, Kubernetes-native log analysis system that simulates payment failure logs, structures and indexes them using FAISS, and applies LangChain with local LLM inference to surface probable root causes.

---

## 📁 Project Structure
```
log-intel-pipeline/
├── app/
│   ├── main.py                         # Log generator with rotation
│   ├── LogConverter.py                 # .log → .jsonl structurer
│   ├── LogEmbedder.py                  # FAISS embedder
│   ├── LlmAgentOllamaLocalResponse.py  # LangChain-based log analyst
│   ├── logs/                           # Mounted volume for logs
│   └── faiss/                          # Mounted volume for FAISS index & metadata
├── deployment/
│   ├── Dockerfile.logger
│   ├── Dockerfile.converter
│   ├── Dockerfile.embedder
│   ├── Dockerfile.analyzer
│   ├── k8s/
│   │   ├── deployment.yaml
│   │   ├── cronjob.yaml
│   │   ├── embedder-job.yaml
│   │   ├── analyzer-job.yaml
│   │   ├── log-pvc.yaml
│   │   └── faiss-pvc.yaml
│   └── helm-log-pipeline/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── logger-deployment.yaml
│           ├── converter-cronjob.yaml
│           ├── embedder-job.yaml
│           ├── analyzer-job.yaml
│           ├── log-pvc.yaml
│           └── faiss-pvc.yaml
```

---

## ⚙️ Prerequisites

- [Docker](https://www.docker.com/)
- [Helm v3+](https://helm.sh/)
- Access to a Kubernetes cluster (local or cloud)
- Optional: [Ollama](https://ollama.com/) installed on the node for local LLM use

---

## 🐳 Build and Push Docker Images

```powershell
# Change to root folder if not already there
cd log-intel-pipeline

# Build images
docker build -f deployment\Dockerfile.logger    -t your-registry\payment-logger:latest .
docker build -f deployment\Dockerfile.converter -t your-registry\log-converter:latest .
docker build -f deployment\Dockerfile.embedder  -t your-registry\log-embedder:latest .
docker build -f deployment\Dockerfile.analyzer  -t your-registry\log-analyzer:latest .

# Push images to your Docker registry
docker push your-registry\payment-logger:latest
docker push your-registry\log-converter:latest
docker push your-registry\log-embedder:latest
docker push your-registry\log-analyzer:latest
```

🔁 Update the image: fields in deployment\helm-log-pipeline\values.yaml to match your registry.

🚀 Install with Helm
```powershell
cd deployment\helm-log-pipeline
helm install log-intel .
```

⏱ This installs:
- A Deployment generating logs (main.py)
- A CronJob converting logs every 10 minutes
- PVCs for shared storage
- Optionally, embedder and analyzer jobs can be run manually

🔁 Upgrade Release

```powershell
# Modify values.yaml or use --set overrides
helm upgrade log-intel .
```
🔻 Uninstall Release

```powershell
helm uninstall log-intel
```
🧹 Remove persistent volumes if no longer needed:

```powershell
kubectl delete pvc log-pvc,faiss-pvc
```
📊 Run FAISS Embedder & Analyzer (manually)

```powershell
kubectl apply -f deployment\k8s\embedder-job.yaml
kubectl apply -f deployment\k8s\analyzer-job.yaml
```