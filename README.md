# 🏦 API Bancária Assíncrona

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-async-brightgreen)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

API bancária desenvolvida com **FastAPI**, **SQLAlchemy Core**, **Databases** e **SQLite**, focada em boas práticas de sistemas financeiros, operações assíncronas e consistência de dados.

Este projeto simula operações bancárias reais como:

* Cadastro de clientes
* Criação de contas
* Depósitos e saques
* Registro de transações

Tudo com controle transacional e segurança lógica.

---

## 🚀 Tecnologias Utilizadas

* **Python 3.12+**
* **FastAPI**
* **SQLAlchemy Core**
* **Databases** (async)
* **SQLite**
* **Pydantic v2**
* **Uvicorn**

---

## 📂 Estrutura do Projeto

```
api-bancaria-assincrona/
│
├── clientes/
│   ├── controllers/
│   ├── services/
│   ├── schemas/
│   └── models/
│
├── contas/
│   ├── controllers/
│   ├── services/
│   ├── schemas/
│   └── models/
│
├── transacoes/
│   ├── controllers/
│   ├── services/
│   ├── schemas/
│   └── models/
│
├── controllers/
│   └── auth.py
│
├── schemas/
│   └── auth.py
│
├── database.py
├── main.py
└── README.md
```

---

## ⚙️ Instalação e Execução

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seu-usuario/api-bancaria-assincrona.git
cd api-bancaria-assincrona
```

### 2️⃣ Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Executar a aplicação

```bash
uvicorn main:app --reload
```

---

## 📖 Documentação Automática

Após iniciar o servidor:

* Swagger UI: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

---

## 🧠 Conceitos Importantes do Projeto

### 🔒 Atualização de Saldo Atômica

O saldo **nunca** é calculado fora do banco de dados.

```sql
saldo = saldo + valor
saldo = saldo - valor
```

Evita:

* Race conditions
* Inconsistência de dados

---

### 🔄 Transações Bancárias

Depósitos e saques:

* Atualizam o saldo
* Registram a transação
* Executam tudo dentro de **transaction()**

Se algo falhar → rollback automático.

---

### 📌 Enum para Tipo de Transação

```python
class TipoTransacao(str, Enum):
    DEPOSITO = "deposito"
    SAQUE = "saque"
```

Garante:

* Validação automática
* Código mais seguro
* Menos erros lógicos

---

### 💰 Decimal em Valores Monetários

```python
from decimal import Decimal
```

Nunca usar `float` em sistemas financeiros.

---

## 📬 Exemplos de Endpoints

### Criar Cliente

```http
POST /clientes/
```

### Criar Conta

```http
POST /contas/
```

### Realizar Transação

```http
POST /transacoes/
```

### Listar Transações

```http
GET /transacoes/?limit=100&skip=0
```

---

## ❗ Observações Importantes

* Projeto educacional com foco em **boas práticas reais**
* Estrutura pensada para escalar
* Código organizado por domínio

---

## 🧑‍💻 Autor

Desenvolvido por **José Carlos**
Estudante de Desenvolvimento de Sistemas
Foco em backend, APIs e arquitetura limpa

---

## 📜 Licença

Este projeto está sob a licença MIT.

Sinta-se livre para estudar, modificar e evoluir 🚀
