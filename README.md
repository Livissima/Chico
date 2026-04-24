# Chico

Utilitário de automação para atividades administrativas do cotidiano escolar em Goiás.

Desenvolvido para secretárias e auxiliares de escolas estaduais que trabalham com os sistemas **SIGE** e **SIAP** da Secretaria de Estado da Educação de Goiás.

Este projeto nasce de uma iniciativa individual para otimizar fluxos de trabalho na rotina administrativa escolar. 
Ele busca mitigar limitações técnicas e gargalos operacionais dos sistemas legados do Estado, oferecendo 
soluções de automação que priorizam a agilidade e a integridade dos dados no atendimento à comunidade escolar.

---

## O que o Chico faz:

- **Download de dados de estudantes** — fichas, contatos, situações, gêneros e fotos via SIGE
- **Consulta e exportação** — gera uma planilha `Database.xlsx` consolidada com dados de todos os estudantes da escola
- **Frequência automatizada** — lança faltas no SIAP a partir de um compilado de ausências, tanto por perfil administrativo quanto por perfil de professor
- **Credenciais** — automatiza o primeiro acesso de estudantes no NetEscola e no e-mail institucional
- **Sondagem** — coleta o resumo de turmas ativas, capacidade e efetivados diretamente do SIGE
- **Estatísticas** — exibe os dados consolidados da escola na interface

---

## Pré-requisitos:

> O setup é manual. É esperado que a pessoa que instalar o Chico tenha familiaridade básica com Python e linha de comando.

- Python 3.12+
- Microsoft Edge instalado (instalado por padrão em qualquer computador com Windows 10/11)
- ChromeDriver compatível com a versão do Chrome instalada
- Acesso ao SIGE e ao SIAP com credenciais válidas
- Windows (o projeto usa caminhos e variáveis de ambiente do Windows)
- Conta com acesso ao OneDrive for Business (para o diretório padrão de dados)

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


> U''se o `pyproject.toml`:
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

## Aviso

O Chico automatiza interações com sistemas da SEDUC-GO (SIGE e SIAP). Seu funcionamento depende da estrutura atual desses sistemas — mudanças nos portais podem exigir atualização dos seletores e XPaths.

Credenciais nunca devem ser commitadas. O arquivo `.env` está no `.gitignore`.

---

## Licença

Uso livre para fins não comerciais — veja [LICENSE](LICENSE).
