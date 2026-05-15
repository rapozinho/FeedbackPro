<<<<<<< HEAD
# FeedbackPro 🌟

**Sistema de Feedback de Clientes** desenvolvido como projeto acadêmico para a disciplina de **Qualidade de Software (QA)**.

O objetivo deste projeto é demonstrar a implementação de um sistema web focado em **código limpo, validações rigorosas e facilidade de teste**, garantindo uma alta qualidade de software (QA) através de requisitos bem definidos e uma arquitetura simples e testável.

## 🎯 Foco em Qualidade (QA)

Este projeto foi desenhado pensando nos princípios de Quality Assurance:
- **Testabilidade:** Ausência de dependências complexas (Docker, serviços externos). Funciona 100% offline com SQLite embutido, facilitando a criação de ambientes de teste.
- **Validação de Dados:** Backend (Python/Flask) implementa validações rigorosas de tipo e intervalo (ex: notas restritas de 1 a 5).
- **Integridade do Banco:** Constraints `CHECK` diretamente no esquema do banco de dados (SQLite) para garantir que dados inválidos não sejam persistidos mesmo se houver falha na aplicação.
- **Prevenção de Erros (Poka-Yoke):** O formulário preserva o preenchimento do usuário em caso de erro, prevenindo frustração e abandono.
- **Feedback Visual Claro:** Mensagens de erro e sucesso são exibidas de forma não ambígua ao usuário.
- **Segurança Básica:** Área administrativa protegida por sessão (login/senha) e prevenção contra injeções SQL através do uso correto de *parameterized queries* nativas do SQLite.

## 🛠️ Tecnologias Utilizadas

O projeto utiliza um stack leve e de fácil execução local, ideal para validações e testes end-to-end (E2E):

- **Backend:** Python 3 + Flask 3.x
- **Banco de Dados:** SQLite (Biblioteca padrão do Python)
- **Frontend:** HTML5 Semântico + CSS3 Puro (Dark Mode, CSS Variables, Flexbox/Grid)
- **Interatividade:** JavaScript mínimo (apenas `IntersectionObserver` para animações de scroll). O componente de *Star Rating* é feito **100% em CSS**.
- **Tipografia:** Google Fonts (Inter)

## ✨ Funcionalidades

### Área Pública (Cliente)
- Formulário intuitivo de envio de feedback.
- Sistema de avaliação por estrelas interativo.
- Campo de comentário opcional.
- Validação visual de campos obrigatórios.

### Área Administrativa (Gestor)
- Login seguro.
- Dashboard completo com estatísticas em tempo real:
  - Total de feedbacks.
  - Média geral de avaliações.
  - Gráfico de barras de distribuição por nota.
- Tabela de listagem de feedbacks com badges visuais.
- Filtro interativo por nota (1 a 5 estrelas).
- Exclusão de registros com alerta de confirmação irreversível.
- **Bônus:** Endpoint de API JSON em `/api/feedbacks` (protegido por autenticação) para facilitar testes de integração.

## 🚀 Como Executar Localmente

**Pré-requisitos:** Python 3.9+ instalado em sua máquina.

1. Clone ou baixe este repositório.
2. Abra o terminal na pasta raiz do projeto (`Trabalho QA`).
3. Instale a única dependência necessária:
   ```bash
   pip install flask
   ```
4. Inicie o servidor web:
   ```bash
   python app.py
   ```
5. Acesse no navegador:
   - **Formulário do Cliente:** [http://127.0.0.1:5000](http://127.0.0.1:5000)
   - **Painel Admin:** [http://127.0.0.1:5000/admin/login](http://127.0.0.1:5000/admin/login)

**Credenciais de Acesso (Admin):**
- Usuário: `admin`
- Senha: `admin123`

*(O banco de dados `feedback.db` será criado automaticamente e populado conforme o uso na primeira execução).*

## 📄 Documentação de Requisitos

A documentação detalhada (Requisitos Funcionais, Não Funcionais, Regras de Negócio, e Diagrama de Rotas/Banco) foi atualizada de acordo com as entregas e está disponível no arquivo PDF gerado em anexo (`Documento de Requisitos v2.0.pdf`).
=======
# FeedbackPro
>>>>>>> 82867a1da7d7004e618ca384af075c64839af5e8
