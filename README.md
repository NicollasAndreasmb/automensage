# Sistema de Aviso de Vencimento de Certificados

Este projeto automatiza o envio de avisos de vencimento de certificados via **WhatsApp** e **E-mail**, registrando os envios em uma planilha de contatos e em um relatório semanal.

---

## Estrutura do Projeto

certificacao/
│
├── data/
│ └── Renovacao.xlsx # Planilha de contatos
│
├── reports/
│ └── weekly_report.xlsx # Relatório de envios
│
├── certificacao/
│ ├── init.py
│ ├── main.py # Script principal
│ ├── config.py # Configurações e variáveis de ambiente
│ ├── storage.py # Funções de leitura e escrita da planilha
│ ├── mensagens.py # Funções de criação de mensagens
│ ├── whatsappCliente.py # Envio de mensagens via WhatsApp
│ ├── emailCliente.py # Envio de mensagens por e-mail
│ └── report.py # Geração e atualização de relatórios
│
├── .env # Configurações sensíveis (login de e-mail, paths etc.)
├── requirements.txt # Dependências do projeto
└── README.md # Este arquivo

markdown


---

## Funcionalidades

1. **Envio via WhatsApp**
   - Utiliza `pywhatkit` para enviar mensagens programadas.
   - Valida números com `phonenumbers`.
   - Caso o WhatsApp falhe, o envio é tentado por e-mail.

2. **Envio via E-mail**
   - Utiliza SMTP configurável (ex: Locaweb, Gmail, Outlook).
   - Funciona como fallback quando o número de telefone está ausente ou inválido.

3. **Mensagens personalizadas**
   - Se houver texto na coluna `Mensagem`, ele é usado.
   - Caso contrário, gera uma mensagem padrão com base nos dados do contato.

4. **Relatórios semanais**
   - Todas as tentativas de envio são registradas no arquivo `reports/weekly_report.xlsx`.
   - Inclui tipo de envio, status, observações e timestamp.

5. **Atualização da planilha de contatos**
   - Marca o status de cada contato: `Enviado (whatsapp)`, `Enviado (e-mail)`, `Pendente`.

---

## Instalação

1. Clone o repositório:

git clone <URL_DO_REPOSITORIO>
cd certificacao
Crie um ambiente virtual e instale as dependências:



python -m venv .venv
source .venv/bin/activate  # Linux / MacOS
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
Configure o .env:

ini
EXCEL_FILE=data/Renovacao.xlsx
DEFAULT_COUNTRY=BR
MINUTES_BETWEEN_MESSAGES=1
WAIT_TIME=10
CLOSE_TIME=3

EMAIL_FROM=seu_email@provedor.com
EMAIL_PASSWORD=sua_senha
EMAIL_SMTP=smtp.provedor.com
EMAIL_PORT=465
Uso
Prepare a planilha Renovacao.xlsx com as colunas:

objectivec

Telefone | Email | Nome_Responsável | Titular | CPF | CNPJ | Mensagem | Status
Execute o script principal:


python -m certificacao.main
Verifique:

WhatsApp Web abrirá automaticamente para envio.

Relatório reports/weekly_report.xlsx será atualizado com todos os envios.

Planilha de contatos terá a coluna Status atualizada.

Dependências
pandas

openpyxl

pywhatkit

phonenumbers

python-dotenv

reportlab (para relatórios avançados se necessário)

Observações
O WhatsApp Web deve estar logado no navegador.

Evite intervalos curtos entre mensagens para não ser bloqueado.

Mensagens sensíveis podem ser enviadas com fallback por e-mail quando o WhatsApp não estiver disponível.

Contato
Nicollas Andreas - nicollasamb@gmail.com

---
