# 🛡️ Infrastructure Setup: Native Wazuh SIEM on DGX Spark

## 🚀 Deployment Overview
This document logs the technical implementation of the **Wazuh 4.12.0** central stack on **NVIDIA DGX Spark (ARM64)**. The project successfully migrated from a failing Docker-emulated environment to a high-performance native AARCH64 installation.

## 💻 Hardware Environment
* **Platform**: NVIDIA DGX Spark (AARCH64)
* **OS**: Ubuntu 24.04 (Noble Numbat)
* **Optimization**: Unified Memory architecture utilized for high-throughput log indexing.



## 🛠️ Phase 1: Critical Troubleshooting Wins
Due to the non-standard hardware architecture, three major technical "hard-blocks" were identified and resolved. **Full visual evidence and terminal captures are linked in the PDF below.**

📄 **[View Full Native Installation Report (PDF)](./reports/Native_Wazuh_Report.pdf)**

### **1. GPG Repository Restoration**
* **The Situation**: Expired NVIDIA AI Workbench keys (Expired Dec 2025) prevented system updates.
* **The Action**: Manually imported fresh GPG keys into `/usr/share/keyrings/` and updated the `apt` sources list to use the `signed-by` parameter.
* **Result**: Restored system chain of trust and repository connectivity.

### **2. DPKG Database Surgery**
* **The Situation**: Failed installation attempts left corrupted post-install metadata, causing `Exit Status 127`.
* **The Action**: Purged poisoned script files in `/var/lib/dpkg/info/wazuh-*` and forced a system-wide reconfiguration.
* **Result**: Cleaned the package manager state, allowing the native Wazuh stack to install correctly.

### **3. API Authorization & JWT Handshake**
* **The Situation**: Credential drift between the Manager and Indexer caused persistent `401 Unauthorized` errors.
* **The Action**: Synchronized the cluster credentials using `wazuh-passwords-tool.sh` and implemented a sanitized JWT Bearer Token handshake.
* **Result**: Programmatic verification of the Manager API success (Status 200).

## 📊 Service Matrix
| Service | Status | Port | Verification |
| :--- | :--- | :--- | :--- |
| **Wazuh Indexer** | ✅ Active | 9200 | `systemctl status wazuh-indexer` |
| **Wazuh Manager** | ✅ Active | 55000 | `curl /manager/info` |
| **Wazuh Dashboard**| ✅ Active | 443 | Web UI Access Verified |

## 📂 Related Documentation
* **Requirements Phase**: [Requirement_Gathering.md](./Requirement_Gathering.md)
* **Proof of Life Screenshots**: Archived in [reports/Native_Wazuh_Report.pdf](./reports/Native_Wazuh_Report.pdf)

---
*Last Updated: 2025-12-20 | Project Phase: 1 (Infrastructure Complete)*
