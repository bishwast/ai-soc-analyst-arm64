# Project Design Document (PDD)

**Project Name:** Autonomous SOC Analyst (Agentic AI)
**Version:** 1.0
**Status:** Draft/Initiation
**Architecture:** ARM64 (NVIDIA Jetson/DGX)

---

## 1. Executive Summary
This project aims to reduce the **"Mean Time to Respond" (MTTR)** for security incidents by automating the Tier 1 analysis of SOC alerts.

By integrating an **Open-Source SIEM (Wazuh)** with a local **Large Language Model (Ollama/Llama 3)**, we are building an "Agentic AI" capable of ingesting security logs, interpreting attack context, and generating human-readable incident reports without manual intervention.

The system is architected to run entirely **on-premise (Edge AI)** using **NVIDIA ARM64** hardware, ensuring complete data privacy and zero cloud costs.

---

## 2. Requirements Analysis

### 2.1 Problem Statement
* **Current Challenge:** Security Operations Centers (SOCs) face "Alert Fatigue" due to the overwhelming volume of daily alerts. Human analysts cannot feasibly review every "Low" or "Medium" priority event, leading to potential missed threats.
* **Deficiency in Existing Solutions:** Traditional SOAR (Security Orchestration, Automation, and Response) tools rely on brittle, hard-coded playbooks. If an attack vector shifts slightly, these static playbooks often fail.

### 2.2 Business Objectives
* **Automate Triage:** Achieve 100% analysis coverage for incoming alerts, extending beyond just High-priority events.
* **Data Privacy:** Guarantee that sensitive log data remains local and is never transmitted to external APIs like OpenAI.
* **Cost Efficiency:** Leverage existing NVIDIA DGX hardware to avoid recurring API subscription costs.

### 2.3 Core Functional Capabilities
* **Ingestion:** The system must pull alerts directly from the Wazuh Manager API in real-time.
* **Analysis:** Alert JSON data must be processed by a local LLM (Llama 3.2 or Mistral).
* **Reasoning:** The Agent must evaluate alert severity based on contextual nuance, rather than relying solely on static rule levels.
* **Reporting:** Output must be a structured "Analyst Report" featuring a summary, calculated risk score, and remediation steps.

### 2.4 Technical Constraints
* **Architecture:** The entire stack must support the **ARM64 (aarch64)** instruction set.
* **Performance:** AI inference latency must be maintained under **30 seconds per alert**.
* **Stability:** The host kernel must be tuned (`vm.max_map_count=262144`) to support the memory mapping requirements of the Wazuh Indexer.

---

## 3. System Architecture

### 3.1 High-Level Design
The solution utilizes a "Triad" architecture, fully containerized via Docker to ensure stability on the ARM64 platform.

1.  **The Sensor (Wazuh Agent):** Deployed on the endpoint (DGX Host) to monitor system calls, SSH logs, and file integrity. It forwards raw telemetry to the Manager.
2.  **The Brain (Wazuh Manager):** Correlates incoming logs and triggers specific "Alerts" (JSON) based on detection rules.
3.  **The Analyst (Python Middleware):** A custom service that polls the API, formats the data into a prompt, and queries the AI model.
4.  **The Intelligence (Ollama):** A GPU-accelerated Docker container hosting the Llama 3 model for text generation.

### 3.2 Data Flow
`[Endpoint Event]` -> `[Wazuh Manager]` -> `(API Fetch)` -> `[Python Middleware]` -> `(Prompt)` -> `[Ollama LLM]` -> `[Final Report]`

---

## 4. Technology Stack

### Hardware
* **Choice:** NVIDIA DGX Spark
* **Justification:** ARM64 Architecture. The Unified Memory (RAM+VRAM) architecture allows larger LLMs to run more efficiently than on standard consumer PCs.

### SIEM
* **Choice:** Wazuh (Docker)
* **Justification:** Open-Source standard. It is free and offers official support for `aarch64` containers.

### AI Engine
* **Choice:** Ollama
* **Justification:** Optimized for Apple Silicon and **NVIDIA Jetson/DGX (ARM)**. It handles GPU offloading automatically.

### Model
* **Choice:** Llama 3.2 (3B)
* **Justification:** A "**Small Language Model**" optimized for edge devices. It provides sufficient reasoning speed without exhausting system RAM.

### Language
* **Choice:** Python 3.10+
* **Justification:** Provides native library support for both the Wazuh API (`requests`) and AI orchestration (`langchain`/`crewai`).

---

## 5. Project Roadmap

**Stage 1: Infrastructure Provisioning (In Progress)**
* **Goal:** Establish the Docker runtime, network layers, and persistent storage volumes.

**Stage 2: SIEM Deployment**
* **Goal:** Configure the Wazuh Manager and deploy the Agent to the host for initial log collection.

**Stage 3: Intelligence Integration**
* **Goal:** Develop the Python middleware to bridge the SIEM alerts with the Ollama inference engine.

**Stage 4: Validation & Testing**
* **Goal:** Execute live-fire simulations (e.g., SSH Bruteforce) to validate end-to-end detection and reporting capabilities.