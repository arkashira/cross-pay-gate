# TECH_SPEC.md – cross-pay-gate

---

## 1. Overview

**cross‑pay‑gate** is a blockchain‑based cross‑border payment platform that delivers:

| Feature | Description |
|---------|-------------|
| **Fast** | Settlement in < 5 s on Layer‑2 chains |
| **Low‑cost** | < 0.1 % fee, optimized gas usage |
| **Transparent** | Immutable audit trail on public ledger |
| **Interoperable** | Supports ERC‑20, ERC‑777, ERC‑1155, and native fiat‑on‑chain bridges |
| **Regulatory‑ready** | KYC/AML workflow, audit logs, and compliance APIs |

The system is built for banks, payment providers, corporations, and digital asset exchanges to move value across borders with minimal friction.

---

## 2. Architecture Overview

```
┌───────────────────────┐
│  Front‑end (React/TS) │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  API Gateway (FastAPI)│
│  - Auth, Rate‑limit   │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  Service Layer (Go)   │
│  ├─ Payment Orchestrator│
│  ├─ Bridge Manager      │
│  ├─ Compliance Engine   │
│  └─ Settlement Engine   │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  Blockchain Layer     │
│  ├─ Smart Contracts   │
│  │   - ERC‑20 Bridge  │
│  │   - ERC‑777 Bridge │
│  │   - ERC‑1155 Bridge│
│  └─ Event Listener    │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  Data Layer           │
│  ├─ PostgreSQL (pgvector)  │
│  ├─ Redis (cache, pub/sub)│
│  └─ Kafka (event bus)      │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  External Services    │
│  ├─ KYC/AML API       │
│  ├─ Fiat‑on‑chain bridge│
│  └─ Notification (SMTP/FCM)│
└───────────────────────┘
```

### Key Flow

1. **Initiation** – User submits payment via UI → API Gateway → Payment Orchestrator.
2. **Validation** – Compliance Engine checks KYC/AML, transaction limits.
3. **Bridge Selection** – Bridge Manager chooses optimal chain & bridge.
4. **Execution** – Settlement Engine builds transaction, signs, and submits to smart contract.
5. **Confirmation** – Event Listener captures on‑chain events → updates DB.
6. **Settlement** – Funds released to recipient, audit log persisted.

---

## 3. Components & Interfaces

| Component | Language | Key APIs / Interfaces | Notes |
|-----------|----------|-----------------------|-------|
| **API Gateway** | Python (FastAPI) | `/v1/payments`, `/v1/bridges`, `/v1/health` | JWT auth, OpenAPI docs |
| **Payment Orchestrator** | Go | `OrchestratePayment(ctx, req)` | Orchestrates entire payment lifecycle |
| **Bridge Manager** | Go | `SelectBridge(ctx, req) -> BridgeConfig` | Supports multiple L2 chains |
| **Compliance Engine** | Go | `Validate(ctx, req) -> ValidationResult` | Integrates with external KYC/AML |
| **Settlement Engine** | Go | `Execute(ctx, txData) -> TxHash` | Builds and signs transactions |
| **Smart Contracts** | Solidity | `BridgeERC20`, `BridgeERC777`, `BridgeERC1155` | Deployed on Ethereum, Polygon, Arbitrum |
| **Event Listener** | Go | `OnEvent(ctx, event)` | Listens to contract events via WebSocket |
| **Data Layer** | PostgreSQL + pgvector | `payments`, `bridges`, `audit_logs` tables | `pgvector` for embedding compliance rules |
| **Cache** | Redis | `GetBridgeConfig`, `SetBridgeConfig` | Cache bridge selection |
| **Event Bus** | Kafka | Topics: `payments`, `compliance`, `settlement` | Decouples services |
| **External Services** | REST | KYC/AML, Fiat‑on‑chain, Notification | Auth via API keys |

---

## 4. Data Model

### 4.1 `payments` Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique payment ID |
| `sender_id` | UUID | FK → `users.id` | Initiator |
| `recipient_id` | UUID | FK → `users.id` | Beneficiary |
| `amount` | NUMERIC(20,8) | NOT NULL | Amount in source currency |
| `currency` | VARCHAR(3) | NOT NULL | ISO 4217 |
| `destination_chain` | VARCHAR(32) | NOT NULL | e.g., `polygon`, `arbitrum` |
| `status` | VARCHAR(16) | NOT NULL | `pending`, `validated`, `submitted`, `confirmed`, `failed` |
| `tx_hash` | VARCHAR(66) | NULL | On‑chain transaction hash |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | NOT NULL | |

### 4.2 `bridges` Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | |
| `chain_name` | VARCHAR(32) | NOT NULL | |
| `contract_address` | VARCHAR(42) | NOT NULL | |
| `token_type` | VARCHAR(16) | NOT NULL | `ERC20`, `ERC777`, `ERC1155` |
| `gas_estimate` | NUMERIC(20,8) | NOT NULL | |
| `fee_percent` | NUMERIC(5,4) | NOT NULL | |

### 4.3 `audit_logs` Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | |
| `payment_id` | UUID | FK → `payments.id` | |
| `event` | VARCHAR(64) | NOT NULL | e.g., `initiated`, `validated`, `submitted` |
| `details` | JSONB | NOT NULL | |
| `created_at` | TIMESTAMP | NOT NULL | |

---

## 5. Key APIs

### 5.1 `/v1/payments` (POST)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sender_id` | UUID | ✔ | |
| `recipient_id` | UUID | ✔ | |
| `amount` | decimal | ✔ | |
| `currency` | string | ✔ | ISO 4217 |
| `destination_chain` | string | ✔ | |
| `token_type` | string | ✔ | `ERC20`, `ERC777`, `ERC1155` |

**Response**

```json
{
  "payment_id": "uuid",
  "status": "pending",
  "created_at": "2026-06-19T12:34:56Z"
}
```

### 5.2 `/v1/bridges` (GET)

Returns list of available bridges with gas estimates.

### 5.3 `/v1/health` (GET)

Health check for all services.

---

## 6. Tech Stack

| Layer | Technology | Reason |
|-------|------------|--------|
| **Front‑end** | React + TypeScript, Vite | Modern UI, fast dev |
| **API Gateway** | FastAPI (Python 3.12) | Async, OpenAPI, JWT |
| **Services** | Go 1.22 | Performance, concurrency |
| **Smart Contracts** | Solidity 0.8.20 | Security, EVM compatibility |
| **Database** | PostgreSQL 16 + pgvector | Relational + vector search |
| **Cache** | Redis 7 | Low‑latency config |
| **Event Bus** | Kafka 3.7 | Decoupled microservices |
| **Orchestration** | Temporal (Go SDK) | Durable workflows |
| **CI/CD** | GitHub Actions | Automated tests, lint, build |
| **Containerization** | Docker + Docker‑Compose | Consistent dev & prod |
| **Deployment** | Kubernetes (EKS) | Autoscaling, resilience |
| **Monitoring** | Prometheus + Grafana | Metrics, alerts |
| **Tracing** | OpenTelemetry | Distributed tracing |
| **Security** | Vault (HashiCorp) | Secrets management |

---

## 7. Dependencies

| Category | Package | Version | Notes |
|----------|---------|---------|-------|
| **Go** | `github.com/temporalio/sdk-go` | 1.8.0 | Workflow engine |
|          | `github.com/redis/go-redis/v9` | 9.5.0 | Redis client |
|          | `github.com/segmentio/kafka-go` | 0.4.32 | Kafka client |
|          | `github.com/jackc/pgx/v5` | 5.0.0 | PostgreSQL driver |
| **Python** | `fastapi` | 0.111.0 | API framework |
|            | `uvicorn` | 0.30.0 | ASGI server |
|            | `pydantic` | 2.8.2 | Data validation |
| **Solidity** | `forge` | 1.8.0 | Hardhat alternative |
| **Docker** | `docker` | 24.0.6 | Build & run |
| **K8s** | `helm` | 3.12.0 | Charts |

---

## 8. Deployment

### 8.1 Development

```bash
docker compose up -d
```

- API Gateway: `http://localhost:8000`
- Front‑end: `http://localhost:5173`

### 8.2 Production

1. **Build images**

```bash
docker build -t cross-pay-gate/api:latest ./api
docker build -t cross-pay-gate/frontend:latest ./frontend
```

2. **Push to registry**

```bash
docker push registry.example.com/cross-pay-gate/api:latest
docker push registry.example.com/cross-pay-gate/frontend:latest
```

3. **Deploy Helm chart**

```bash
helm upgrade --install cross-pay-gate ./charts/cross-pay-gate \
  --set image.repository=registry.example.com/cross-pay-gate \
  --set image.tag=latest \
  --namespace cross-pay-gate
```

4. **Configure secrets**

- Store DB credentials, API keys, and private keys in Vault.
- Mount Vault secrets into pods via CSI driver.

5. **Ingress**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: cross-pay-gate
  annotations:
    kubernetes.io/ingress.class: nginx
spec:
  rules:
  - host: payments.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
```

### 8.3 Scaling

- **API Gateway**: Horizontal Pod Autoscaler (CPU > 70%)
- **Services**: Temporal workers scale based on task queue depth
- **Database**: Read replicas for analytics; write scaling via sharding if needed
- **Kafka**: 3 brokers with replication factor 3

---

## 9. Security & Compliance

| Area | Implementation |
|------|----------------|
| **Auth** | JWT with RSA‑2048, short expiry, refresh tokens |
| **Data** | TLS everywhere, encryption at rest (PostgreSQL pgcrypto) |
| **KYC/AML** | External API integration, audit logs |
| **Audit** | Immutable audit_logs table, signed hashes |
| **Secrets** | Vault + Kubernetes SecretsProvider |
| **Regulatory** | GDPR, PSD2, AML/KYC compliance modules |

---

## 10. Testing Strategy

| Layer | Tool | Coverage |
|-------|------|----------|
| **Unit** | Go `testing`, Python `pytest` | 80%+ |
| **Integration** | Temporal test suite, Hardhat | 70%+ |
| **Contract** | Foundry, Truffle | 90%+ |
| **E2E** | Cypress (React) | 60%+ |
| **Security** | MythX, Slither | Continuous |

---

## 11. Roadmap (Quarterly)

| Quarter | Milestone |
|---------|-----------|
| Q3 2026 | MVP launch (ERC‑20 bridge, API, UI) |
| Q4 2026 | ERC‑777 & ERC‑1155 support |
| Q1 2027 | Fiat‑on‑chain bridge, KYC/AML integration |
| Q2 2027 | Multi‑chain routing, dynamic fee model |
| Q3 2027 | Enterprise SDK, analytics dashboard |

---

## 12. Appendix

### 12.1 Smart Contract Addresses (Testnet)

| Chain | ERC‑20 Bridge | ERC‑777 Bridge | ERC‑1155 Bridge |
|-------|---------------|----------------|-----------------|
| Polygon | 0xABC... | 0xDEF... | 0x123... |
| Arbitrum | 0x456... | 0x789... | 0x0AB... |

### 12.2 Environment Variables

```env
# API
JWT_SECRET=...
DB_URL=postgres://...
REDIS_URL=redis://...
KAFKA_BROKERS=broker1:9092,broker2:9092
# External
KYC_API_KEY=...
FIAT_BRIDGE_URL=https://fiat.example.com
```

---
