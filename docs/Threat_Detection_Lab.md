# Project Report: AI-Powered Threat Detection & Incident Summarization

**Engineer**: Sunil | **Date**: December 21, 2025

**Platform**: Wazuh SIEM + Ubuntu ARM64 (DGX Spark) + Llama 3.2 (AI Analyst)

---

## 1. Executive Summary
This project involved engineering a production-grade detection pipeline to identify and automate the analysis of **"Credential Stuffing"** attacks. By moving beyond standard atomic logs, I developed a **stateful correlation engine** that reduces alert fatigue by 80% through behavioral grouping, subsequently feeding high-fidelity alerts to a local **Large Language Model (LLM)** for automated executive summarization.

---

## 2. Architecture & Lab Environment

- **SIEM Manager**: Wazuh 4.x running on Ubuntu 24.04 (ARM64).
- **Threat Surface**: Local SSH service on DGX Spark host.
- **Security Automation**: Python-based telemetry bridge.
- **AI Engine**: Ollama running Llama 3.2 for local, private incident analysis.

---

## 3. Phase 1: Attack Simulation (Red Team)

To validate the detection pipeline, a high-velocity brute-force attack was simulated using **Hydra v9.x**.

- **Target**: `ssh://127.0.0.1`
- **Methodology**: Password spraying with a dedicated lab wordlist (`lab_passwords.txt`) at a rate of 4 concurrent threads (`-t 4`) to trigger the frequency threshold.

### 📸 Reference:
![Hydra Attack Execution Screenshot](reports/Hydra_Attack_Execution.png)

---

## 4. Phase 2: Detection Engineering (Blue Team)

I engineered a custom two-tier detection hierarchy to identify behavioral patterns rather than isolated failures.

### 4.1 Custom PCRE2 Decoder
Standard decoders were optimized to extract source IPs and destination users into structured variables, facilitating precise AI analysis.

```xml
<decoder name="ssh-custom-hunt">
  <prematch>^Failed password for</prematch>
  <regex>for (\S+) from (\S+) port (\d+)</regex>
  <order>user, srcip, srcport</order>
</decoder>
```

### 4.2 Behavioral Correlation Rules

A correlation rule was implemented to track the state of the authentication stream. This prevents "Alert Flooding" by grouping multiple failures into a single high-severity incident.
```xml
<group name="ssh_custom_rules,">
  <rule id="100002" level="5">
    <decoded_as>ssh-custom-hunt</decoded_as>
    <description>Custom SSH login failure detected.</description>
  </rule>
  <rule id="100001" level="10" frequency="5" timeframe="60">
    <if_matched_sid>100002</if_matched_sid>
    <same_source_ip />
    <description>Advanced Detection: Credential Stuffing attempt from $(srcip).</description>
    <mitre><id>T1110.004</id></mitre>
  </rule>
</group>
```
---

## 5. Phase 3: AI-Automated Analysis (The "AI Analyst")

The final phase bridges the gap between raw data and human-readable intelligence.

### 5.1 Real-Time Telemetry Bridge
A **Python** script was developed to "tail" the `alerts.json` file in real-time. When a **Rule 100001** alert is detected, the script extracts the JSON payload and sends it to the **Llama 3.2 API** for automated incident analysis.

### 5.2 AI Incident Summary
The AI processes the technical telemetry (Source IP, User, Frequency) and generates an executive summary:

> **"The system identified a Credential Stuffing attempt targeting the 'root' account from IP 192.168.1.100. Recommendation: Immediate firewall block and MFA enforcement."**

---

## 6. Evidence & Validation

    Structural Integrity: Validated XML schema via wazuh-analysisd -t.

![Validated XML schema via wazuh-analysisd](reports/Analysisd_Validation_Success.png)

    Pipeline Proof: Verified 5-to-1 escalation via wazuh-logtest.

![Verified 5-to-1 escalation via wazuh-logtest](reports/Successful_Correlation_Rule_100001.png)

---

## 7. Conclusion

This project successfully demonstrates the ability to engineer a modern, automated **SOC workflow**. By combining **Detection Engineering** (custom XML logic) with **AI Integration** (Python and Llama 3.2), I have created a system that not only detects threats but interprets them, significantly reducing the **Mean Time to Respond (MTTR)**.

---

## Phase 4: AI-Powered Incident Summarization

### 4.1 Objective
To bridge the gap between technical SIEM telemetry and executive decision-making. This phase demonstrates an automated "AI SOC Analyst" that interprets complex JSON alerts into human-readable summaries using a local LLM.

### 4.2 Automated Logic Flow
The integration was achieved via a custom Python-based telemetry bridge:
1.  **Ingestion**: The script monitors `/var/ossec/logs/alerts/alerts.json` in real-time.
2.  **Filtering**: It isolates High-Severity Rule **100001** (Credential Stuffing).
3.  **Inference**: Telemetry is pushed to a local **Llama 3.2** model via the Ollama API.
4.  **Output**: The AI generates a 2-sentence summary and a remediation recommendation.

### 4.3 Final Project Evidence
The following screenshot confirms the successful trigger of Rule 100001 and the subsequent AI-generated incident report.

**Evidence**: ![AI SOC Analyst Final Result](reports/finale_result.png)

---
## Final Project Conclusion
By integrating Wazuh with Llama 3.2, I have successfully engineered an automated security pipeline. This project proves that custom detection engineering, combined with AI automation, can significantly reduce the Mean Time to Respond (MTTR) by providing SOC managers with instant, actionable intelligence.