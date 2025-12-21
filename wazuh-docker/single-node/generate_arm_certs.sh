#!/bin/bash
# Manually generate Wazuh Indexer certificates for ARM64

mkdir -p config/wazuh_indexer_ssl_certs
cd config/wazuh_indexer_ssl_certs

# 1. Create Root CA
openssl genrsa -out root-ca.key 2048
openssl req -x509 -new -nodes -key root-ca.key -sha256 -days 3650 -out root-ca.pem -subj "/C=US/L=California/O=Wazuh/CN=root-ca"

# 2. Create Admin Cert
openssl genrsa -out admin-key.pem 2048
openssl req -new -key admin-key.pem -out admin.csr -subj "/C=US/L=California/O=Wazuh/CN=admin"
openssl x509 -req -in admin.csr -CA root-ca.pem -CAkey root-ca.key -CAcreateserial -out admin.pem -days 3650 -sha256

# 3. Create Indexer Cert (wazuh.indexer)
openssl genrsa -out wazuh.indexer-key.pem 2048
openssl req -new -key wazuh.indexer-key.pem -out wazuh.indexer.csr -subj "/C=US/L=California/O=Wazuh/CN=wazuh.indexer"
echo "subjectAltName=DNS:wazuh.indexer,DNS:localhost" > indexer.ext
openssl x509 -req -in wazuh.indexer.csr -CA root-ca.pem -CAkey root-ca.key -CAcreateserial -out wazuh.indexer.pem -days 3650 -sha256 -extfile indexer.ext

# 4. Create Manager Cert (wazuh.manager)
openssl genrsa -out wazuh.manager-key.pem 2048
openssl req -new -key wazuh.manager-key.pem -out wazuh.manager.csr -subj "/C=US/L=California/O=Wazuh/CN=wazuh.manager"
echo "subjectAltName=DNS:wazuh.manager" > manager.ext
openssl x509 -req -in wazuh.manager.csr -CA root-ca.pem -CAkey root-ca.key -CAcreateserial -out wazuh.manager.pem -days 3650 -sha256 -extfile manager.ext

# 5. Create Dashboard Cert (wazuh.dashboard)
openssl genrsa -out wazuh.dashboard-key.pem 2048
openssl req -new -key wazuh.dashboard-key.pem -out wazuh.dashboard.csr -subj "/C=US/L=California/O=Wazuh/CN=wazuh.dashboard"
echo "subjectAltName=DNS:wazuh.dashboard" > dashboard.ext
openssl x509 -req -in wazuh.dashboard.csr -CA root-ca.pem -CAkey root-ca.key -CAcreateserial -out wazuh.dashboard.pem -days 3650 -sha256 -extfile dashboard.ext

# 6. Cleanup CSRs and ext files
rm *.csr *.ext root-ca.srl

# 7. Set Permissions
chmod 500 *.pem *.key
chmod 400 *key.pem
echo "Success: Certificates generated for ARM64."
