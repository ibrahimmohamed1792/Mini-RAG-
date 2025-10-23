# 🧠 Mini-RAG Project

This repository contains the early setup for the **Mini-RAG** project.  
We’re currently setting up the development environment and base configuration before moving on to implementation.

---

## ⚙️ Development Environment

- **Python**: 3.14  
- **Environment Manager**: [Miniconda](https://docs.conda.io/en/latest/miniconda.html)  
- **Platform**: Ubuntu via Windows Subsystem for Linux (WSL)

---

## 🧩 Step 1 — Install WSL

If you’re on Windows, open PowerShell **as Administrator** and run:
```
wsl --install
```
Restart your computer when prompted, then open Ubuntu from the Start menu and set your username and password.

---

## 🐍 Step 2 — Install Miniconda

Download Miniconda for Linux from the official page:  
👉 https://docs.conda.io/en/latest/miniconda.html

Then run:
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  
bash Miniconda3-latest-Linux-x86_64.sh  
source ~/.bashrc
```
---

## 🧱 Step 3 — Create the Project Environment

Inside Ubuntu (WSL):
```
conda create -n mini-rag python=3.14  
conda activate mini-rag
```
---




## 🧑‍💻 Author
Ibrahim Mohamed  
Project Lead — Mini-RAG
