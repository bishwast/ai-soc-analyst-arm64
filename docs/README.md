# AI-SOC Analyst: Automated Threat Intelligence on ARM64

##  Project Overview
This project demonstrates a next-generation, privacy-first **Security Operations Center (SOC)** deployed natively on **NVIDIA DGX Spark** hardware. By combining the **Wazuh SIEM stack** with a local **Llama 3.2 LLM**, this system automates Tier-1 alert analysis without the costs or privacy risks of cloud-based AI.

The core of the project is a stateful correlation engine that detects complex behavioral patterns, such as **Credential Stuffing**, and triggers an automated AI summary for immediate executive response.

## Project Documentation & Workflow
The project is divided into three distinct phases. Access the detailed technical logs below:

### **Part 1: Project Definition**
* **[Requirement_Gathering.md](./docs/Requirement_Gathering.md)**: Defines the project scope, hardware constraints, and Non-Functional Requirements (NFRs) for data sovereignty and zero-cost AI.

### **Part 2: Infrastructure & Deployment**
* **[Infrastructure_Setup.md](./docs/Infrastructure_Setup.md)**: Documentation of the native AARCH64 installation, including deep-dive troubleshooting for GPG key restoration and DPKG database repairs.
* **[Native Installation Report (PDF)](./docs/reports/Native_Wazuh_Report.pdf)**: Comprehensive visual evidence, terminal logs, and system health verification screenshots.
* **[Agent_Enrollment.md](./docs/Agent_Enrollment.md)**: Self-monitoring verification using the Wazuh built-in agent (ID 000).

### **Part 3: Detection Engineering & AI Integration**
* **[Threat_Detection_Lab.md](./docs/Threat_Detection_Lab.md)**: Technical deep-dive into the custom PCRE2 decoders and the Tier-2 correlation rules engineered to detect high-frequency Hydra SSH brute-force attacks.
* **[AI SOC Analyst (Python Script)](./src/ai_analyst.py)**: The real-time automation bridge that tails the Wazuh `alerts.json` file and pushes high-severity events to Llama 3.2 via the Ollama API.
* **[Final Incident Evidence](./reports/finale_result.png)**: Visual proof of the end-to-end pipeline: **Attack Simulation -> SIEM Correlation -> AI Summarization**.

---

## Tech Stack
* **SIEM**: Wazuh 4.12.0 (Indexer, Manager, Dashboard)
* **Hardware**: NVIDIA DGX Spark (ARM64 / AARCH64)
* **AI Engine**: Ollama running Llama 3.2 (3B)
* **Language**: Python 3.12 (PEP 668 Virtualized Environment)
* **Attack Tool**: Hydra v9.5

## Key Differentiators
* **Zero-Cost**: No per-token costs for log analysis.
* **Data Sovereignty**: 100% on-premise; security logs never leave the local network.
* **Native Performance**: Optimized for ARM64 unified memory, bypassing Docker emulation overhead.
* **Stateful Intelligence**: Moves beyond simple "failed login" alerts to recognize behavioral patterns.

---
*Created as part of the AI-SOC Analyst Portfolio.*