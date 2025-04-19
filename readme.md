# 🐾 Blackcat — Framework para Microserviços Python na AWS

O **Blackcat** é um framework open source projetado para acelerar a criação de **microserviços Python**, com foco em produtividade, arquitetura limpa e integração nativa com a **AWS**. Ele oferece um conjunto de ferramentas e estruturas padronizadas para construir serviços robustos com filas (SQS), tópicos (SNS), APIs HTTP e workers, tudo com **Clean Architecture**, **testabilidade** e **boas práticas** desde o início.

# 💥 Dores que o Framework `blackcat` se propõe a resolver

## 🔧 Complexidade na Criação de Microserviços

- Criar a estrutura inicial de um microserviço leva tempo e exige conhecimento profundo de boas práticas.
- Projetos diferentes com estruturas inconsistentes dificultam manutenção e escalabilidade.
- A ausência de um padrão para orquestração de filas, workers e APIs gera retrabalho.

## 🧱 Falta de Arquitetura Sólida

- Muitos projetos começam sem separação clara entre camadas, misturando domínio com infraestrutura.
- Regras de negócio acopladas ao framework dificultam testes e evolução.
- A ausência de Clean Architecture leva a código difícil de manter.

## 📦 Implementação Repetitiva de Adapters AWS

- Repetição de código para uso de boto3 (SQS, SNS, DynamoDB) em cada projeto.
- Tratamento inconsistente de erros e logs em chamadas AWS.
- Dificuldade para mockar essas integrações em testes.

## 🧪 Baixa Testabilidade

- Estruturas acopladas dificultam a criação de testes unitários reais.
- Difícil mockar camadas de infraestrutura sem contratos claros.
- Muitos projetos carecem de cultura e estrutura pronta para testes.

## ⚙️ Dificuldade na Configuração

- Uso disperso e desorganizado de variáveis de ambiente.
- Ausência de validação ou fallback em `.env` dificulta setup local e deploy.
- Inconsistência entre ambientes (dev, staging, prod) causa bugs de configuração.

## 🩺 Ausência de Healthcheck e Observabilidade

- Serviços sem healthcheck impedem boa integração com ECS, Fargate ou K8s.
- Falta de padrão em logs e métricas reduz visibilidade e rastreabilidade.
- Diagnóstico de falhas fica mais lento e difícil.

## 🚀 Lentidão no Time-to-Market

- Equipes perdem tempo com setup básico ao invés de focar em regras de negócio.
- POCs demoram para virar produção por falta de base reutilizável.
- Cada novo serviço exige reaprendizado de padrões e integração com AWS.

## 🧑‍💻 Experiência do Desenvolvedor Inconsistente

- Cada dev aplica padrões diferentes ao construir microserviços.
- Falta de ferramentas de scaffolding padronizadas aumenta tempo de entrega.
- Curva de aprendizado mais íngreme para novos devs em times com múltiplos serviços.

## 🔐 Falta de Segurança Padrão

- Uso incorreto de variáveis sensíveis em logs e código.
- Acesso direto ao boto3 sem abstrações seguras.
- Dificuldade de aplicar boas práticas de IAM e VPC por falta de estrutura comum.


# 👤 Personas do Framework `blackcat`

## 🧑‍💻 Desenvolvedor Backend Python

- Trabalha com microsserviços e precisa entregar com agilidade e qualidade.
- Quer evitar escrever código repetitivo para lidar com boto3, filas, APIs.
- Valoriza boas práticas como Clean Code e Clean Architecture.
- Precisa de produtividade sem abrir mão de estrutura e testabilidade.

## 🏗️ Arquiteto de Software

- Deseja padronizar a estrutura de microsserviços no time.
- Busca soluções que promovam separação de camadas, modularidade e escalabilidade.
- Quer facilitar a manutenção e evolução dos serviços com base em princípios sólidos.
- Valoriza frameworks que impõem boas práticas de arquitetura sem atrapalhar a entrega.

## 🚀 Tech Lead / Engenheiro de Plataforma

- Responsável por definir padrões e acelerar entregas dentro do time.
- Procura ferramentas que otimizem o ciclo de desenvolvimento e reduzam erros comuns.
- Quer promover padronização sem limitar a flexibilidade dos times.
- Valoriza automação via CLI, estrutura pré-definida e integração com AWS.

## 🧪 Engenheiro de Qualidade / Testes

- Precisa garantir que os serviços sejam testáveis, previsíveis e confiáveis.
- Enfrenta dificuldade para testar serviços acoplados e mal estruturados.
- Se beneficia de arquitetura limpa com injeção de dependências e estrutura de testes pronta.

## 🌐 Desenvolvedor DevOps / Cloud Engineer

- Focado em rodar microsserviços de forma estável e segura na AWS.
- Quer healthcheck nativo, observabilidade e serviços leves prontos para ECS/Fargate.
- Busca soluções com bom suporte a configuração via ambiente, logs e compatibilidade com cloud-native tools.

## 🧑‍🎓 Desenvolvedor Júnior ou em Transição

- Ainda está aprendendo AWS e boas práticas de arquitetura.
- Se sente sobrecarregado com a quantidade de decisões e padrões para seguir.
- Com o Blackcat, consegue entregar microsserviços reais com confiança e estrutura.
- Aprende Clean Architecture na prática, com base sólida e produtividade.


# ✅ Requisitos Funcionais — Framework `blackcat`

## 🔧 Execução de Serviços

- Permitir execução de serviços via `run_microservice(service: Service)`.
- Suportar múltiplos serviços registrados por projeto.
- Determinar o comportamento com base no tipo de serviço.
- Suportar seleção dinâmica via variável de ambiente `SERVICE_NAME`.

## 🧩 Tipos de Serviço

- Suportar três tipos:
  - `Consumer`: serviço contínuo consumindo filas SQS.
  - `Worker`: serviço de execução pontual ou agendada.
  - `RestAPI`: serviço Flask com endpoints HTTP.
- Aplicar comportamento especializado por tipo:
  - Consumer: loop + healthcheck.
  - Worker: execução única sem healthcheck.
  - RestAPI: Flask + healthcheck embutido.

## ⚙️ Modelagem de Serviço

- Fornecer classe `Service` com atributos:
  - `name`
  - `type`
  - `entrypoint`
  - `queue_name` (quando aplicável)
  - `endpoint_module` (para APIs)

## 🛠️ CLI e Scaffolding

- Disponibilizar CLI com comando:

  ```bash
  blackcat generate-service <service-name> --type <service-type>
  ```

- Gerar estrutura completa:
  - Use case
  - Contrato
  - Entrypoint
  - Teste unitário
  - Registro em `services/__init__.py`

## 📦 Adapters AWS

- Incluir pacote `adapters_aws` com suporte a:
  - SQS: `send`, `receive`, `delete`
  - SNS: `publish`
  - DynamoDB: `save`, `get`
- Encapsular boto3 com interfaces minimalistas e testáveis.
- Tratar exceções e logs de forma padronizada.

## 📜 Configuração e Ambiente

- Carregar variáveis de ambiente via `pydantic.BaseSettings`.
- Suportar `.env` para ambientes locais.
- Validar campos obrigatórios e aplicar fallback.

## 🩺 Healthcheck

- Incluir servidor de healthcheck HTTP para:
  - Services do tipo `Consumer`
  - Services do tipo `RestAPI`
- Endpoint `/health` compatível com ECS, Fargate e K8s.

## 🔍 Observabilidade (opcional)

- Suportar integração com logging estruturado.
- Oferecer base para instrumentação de métricas e rastreamento.




# 🔐 Requisitos Não Funcionais — Framework `blackcat`

## 🧼 Qualidade de Código e Arquitetura

- O código do framework deve seguir os princípios de Clean Code e Clean Architecture.
- Deve adotar uma estrutura modular e organizada por camadas: domain, application, infra e entrypoints.
- A utilização de tipagem estática (type hints) deve ser padrão.
- Deve permitir extensão sem modificação (princípio Open/Closed).

## 🧪 Testabilidade

- Todos os componentes do framework devem ser projetados para serem testáveis isoladamente.
- A estrutura gerada pela CLI deve incluir testes unitários prontos.
- Deve facilitar o uso de mocks para AWS e outros adapters.

## ⚙️ Usabilidade e Experiência do Desenvolvedor (DX)

- Deve minimizar boilerplate e repetição de código.
- A CLI deve permitir geração automática de serviços padronizados.
- O fluxo de criação e execução de serviços deve ser simples e previsível.
- A estrutura gerada deve estar pronta para execução com o mínimo de configuração adicional.

## 🚀 Performance e Eficiência

- O consumo de mensagens SQS deve utilizar long polling para evitar requisições excessivas.
- A inicialização dos serviços deve ser leve, compatível com execução em containers.
- A comunicação com AWS deve reusar conexões sempre que possível.

## 🛠️ Manutenibilidade e Evolução

- O framework deve ser fácil de manter, com separação clara de responsabilidades.
- Deve permitir evolução incremental sem quebrar serviços existentes.
- Deve ser possível substituir adaptadores (ex: troca de backend de fila) com impacto mínimo.

## 🌍 Compatibilidade e Portabilidade

- Compatível com Python 3.10+.
- Preparado para ambientes AWS (ECS, Fargate, Lambda).
- Compatível com Docker e ferramentas de orquestração como K8s.
- Deve suportar deploy em múltiplos ambientes: dev, staging e prod.

## 🩺 Observabilidade e Diagnóstico

- Deve oferecer suporte embutido a healthcheck HTTP.
- Deve facilitar integração com sistemas de log estruturado e métricas.
- Os serviços gerados devem ser monitoráveis em ambiente produtivo (ECS, CloudWatch, etc).

## 🔐 Segurança

- Não deve expor informações sensíveis em logs.
- O uso de variáveis de ambiente deve ser seguro e validado via configuração.
- Deve seguir boas práticas de acesso seguro à AWS (IAM, Secrets Manager, VPC).

## 📚 Documentação

- Deve fornecer documentação clara com:
  - Guia de instalação
  - Exemplos por tipo de serviço
  - Referência da CLI
  - Boas práticas
- Deve incluir modelos e comentários nos templates gerados pela CLI.




# ✅ Capacidades do Framework `payment_framework`

## 🔧 Execução e Orquestração de Serviços

- Permite a definição e execução de múltiplos serviços por projeto.
- Suporte a 3 tipos de serviços:
  - **Consumer**: escuta filas SQS continuamente.
  - **Worker**: executa rotinas únicas ou agendadas (batch).
  - **RestAPI**: expõe endpoints HTTP com Flask.
- Inicialização simplificada com `run_microservice()`.
- Resolução automática do serviço a ser executado via variável `SERVICE_NAME`.
- Diferencia o ciclo de vida e comportamento com base no tipo de serviço.

## 🛠️ CLI e Automação de Estrutura

- Comando CLI `generate-service` para criar novos serviços.
- Criação automática de:
  - Caso de uso
  - Contrato (porta)
  - Entrypoint (consumer, worker ou API)
  - Teste de unidade
  - Registro no roteador de serviços (`services/__init__.py`)
- Permite padronização e aceleração da criação de novos serviços.

## 📦 Adapters AWS

- Adapters genéricos encapsulando `boto3` para:
  - **SQS** (`send`, `receive`, `delete`)
  - **SNS** (`publish`)
  - **DynamoDB** (`save`, `get`)
- Interfaces minimalistas, testáveis e reutilizáveis.
- Tratamento uniforme de erros e logs para operações AWS.
- Permite substituição fácil por mocks ou simuladores (ex: LocalStack, fake).

## 🧱 Clean Architecture Modular

- Estrutura dividida em camadas bem definidas:
  - `domain`: entidades e objetos de valor.
  - `application`: casos de uso e orquestração.
  - `infra`: repositórios, adapters, models e configuração.
  - `entrypoints`: interfaces de entrada (ex: consumidores, APIs).
- Inversão de dependência com uso de interfaces (ports).
- Desacoplamento total entre lógica de negócio e infraestrutura.

## ⚙️ Configuração e Ambientes

- Gerenciamento de configuração via `pydantic.BaseSettings`.
- Suporte a arquivos `.env` para ambientes locais.
- Validação e fallback seguro de variáveis obrigatórias.
- Permite fácil parametrização via ambiente (`dev`, `staging`, `prod`).

## 🧪 Testabilidade

- Arquitetura desenhada para facilitar testes unitários e de integração.
- Separação clara de responsabilidade entre camadas facilita mocks.
- Estrutura gerada por CLI já inclui arquivos de teste base.
- Adaptadores e casos de uso testáveis sem dependência real da AWS.

## 🩺 Healthcheck e Observabilidade

- Servidor de healthcheck incluído por padrão para:
  - Serviços do tipo **Consumer**
  - Serviços do tipo **RestAPI**
- Endpoint `/health` pronto para uso com load balancers e ECS/K8s.
- Base para integração futura com observabilidade (logs, métricas).

## 🌐 Compatibilidade com Ambientes AWS

- Framework compatível com execução em:
  - **ECS / Fargate**
  - **Docker**
  - **CloudWatch Logs**
- Adaptadores prontos para uso em ambiente cloud, com suporte a configuração via `env`.
- Estrutura preparada para integração com Secrets Manager e EventBridge.

## 🧑‍💻 Experiência do Desenvolvedor (DX)

- Curva de aprendizado suave com interface declarativa e CLI intuitiva.
- Redução significativa de boilerplate.
- Abstração total de `boto3`.
- Permite que o dev foque no negócio e não na infraestrutura.


# 🎯 Casos de Uso Alvo — Framework `blackcat`

O Blackcat foi projetado para acelerar e padronizar o desenvolvimento de microserviços pequenos e independentes, com foco em Clean Architecture, execução em nuvem (AWS) e integração com filas, tópicos e APIs.

## 📥 Serviços de Consumo de Fila (SQS)

- Processamento assíncrono de comandos ou eventos via SQS.
- Orquestração de casos de uso acionados por mensagens.
- Integração entre serviços desacoplados por eventos.
- Exemplo: `start_payment_cmd`, `order_created_evt`, `user_signup_cmd`.

## 🔄 Serviços Worker (Batch/Agendados)

- Execução de tarefas periódicas como rotinas de limpeza, reconciliação ou expiração.
- Job com ciclo de vida curto e sem dependência de entrada externa.
- Integração com orquestradores de jobs (EventBridge, cron, Airflow, etc).
- Exemplo: `expire_pending_payments`, `sync_customer_data`, `send_reminders`.

## 🌐 APIs Leves com Flask

- Exposição de endpoints REST para consulta de dados, status ou triggering de ações pontuais.
- Ideal para interfaces internas, microsserviços utilitários ou painéis administrativos.
- Rodando com Gunicorn, prontos para ECS/Fargate.
- Exemplo: `GET /payment/{id}`, `POST /invoice/{id}/resend`.

## 🧪 Prototipação de Microserviços

- Criação rápida de microserviços padronizados com CLI.
- Validação de conceitos sem necessidade de configurar boto3 manualmente.
- Ideal para POCs que precisam virar produção rapidamente.

## 🧱 Serviços com Clean Architecture Modular

- Projetos que precisam de separação clara entre domínio, aplicação, infraestrutura e entrada.
- Exemplo: serviços com regras de negócio complexas e independência de implementação AWS.

## 🌩️ Microserviços nativos em AWS

- Serviços com deploy em:
  - ECS / Fargate
  - Lambda (com adaptações)
  - Containers Docker com healthcheck compatível
- Uso de:
  - SQS
  - SNS
  - DynamoDB
  - Secrets Manager
  - CloudWatch Logs

## 🧑‍💻 Onboarding de Times e Devs

- Equipes que precisam de uma base de código consistente para serviços Python.
- Time com diferentes níveis de experiência com AWS.
- Projetos onde o tempo de setup e padronização importa mais que flexibilidade total.


# 🧠 Benefícios do Framework `blackcat`

## 🔧 Produtividade e Eficiência

- Criação rápida de microserviços padronizados com o comando `generate-service`.
- Redução significativa de código repetitivo (boilerplate).
- Agilidade no onboarding de novos serviços e desenvolvedores.
- Inicialização automática e desacoplada com `run_microservice()`.

## 🛠️ Padrão e Arquitetura Limpa

- Implementa Clean Architecture de forma prática e orientada ao domínio.
- Separação clara entre camadas: domínio, aplicação, infraestrutura e entrada.
- Arquitetura preparada para evolução, manutenção e testes.

## 📦 Integração Nativa com AWS

- Adapters prontos e reutilizáveis para SQS, SNS e DynamoDB.
- Sem necessidade de configurar boto3 manualmente.
- Compatível com AWS ECS, Fargate, Lambda e CloudWatch Logs.
- Suporte a `.env` e variáveis de ambiente para deploy em cloud.

## 🧪 Testabilidade e Qualidade

- Casos de uso e adaptadores projetados para serem testados isoladamente.
- Código gerado pela CLI já vem com testes unitários prontos.
- Fácil mock de dependências externas como filas e banco de dados.

## 🩺 Confiabilidade Operacional

- Healthcheck embutido para REST APIs e consumers.
- Pronto para ambientes com balanceamento de carga, auto scaling e monitoramento.
- Comportamento adaptável ao tipo de serviço: consumer, worker ou API.

## 🌍 Versatilidade e Escalabilidade

- Suporte a múltiplos serviços dentro do mesmo projeto.
- Ideal para workloads variados: fila, batch, API.
- Pode ser usado para MVPs, sistemas legados ou plataformas robustas.

## 🧑‍💻 Foco no Desenvolvedor

- Interface declarativa e CLI intuitiva.
- Reduz curva de aprendizado para devs iniciantes em AWS.
- Permite foco total na lógica de negócio, não na infraestrutura.
- Documentação clara, exemplos prontos e estrutura previsível.

## 🔐 Segurança e Confiabilidade

- Tratamento padronizado de exceções AWS.
- Respeita boas práticas no uso de variáveis de ambiente e segredos.
- Arquitetura compatível com ambientes seguros (IAM, VPC, Secrets Manager).


# 🧠 Especialidades Técnicas Necessárias

## 1. Arquitetura de Software
- Clean Architecture e Hexagonal Architecture  
- Design orientado a domínio (DDD – básico)  
- Princípios SOLID  
- Inversão de dependência com containers de injeção  

## 2. Desenvolvimento Backend em Python
- Padrões Pythonic e Clean Code  
- Tipagem estática (`typing`)  
- Programação orientada a objetos (OOP) e `dataclasses`  
- Manipulação de mensagens (JSON, serialização, etc.)  
- Organização de pacotes e módulos reutilizáveis  

## 3. AWS (Amazon Web Services)
- SQS (envio, recebimento, long polling)  
- SNS (publicação, tópicos)  
- DynamoDB (modelagem NoSQL, acesso com PynamoDB ou boto3)  
- Secrets Manager e variáveis de ambiente  
- Execução em ECS, Fargate ou Lambda  
- Observabilidade com CloudWatch (logs e métricas)  

## 4. Integração com AWS via boto3
- Uso avançado e seguro do `boto3`  
- Encapsulamento com adaptadores (abstração e mockabilidade)  
- Tratamento de erros da AWS  

---

# ⚙️ DevOps e Infraestrutura

- Docker (empacotamento dos serviços)  
- Configuração via `.env`, `pydantic.BaseSettings`, variáveis de ambiente  
- Healthcheck HTTP para containers  
- Integração com pipelines CI/CD (GitHub Actions, GitLab CI, etc.)  

---

# 🧪 Qualidade e Testes

- Testes unitários com `pytest`  
- Uso de `moto` ou mocks para simular serviços AWS  
- Testes por contrato para interfaces (ports)  
- Cobertura de testes e testes em camada de aplicação  

---

# 🛠️ Produtividade e Ferramentas

- Criação de CLIs com `argparse`, `click` ou similares  
- Geração de scaffolding (templates de arquivos e serviços)  
- Padronização de estrutura com código gerado  

---

# 📄 Documentação e Comunicação

- Documentar padrões, guias de uso e boas práticas (`README`, Wiki)  
- Explicar arquitetura de forma clara para onboardings  
- Criar exemplos e modelos para novos devs  

---

# 🎯 Desejável (Nice to Have)

- Conhecimento de tracing (OpenTelemetry, X-Ray)  
- Integração com EventBridge  
- Ferramentas como LocalStack ou Testcontainers  
- Familiaridade com ferramentas de scaffolding (Yeoman, Cookiecutter)  


# ✅ Conceitos Implementados pelo Framework Blackcat

## 🔧 Arquitetura e Design
- **Clean Architecture**  
  Separação por camadas: domínio, aplicação, infraestrutura e entrada.

- **Hexagonal Architecture (Ports & Adapters)**  
  Uso explícito de *input ports* e *output ports* para isolamento de dependências externas.

- **Inversão de Dependência (DIP)**  
  Interfaces definidas nas camadas internas, com injeção de implementações externas.

- **Single Responsibility Principle (SRP)**  
  Separação clara de responsabilidades entre entidades, casos de uso e adaptadores.

- **Open/Closed Principle (OCP)**  
  Componentes podem ser estendidos sem precisar ser modificados diretamente.

- **Separation of Concerns**  
  Domínio não depende de infraestrutura, e infraestrutura depende do domínio via interfaces.

## 🧱 Engenharia de Software
- **Domain-Driven Design (DDD leve)**  
  Entidades, objetos de valor e casos de uso bem definidos e isolados.

- **Programação orientada a objetos (OOP)**  
  Uso extensivo de `dataclasses`, encapsulamento e abstrações com interfaces.

- **Pythonic Design e Clean Code**  
  Código limpo, legível e idiomático com tipagem estática (`type hints`).

## ⚙️ Execução e Orquestração
- **Ciclo de vida de serviços orientado por tipo**
  - `Consumer` (event-driven, com SQS)
  - `Worker` (tarefa pontual ou agendada)
  - `RestAPI` (serviço HTTP com Flask)

- **Autoorquestração por variável de ambiente (`SERVICE_NAME`)**  
  Escolha dinâmica do serviço no runtime.

- **Factory para instanciar e registrar múltiplos serviços**  
  Execução desacoplada e modular.

## 📦 Adapters e AWS
- **Encapsulamento de boto3**  
  Interfaces simples e testáveis para SQS, SNS, DynamoDB.

- **Design orientado a adapters**  
  Implementação de adaptadores para filas, tópicos, banco e configuração.

- **Dry-run e logging estruturado nos adapters**  
  Facilita rastreamento e testes.

## 🧪 Testabilidade
- **Mock de dependências externas**  
  Arquitetura favorece substituição fácil de implementações reais.

- **Compatibilidade com `moto` e stubs**  
  Permite testes unitários sem depender da AWS real.

- **Separação clara para testes por contrato**  
  Casos de uso podem ser testados isoladamente.

## 🛠️ Dev e Produtividade
- **CLI para scaffolding de serviços**  
  Geração de arquivos e estrutura base com comando `generate-service`.

- **Padronização automática de novos microsserviços**  
  Redução de boilerplate e onboarding acelerado.

## ⚙️ Configuração
- **Gerenciamento de configuração via `pydantic.BaseSettings`**  
  Validação de variáveis de ambiente com fallback seguro.

- **Suporte a `.env` para ambientes locais**  
  Facilita setup e portabilidade.

## 🩺 Observabilidade
- **Healthcheck embutido** (`/health`)  
  Compatível com ECS, Fargate, K8s.

- **Estrutura pronta para integração com logs e métricas estruturadas**

## 🐳 Cloud Native e Deploy
- **Compatível com AWS ECS, Fargate, Lambda, Docker**  
  Serviços preparados para nuvem desde a concepção.

- **Serviços leves e portáveis com healthcheck nativo**

## 🔐 Segurança e Boas Práticas
- **Uso seguro de variáveis sensíveis (Secrets Manager)**  
- **Não exposição de segredos em logs**
- **Abstração de acesso AWS com práticas recomendadas de IAM**


# 🧱 Stack Tecnológica — Framework Blackcat

## 🔤 Linguagem
- **Python 3.10+**

---

## 🧠 Arquitetura e Design
- **Clean Architecture**
- **Hexagonal Architecture (Ports & Adapters)**
- **Domain-Driven Design (leve)**
- **Princípios SOLID**
- **Injeção de Dependência com `punq`** (ou similar)

---

## 📦 AWS SDK e Integrações
- **boto3** — SDK oficial da AWS
- **SQS** — Fila de mensagens
- **SNS** — Tópicos de notificação
- **DynamoDB** — Banco NoSQL
- **Secrets Manager** — Gestão de segredos
- **CloudWatch** — Logs e métricas

---

## ⚙️ Configuração e Ambientes
- **pydantic.BaseSettings** — Configuração com validação
- **dotenv** — Suporte a `.env` para ambientes locais

---

## 🔧 Execução e CLI
- **CLI customizada** — Geração de scaffolding (`blackcat generate-service`)
- **Flask** — Para serviços REST com healthcheck embutido
- **Gunicorn** *(sugerido para produção)*

---

## 🧪 Testes
- **pytest** — Testes unitários e de integração
- **moto** — Mock de serviços AWS (opcional)
- **unittest.mock** — Mocks e spies para injeção de dependências

---

## 🐳 Containerização e Deploy
- **Docker** — Containerização de serviços
- **ECS / Fargate** — Execução de containers na AWS
- **Lambda** *(compatível com ajustes)*
- **Variáveis de ambiente (.env)** — Config

# 📁 Diretório do Projeto que Implementa o BlackCat

```plaintext
.
├── main.py
├── blackcat
├── payment/
│   ├── application/
│   │   ├── config/
│   │   │   └── start_payment_config.py
│   │   ├── ports/
│   │   │   ├── driven/
│   │   │   │   ├── payment_repository_contracts.py
│   │   │   │   ├── queue_adapter_contracts.py
│   │   │   │   └── topic_adapter_contracts.py
│   │   │   └── driving/
│   │   │       ├── confirm_payment_usecase_contracts.py
│   │   │       ├── expire_pending_payments_usecase_contracts.py
│   │   │       └── start_payment_usecase_contracts.py
│   │   └── usecases/
│   │       ├── confirm_payment_usecase.py
│   │       ├── expire_pending_payments_usecase.py
│   │       └── start_payment_usecase.py
│   ├── domain/
│   │   ├── entities/
│   │   │   └── payment.py
│   │   └── value_objects/
│   │       └── payment_method.py
│   ├── entrypoints/
│   │   └── interfaces/
│   │       ├── api/
│   │       │   └── rest_api.py
│   │       ├── consumers/
│   │       │   ├── payment_processed_event_consumer.py
│   │       │   └── start_payment_command_consumer.py
│   │       └── worker/
│   │           └── expire_pending_payments_worker.py
│   └── infra/
│       ├── adapters/
│       │   └── start_payment_usecase_config_adapter.py
│       ├── config/
│       │   └── settings.py
│       ├── models/
│       │   └── payment_model.py
│       └── repositories/
│           └── payment_repository.py
└── tests/
    └── integration/
        ├── conftest.py
        └── start_payment/
            ├── conftest.py
            └── test_all_flow.py


