# 🦮 Sistema de Cadastro de Usuários, Cães-Guia e Candidatos

## 📌 Sobre o Projeto (Português)
Este projeto é um protótipo desenvolvido com **Django** e **PostgreSQL** para gerenciar:
- Usuários do sistema
- Cães-guia em treinamento
- Candidatos a receber um cão-guia
- Formação de dupla entre cão e candidato

O sistema permite cadastrar, listar e gerenciar os dados de forma prática, integrando a interface web com o banco de dados.

### 🗂 Estrutura do Banco de Dados
- **USUÁRIOS**: informações básicas de acesso.
- **CÃES_GUIAS**: dados de identificação e treinamento dos cães.
- **CANDIDATOS**: informações pessoais e status de aptidão (Apto/Inapto).
- **FORMAÇÃO_DUPLA**: relação entre cães e candidatos, com datas de início e fim.

### 🚀 Tecnologias Utilizadas
- **Python** + **Django**
- **PostgreSQL**
- **HTML/CSS** para interface
- **Bootstrap** (opcional) para estilo

### ▶️ Como Executar o Projeto
1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```
2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure o banco no `settings.py`.
5. Execute as migrações e inicie o servidor:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## 🦮 Guide Dog User and Candidate Registration System

## 📌 About the Project (English)
This project is a prototype developed with **Django** and **PostgreSQL** to manage:
- System users
- Guide dogs in training
- Candidates to receive a guide dog
- Pair formation between dog and candidate

The system allows registering, listing, and managing data easily, integrating the web interface with the database.

### 🗂 Database Structure
- **USUÁRIOS (Users)**: basic access information.
- **CÃES_GUIAS (Guide Dogs)**: identification and training details.
- **CANDIDATOS (Candidates)**: personal information and aptitude status (Apto/Inapto).
- **FORMAÇÃO_DUPLA (Pairing)**: relationship between dogs and candidates, with start and end dates.

### 🚀 Technologies Used
- **Python** + **Django**
- **PostgreSQL**
- **HTML/CSS** for interface
- **Bootstrap** (optional) for styling

### ▶️ How to Run the Project
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/your-repository.git
   ```
2. Create and activate the virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the database in `settings.py`.
5. Run migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
