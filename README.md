# Chico

Utilitário de automação para atividades administrativas do cotidiano escolar em Goiás.

Desenvolvido para servidores da educação que trabalham com os sistemas **SIGE** e/ou **SIAP**, de autoriada Secretaria de Estado da Educação de Goiás.

Este projeto nasce de uma iniciativa individual para atender as necessidades percebidas na rotina administrativa escolar. 
Ele busca mitigar limitações técnicas e gargalos operacionais dos sistemas legados do Estado, oferecendo 
soluções de automação, tratamento e análise de dados e navegabilidade.

---

## O que o Chico faz:

- **Download de dados** — download automatizado de dados pessoais e institucionais de estudantes e servidores a partir de diversas fontes dispersas e desorganizadas nos sistemas estaduais
- **Consulta de dados** — compila os dados obtidos em uma base de dados organizada que facilita a visualização e alimenta múltiplas funcionalidades
- **Análise de dados** — tabelas e dashboards de dados pessoais, institucionais, pedagógicos e frequência escolar
- **Gerenciamento de frequência** — gerencia automaticamente a frequência escolar no SIAP a partir dos dados coletados manualmente
- **Gerenciamento de credenciais** — gerencia automaticamente as credenciais NetEscola e @educa dos estudantes

---

## Pré-requisitos:

> O setup é manual. É esperado que a pessoa que instalar o Chico tenha familiaridade básica com Python e linha de comando.

- Windows 10 ou 11
- Python 3.12+
- Microsoft Edge 
- Acesso ao SIGE e ao SIAP com credenciais válidas
- OneDrive (opcional)

---

## Instalação:

**1. Clone o repositório**
```bash
git clone https://github.com/Livissima/Chico.git
cd chico
```

**2. Crie e ative um ambiente virtual**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**3. Instale as dependências**


> Use o `pyproject.toml`:
> ```bash
> pip install .
> ```

**4. Configure as credenciais**

Copie o arquivo de exemplo e preencha com suas credenciais:
```bash
copy .env.example .env
```

Edite o `.env` com suas credenciais do SIGE e do SIAP. O arquivo `.env.example` documenta todos os campos necessários.

**5. Execute**
```bash
python -m app.main
```

---

## Estrutura de diretórios esperada:

O Chico trabalha com uma pasta base (por padrão no OneDrive, configurável na interface). Dentro dela, ele espera e cria a seguinte estrutura:

```
<diretório base>/
├── fonte/
│   ├── Fichas/             ← JSONs baixados pelo bot SIGE
│   ├── Contatos/
│   ├── Situações/
│   ├── Gêneros/
│   ├── Controle de Frequência/
│   │   └── Registro de Faltas/   ← planilhas .xlsx com o registro diário
│   ├── resumo.json
│   └── Database.json
└── Database.xlsx           ← gerado pela Consulta
```

---

## Aviso e considerações:

O Chico automatiza interações com sistemas da SEDUC-GO (SIGE e SIAP). Seu funcionamento depende da estrutura atual 
desses sistemas — mudanças nos portais podem exigir atualização dos seletores e XPaths.

Credenciais nunca devem ser commitadas. O arquivo `.env` está no `.gitignore`, e deve ser preenchido de acordo com o [.env.example](.env.example)


Há várias funcionalidades que ainda estão sendo planejadas e/ou testadas para serem implementadas efetivamente no projeto.
Algumas estão no package [sketches](sketches), outras apenas em minha cabeça. 
É possível e até provável que existam novidades não documentadas neste arquivo.

Os produtos deste programa sustentam uma cadeia de consultas externas em `VBA` e `Excel`, que em algum futuro serão portadas para python. 
Esse esforço se tornou uma prioridade desde Julho de 2026, quando a SEDUC deixou de fornecer assinaturas do Office 365 para seus servidores.

Acompanhe o projeto!!

---

## Licença

Uso livre para fins não comerciais — veja [LICENSE](LICENSE).

___
