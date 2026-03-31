# 🩺 MediQuery.ai: Advanced Medical RAG Chatbot

[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/Framework-LangChain-green.svg)](https://python.langchain.com/)
[![AWS ECR](https://img.shields.io/badge/AWS-ECR-orange.svg)](https://aws.amazon.com/ecr/)
[![Docker](https://img.shields.io/badge/Container-Docker-blue.svg)](https://www.docker.com/)

**MediQuery.ai** is a professional-grade medical assistant built using a **Retrieval-Augmented Generation (RAG)** architecture. It answers questions based on your indexed medical documents instead of raw LLM hallucinations, improving accuracy and trustworthiness.

---

## 📸 Demo Showcase

Modern, responsive UI with **Dark Mode** toggle for optimal readability.

| 🌙 Dark Mode (Default) | ☀️ Light Mode |
| :----------------------: | :-----------: |
| <img src="assets/Screenshot%202026-03-27%20013749.png" width="800" alt="MediQuery AI Dark Mode"/> | <img src="assets/Screenshot%202026-03-27%20013825.png" width="800" alt="MediQuery AI Light Mode"/> |

---

## 🚀 Key Features

- **Context‑aware answers:**  
  Powered by **LangChain** and **Groq (Llama‑3.3‑70B)** for fast, accurate medical reasoning grounded in your documents.
- **Semantic search:**  
  Uses **Pinecone** for real‑time similarity search over embedded medical text.
- **Modern UI:**  
  Clean, responsive Flask frontend with **Dark Mode**, **glassmorphism**, and real‑time thinking indicators.
- **Automated deployment:**  
  Fully integrated **CI/CD pipeline** (GitHub Actions → AWS ECR → EC2/Docker).

---

## 🛠️ Tech Stack

| Category              | Technology |
| :-------------------- | :--------- |
| **LLM Framework**     | LangChain |
| **Large Language Model** | Groq (`llama3-70b-8192`) |
| **Vector Database**   | Pinecone |
| **Embeddings**        | HuggingFace (`all-MiniLM-L6-v2`) |
| **Backend**           | Flask (Python 3.10) |
| **Frontend**          | HTML5, CSS3, JavaScript (AJAX) |
| **Cloud / DevOps**    | AWS (EC2, ECR), Docker, GitHub Actions |

---

## 📂 Project Structure

```text
.
├── app.py              # Flask app (routes & RAG logic)
├── store_index.py      # Script to populate Pinecone index
├── src/
│   ├── helper.py       # Helper functions (embeddings, utils)
│   └── prompt.py       # System / RAG prompts
├── assets/             # Screenshots (linked above)
├── static/             # CSS / JS, images (Dark Mode styles)
├── templates/          # HTML templates (chat.html)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker build config
└── .github/workflows   # GitHub Actions CI/CD workflows
```

---

## 🚀 How to Run Locally

1. **Clone the repository**

   ```bash
   git clone https://github.com/salonyranjan/MediQuery.ai.git
   cd MediQuery.ai
   ```

2. **Create a conda environment**

   ```bash
   conda create -n medibot python=3.10 -y
   conda activate medibot
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**

   Create `.env` in the root directory and add:

   ```text
   PINECONE_API_KEY=xxxxxxxxxxxxxxxx
   OPENAI_API_KEY=xxxxxxxxxxxxxxxx
   GROQ_API_KEY=xxxxxxxxxxxxxxxx
   ```

   Replace values with your actual API keys.

5. **Build the vector index**

   ```bash
   python store_index.py
   ```

6. **Run the app**

   ```bash
   python app.py
   ```

   Open your browser:http://localhost:8080

text

---

## 🐳 Docker Quick Start (no conda)

If you prefer running via Docker:

```bash
# 1. Build the image
docker build -t mediquery .

# 2. Run the container
docker run -d -p 8080:8080 \
-e PINECONE_API_KEY="xxxxxxxxxxxxxxxx" \
-e GROQ_API_KEY="xxxxxxxxxxxxxxxx" \
--name mediquery_app \
mediquery
```

Then open:http://localhost:8080

---

## 🚀 AWS Deployment Overview (EC2 + Docker + GitHub Actions)

1. **Login to AWS Console**  
   Go to [https://aws.amazon.com](https://aws.amazon.com) and sign in.

2. **Create an IAM user for deployment**  
   - Attach policies:
     - `AmazonEC2ContainerRegistryFullAccess`  
     - `AmazonEC2FullAccess`  
   - Save the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

3. **Create an ECR repository**

   Example (replace with your account and region):

   ```text
   315865595366.dkr.ecr.us-east-1.amazonaws.com/medicalbot
   ```

4. **Launch an EC2 instance (Ubuntu)**

   - Choose an Ubuntu AMI (e.g., `ubuntu/focal`).
   - Attach a key pair and security group allowing port `8080`.

5. **Install Docker on EC2**

   ```bash
   sudo apt-get update -y
   sudo apt-get upgrade -y

   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   newgrp docker
   ```

6. **Configure EC2 as a self‑hosted GitHub Actions runner**

   - In GitHub: Settings → Actions → Runners → New self‑hosted runner.
   - Choose Linux and run the provided commands on your EC2 machine.

7. **Add GitHub Secrets**

   In your repo: Settings → Secrets and variables → Actions.

   Add:

   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_DEFAULT_REGION` (e.g., `eu-north-1`)
   - `ECR_REPO` (e.g., `577435557871.dkr.ecr.eu-north-1.amazonaws.com/medical_chatbot`)
   - `PINECONE_API_KEY`
   - `OPENAI_API_KEY`
   - `GROQ_API_KEY`

Once GitHub Actions runs, it will:

- Build and push the Docker image to ECR.  
- Deploy it to EC2 via `docker pull` and `docker run`.  
- Expose the app on port `8080`.


