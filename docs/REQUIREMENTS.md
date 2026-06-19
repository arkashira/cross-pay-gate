# REQUIREMENTS.md

## Project Overview
**Project Name:** cross-pay-gate  
**Repository:** `arkashira/cross-pay-gate`  
**Description:** A blockchain‑based cross‑border payment platform that delivers fast, low‑cost, and transparent transactions for banks, payment providers, corporations, and digital asset exchanges.

The platform will expose a set of APIs, a web dashboard, and a mobile SDK, enabling participants to initiate, track, and settle cross‑border payments using a permissioned blockchain backbone.

---

## 1. Functional Requirements

| ID | Description | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| **FR‑1** | **User Onboarding** | P1 | • New participants (banks, exchanges, corporates) can register via a web form. <br>• Identity is verified through KYC/AML checks (integration with external provider). <br>• Upon success, a unique wallet address is provisioned. |
| **FR‑2** | **Payment Initiation** | P1 | • Users can create a payment request specifying amount, currency, destination, and optional memo. <br>• System validates currency pair, compliance rules, and available balance. <br>• Payment is signed by the sender’s private key and submitted to the blockchain. |
| **FR‑3** | **Payment Status Tracking** | P1 | • Users can query status (Pending, Confirmed, Failed, Reversed). <br>• Real‑time updates via WebSocket or polling. |
| **FR‑4** | **Settlement Engine** | P1 | • On confirmation, funds are moved to the recipient’s wallet. <br>• Settlement fee is deducted automatically. |
| **FR‑5** | **Fee Calculation** | P2 | • Fees are calculated based on amount, currency pair, and participant tier. <br>• Fee schedule is configurable via admin panel. |
| **FR‑6** | **Audit Trail** | P1 | • Every transaction is logged immutably on the blockchain. <br>• Logs are exportable in CSV/JSON for compliance. |
| **FR‑7** | **Compliance & AML** | P2 | • Transactions over threshold trigger automated AML checks. <br>• Suspicious activity is flagged and routed to compliance team. |
| **FR‑8** | **Admin Dashboard** | P2 | • View all transactions, participants, fee structures. <br>• Manage participant status (active, suspended). |
| **FR‑9** | **API Gateway** | P1 | • RESTful endpoints for all core functionalities. <br>• Rate limiting (100 req/s per IP). |
| **FR‑10** | **Mobile SDK** | P3 | • iOS/Android SDK exposing payment initiation and status APIs. <br>• SDK handles secure key storage (iOS Keychain, Android Keystore). |
| **FR‑11** | **Multi‑Chain Support** | P3 | • Ability to route payments via multiple underlying blockchains (e.g., Ethereum, Polygon) based on cost/latency. |
| **FR‑12** | **Notification Service** | P2 | • Email/SMS/Push notifications on payment status changes. |
| **FR‑13** | **Currency Conversion** | P2 | • Real‑time FX rates fetched from a licensed provider; conversion applied during payment. |
| **FR‑14** | **Retry Logic** | P2 | • Automatic retry of failed blockchain confirmations up to 3 times with exponential back‑off. |
| **FR‑15** | **Rollback & Reversal** | P2 | • Authorized users can reverse a transaction within 24h if not yet settled. |

---

## 2. Non‑Functional Requirements

| ID | Requirement | Details |
|----|-------------|---------|
| **NFR‑1** | **Performance** | • 99.9% uptime. <br>• Average payment initiation latency < 2 s (excluding blockchain confirmation). <br>• Blockchain confirmation time ≤ 15 s (target). |
| **NFR‑2** | **Scalability** | • Handle 10k concurrent users and 5k tx/s. <br>• Horizontal scaling via Kubernetes. |
| **NFR‑3** | **Security** | • TLS 1.3 for all network traffic. <br>• End‑to‑end encryption of private keys. <br>• OWASP Top‑10 mitigations. <br>• Regular penetration testing. |
| **NFR‑4** | **Compliance** | • GDPR, CCPA, PCI‑DSS compliant. <br>• Data residency per jurisdiction. |
| **NFR‑5** | **Reliability** | • 99.9% SLA. <br>• Automated failover for critical services. |
| **NFR‑6** | **Observability** | • Centralized logging (ELK). <br>• Metrics via Prometheus + Grafana. <br>• Alerting for SLA breaches. |
| **NFR‑7** | **Maintainability** | • Codebase follows Go best practices. <br>• CI/CD pipeline with unit/integration tests (≥80% coverage). |
| **NFR‑8** | **Internationalization** | • UI supports at least 5 locales (en, es, fr, zh, ar). |
| **NFR‑9** | **Documentation** | • Public API docs (OpenAPI). <br>• Developer guide for SDKs. |

---

## 3. Constraints

| ID | Constraint | Impact |
|----|------------|--------|
| **C‑1** | **Blockchain Choice** | Must use a permissioned blockchain (e.g., Hyperledger Fabric) to satisfy regulatory requirements. |
| **C‑2** | **Data Licensing** | All datasets used for FX rates and AML rules must be licensed for commercial use. |
| **C‑3** | **Infrastructure** | Must run on AWS GovCloud for U.S. participants; Azure for EU. |
| **C‑4** | **Open‑Source Dependencies** | Only MIT/Apache‑2.0 licensed libraries may be used. |
| **C‑5** | **Regulatory Review** | Must obtain regulatory approval before live deployment in each jurisdiction. |

---

## 4. Assumptions

| ID | Assumption | Rationale |
|----|------------|-----------|
| **A‑1** | Participants will provide valid cryptographic keys. | Core to blockchain security. |
| **A‑2** | External KYC/AML provider will expose REST APIs. | Enables automated onboarding. |
| **A‑3** | FX rate provider offers a free tier with 1‑minute refresh. | Keeps cost low during MVP. |
| **A‑4** | Users will have internet connectivity with ≥ 1 Mbps. | Required for real‑time status updates. |
| **A‑5** | The platform will initially support USD, EUR, GBP, JPY, and CNY. | Focus on major currencies for MVP. |

---

## 5. Deliverables

1. **API Specification** – OpenAPI v3.0.  
2. **Admin Dashboard** – React SPA with role‑based access.  
3. **Mobile SDKs** – iOS (Swift) & Android (Kotlin).  
4. **Compliance Package** – KYC/AML integration, audit logs.  
5. **Deployment Scripts** – Helm charts for Kubernetes.  
6. **Documentation** – User guide, developer docs, API reference.  

---

## 6. Acceptance Checklist

- [ ] All functional requirements implemented and unit‑tested.  
- [ ] End‑to‑end integration tests covering payment flow.  
- [ ] Security audit passed (OWASP, penetration test).  
- [ ] Performance benchmark meets latency targets.  
- [ ] Documentation fully published.  
- [ ] Deployment pipeline operational.  

---
