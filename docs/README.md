# 🛡️ AI-SOC Analyst: Automated Threat Intelligence on ARM64

## 🌟 Project Overview
This project demonstrates a next-generation, privacy-first **Security Operations Center (SOC)** deployed natively on **NVIDIA DGX Spark** hardware. By combining the **Wazuh SIEM stack** with a local **Llama 3.2 LLM**, this system automates Tier-1 alert analysis without the costs or privacy risks of cloud-based AI.

## 📁 Project Documentation & Workflow
The project is divided into three distinct phases. Access the detailed technical logs below:

### **Part 1: Project Definition**
* **[Requirement_Gathering.md](./Requirement_Gathering.md)**: Defines the project scope, hardware constraints, and Non-Functional Requirements (NFRs) for data sovereignty and zero-cost AI.

### **Part 2: Infrastructure & Deployment**
* **[Infrastructure_Setup.md](./Infrastructure_Setup.md)**: Documentation of the native AARCH64 installation, including deep-dive troubleshooting for GPG key restoration and DPKG database repairs.
* **[Native Installation Report (PDF)](./reports/Native_Wazuh_Report.pdf)**: Comprehensive visual evidence, terminal logs, and system health verification screenshots.

### * [Agent_Enrollment.md](./Agent_Enrollment.md): Self monitoring verification using Wazuh built-in agent (ID 000) in DGX Spark.

### * [Threat_Detection_Lab.md](./Threat_Detection_Lab.md): Log of the Hydra SSH brute-force simulation and Wazuh rule verification.



### **Part 3: AI Integration (Work in Progress)**
* **Upcoming**: Python middleware to poll the Wazuh API and generate automated incident summaries using **Ollama**.

---

## 💻 Tech Stack
* **SIEM**: Wazuh 4.12.0 (Indexer, Manager, Dashboard)
* **Hardware**: NVIDIA DGX Spark (ARM64 / AARCH64)
* **AI Engine**: Ollama running Llama 3.2 (3B)
* **Language**: Python (for API integration)

## 🎯 Key Differentiators
* **Zero-Cost**: No per-token costs for log analysis.
* **Data Sovereignty**: 100% on-premise; security logs never leave the local network.
* **Native Performance**: Optimized for ARM64 unified memory, bypassing Docker emulation overhead.

---
*Created as part of the AI-SOC Analyst Portfolio.*
