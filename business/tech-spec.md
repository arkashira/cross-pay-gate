# Tech Spec
## Stack
* Language: **Rust**
* Framework: **Actix-web**
* Runtime: **Docker**

## Hosting
* Free-tier-first: **AWS Free Tier**
* Specific platforms: 
  + **AWS Elastic Container Service (ECS)** for container orchestration
  + **AWS Relational Database Service (RDS)** for database management
  + **AWS CloudWatch** for monitoring and logging

## Data Model
### Tables/Collections
* **Users**
	+ id (primary key)
	+ username
	+ email
	+ password (hashed)
* **Transactions**
	+ id (primary key)
	+ user_id (foreign key)
	+ sender_address
	+ recipient_address
	+ amount
	+ currency
	+ status (pending, completed, failed)
* **Payment Methods**
	+ id (primary key)
	+ user_id (foreign key)
	+ payment_method (e.g. bank account, credit card)
	+ payment_method_details (e.g. account number, expiration date)

### Key Fields
* **Transaction ID**: a unique identifier for each transaction
* **User ID**: a unique identifier for each user
* **Payment Method ID**: a unique identifier for each payment method

## API Surface
### Endpoints
1. **POST /users**: create a new user
	* Method: POST
	* Path: /users
	* Purpose: create a new user account
	* Request Body: { username, email, password }
2. **GET /users**: retrieve a list of all users
	* Method: GET
	* Path: /users
	* Purpose: retrieve a list of all users
3. **POST /transactions**: create a new transaction
	* Method: POST
	* Path: /transactions
	* Purpose: create a new transaction
	* Request Body: { user_id, sender_address, recipient_address, amount, currency }
4. **GET /transactions**: retrieve a list of all transactions
	* Method: GET
	* Path: /transactions
	* Purpose: retrieve a list of all transactions
5. **GET /transactions/{transaction_id}**: retrieve a specific transaction
	* Method: GET
	* Path: /transactions/{transaction_id}
	* Purpose: retrieve a specific transaction
6. **POST /payment-methods**: create a new payment method
	* Method: POST
	* Path: /payment-methods
	* Purpose: create a new payment method
	* Request Body: { user_id, payment_method, payment_method_details }
7. **GET /payment-methods**: retrieve a list of all payment methods
	* Method: GET
	* Path: /payment-methods
	* Purpose: retrieve a list of all payment methods
8. **GET /payment-methods/{payment_method_id}**: retrieve a specific payment method
	* Method: GET
	* Path: /payment-methods/{payment_method_id}
	* Purpose: retrieve a specific payment method

## Security Model
* **Authentication**: JSON Web Tokens (JWT) with RSA encryption
* **Authorization**: role-based access control (RBAC) with three roles: admin, user, and guest
* **Secrets Management**: AWS Secrets Manager for storing and retrieving sensitive data
* **IAM**: AWS Identity and Access Management (IAM) for managing access to AWS resources

## Observability
* **Logs**: AWS CloudWatch Logs for logging and monitoring
* **Metrics**: AWS CloudWatch Metrics for monitoring and alerting
* **Traces**: AWS X-Ray for distributed tracing and monitoring

## Build/CI
* **Build Tool**: Cargo (Rust package manager)
* **CI/CD Pipeline**: GitHub Actions for automating build, test, and deployment
* **Testing Framework**: Rust testing framework for unit testing and integration testing
* **Code Quality**: Rustfmt and Clippy for code formatting and linting