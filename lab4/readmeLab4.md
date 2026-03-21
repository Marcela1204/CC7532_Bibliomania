# Descrição de dois componentes implementados:
## Componente Leitor
O componente Leitor é responsável pelo gerenciamento dos leitores da biblioteca.   

Principais responsabilidades:   
1. Cadastro de leitores
2. Atualização de dados de leitores
3. Listagem de leitores cadastrados
4. Consulta do histórico de empréstimos de um leitor    

Este componente fornece uma interface que permite que outros componentes acessem suas funcionalidades sem depender diretamente de sua implementação.

## Componente Emprestimo
O componente Emprestimo é responsável por gerenciar o processo de empréstimo de livros.   

Principais responsabilidades:
1. Registrar empréstimos
2. Registrar devoluções
3. Renovar empréstimos
4. Visualizar empréstimos ativos
5. Validar leitores antes de realizar empréstimos
6. Validar prazos de empréstimo   

Este componente utiliza funcionalidades do componente Leitor para verificar se um leitor existe antes de registrar um empréstimo.

# Interfaces fornecidas
## ILeitor
Interface fornecida pelo componente Leitor.   

Operações disponíveis:
- cadastrarLeitor(dadosLeitor)
- atualizarLeitor(idLeitor, dadosLeitor)
- listarLeitores()
- acessarHistoricoLeitor(idLeitor)

Essa interface permite que outros componentes acessem informações e operações relacionadas aos leitores.

## IEmprestimo
Interface fornecida pelo componente Emprestimo.

Operações disponíveis:
- registrarEmprestimo(idLeitor, idLivro)
- registrarDevolucao(idEmprestimo)
- renovarEmprestimo(idEmprestimo)
- visualizarEmprestimosAtivos(idLeitor)
- validaLeitor(idLeitor)
- validarPrazo(idEmprestimo)

Essa interface define as operações responsáveis pelo gerenciamento de empréstimos.

# Interfaces requeridas
O componente Emprestimo requer a interface: <b>ILeitor</b>

Essa interface é utilizada para validar a existência de um leitor antes de registrar um empréstimo.   

Dessa forma, o componente Emprestimo depende apenas da interface e não da implementação concreta do componente Leitor.

# Explicação de como ocorre a comunicação entre eles
## Injecao de Dependencia

### Como foi implementada

A injecao de dependencia no projeto Bibliomania segue o padrao **Interface + Container (Singleton)**, aplicado nos componentes Leitor e Emprestimo. O objetivo e evitar acoplamento direto entre as camadas, permitindo que a logica de negocio (Service) nao dependa diretamente da implementacao concreta de acesso a dados (Repository).

### Estrutura por componente

Cada componente possui tres arquivos que formam o mecanismo de injecao de dependencia:

1. **`interfaces.py`** - Define as interfaces abstratas (classes ABC):
   - `IRepository` - Contrato para a camada de acesso a dados (criar, atualizar, listar, buscar)
   - `IService` - Contrato para a camada de logica de negocio (regras de negocio, validacoes)

2. **`repositories.py`** - Implementacao concreta do `IRepository`:
   - Implementa todos os metodos abstratos usando Django ORM
   - E a unica camada que conhece o banco de dados diretamente

3. **`services.py`** - Implementacao concreta do `IService`:
   - Recebe o repositorio via **construtor** (injecao por construtor)
   - Nunca instancia o repositorio diretamente
   - Depende apenas da interface abstrata, nao da implementacao concreta

4. **`container.py`** - Container de injecao de dependencia:
   - Implementa o padrao **Singleton** com `@classmethod`
   - Responsavel por instanciar e conectar as dependencias
   - Fornece metodos `get_repository()` e `get_service()`
   - Possui metodo `reset()` para facilitar testes

### Fluxo de funcionamento

```
Views/API  -->  Container.get_service()  -->  Service(repository)  -->  Repository  -->  Django ORM  -->  Banco de Dados
```

1. A **View** (ou endpoint da API) solicita o servico ao **Container**:
   ```python
   service = EmprestimoContainer.get_service()
   ```

2. O **Container** verifica se ja existe uma instancia (Singleton). Se nao, cria o **Repository** e injeta no **Service**:
   ```python
   cls._service_instance = IEmprestimo(
       emprestimo_repository=cls.get_repository(),
       leitor_repository=LeitorContainer.get_repository(),
   )
   ```

3. O **Service** recebe os repositorios pelo construtor e os armazena:
   ```python
   class IEmprestimo(IEmprestimoService):
       def __init__(
           self,
           emprestimo_repository: IEmprestimoRepository,
           leitor_repository: ILeitorRepository,
       ):
           self._emprestimo_repo = emprestimo_repository
           self._leitor_repo = leitor_repository
   ```

4. O **Service** utiliza os repositorios apenas pelas interfaces abstratas (`IEmprestimoRepository`, `ILeitorRepository`), sem conhecer as classes concretas.

### Exemplo concreto: Componente Emprestimo

O componente Emprestimo demonstra a injecao de dependencia com **multiplas dependencias**, pois depende tanto do seu proprio repositorio quanto do repositorio do Leitor:

```
emprestimo/interfaces.py       -> Define IEmprestimoRepository e IEmprestimoService (contratos abstratos)
emprestimo/repositories.py     -> EmprestimoRepository implementa IEmprestimoRepository (acesso ao banco via Django ORM)
emprestimo/services.py         -> IEmprestimo implementa IEmprestimoService, recebe IEmprestimoRepository e ILeitorRepository no construtor
emprestimo/container.py        -> EmprestimoContainer cria EmprestimoRepository e injeta junto com LeitorContainer.get_repository() em IEmprestimo
emprestimo/views.py            -> Usa EmprestimoContainer.get_service() para obter o servico pronto para uso
emprestimo/api.py              -> Usa EmprestimoContainer.get_service() para obter o servico pronto para uso
```

### Exemplo concreto: Componente Leitor

```
leitor/interfaces.py       -> Define ILeitorRepository e ILeitorService (contratos abstratos)
leitor/repositories.py     -> LeitorRepository implementa ILeitorRepository (acesso ao banco via Django ORM)
leitor/services.py         -> ILeitor implementa ILeitorService, recebe ILeitorRepository no construtor
leitor/container.py        -> LeitorContainer cria LeitorRepository e injeta em ILeitor (Singleton)
leitor/views.py            -> Usa LeitorContainer.get_service() para obter o servico pronto para uso
leitor/api.py              -> Usa LeitorContainer.get_service() para obter o servico pronto para uso
```

### Beneficios desta abordagem

- **Desacoplamento**: O Service nao conhece a implementacao concreta do Repository
- **Testabilidade**: E possivel substituir o Repository por um mock nos testes (via `Container.reset()`)
- **Principio da Inversao de Dependencia (DIP)**: Modulos de alto nivel (Service) dependem de abstracoes (interfaces), nao de implementacoes concretas
- **Singleton**: Garante uma unica instancia por componente, evitando criacao desnecessaria de objetos
- **Composicao entre componentes**: O EmprestimoContainer reutiliza o LeitorContainer para obter o repositorio de leitores, demonstrando como a DI facilita a integracao entre componentes sem acoplamento direto

# Instruções para execução do projeto

## Requisitos

- Python 3.12+
- PostgreSQL (Supabase)

## Como executar

1. Clone o repositorio:
```bash
git clone https://github.com/Marcela1204/CC7532_Bibliomania.git
```

2. Vá até a raiz do projeto
```bash
cd lab4
```

3. Crie e ative o ambiente virtual:
```bash
python -m venv .venv
```

```bash
source .venv/bin/activate  # Linux/Mac
# source .venv/Scripts/activate no Windows
```

4. Instale as dependencias:
```bash
pip install -r requirements.txt
```

5. Configure as variaveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com as credenciais de acesso
```

6. Execute as migracoes:
```bash
python manage.py migrate
```

7. Inicie o servidor Django:
```bash
python manage.py runserver
```

8. Acessar projeto rodando localmente: 
``` 
http://127.0.0.1:8000/
```

--- 

## API REST (FastAPI)

### Leitores (porta 8001)
| Metodo | Endpoint | Descricao |
|---|---|---|
| GET | `/api/leitores` | Listar todos os leitores |
| POST | `/api/leitores` | Cadastrar novo leitor |
| GET | `/api/leitores/{id}` | Buscar leitor por ID |
| PUT | `/api/leitores/{id}` | Atualizar leitor |
| GET | `/api/leitores/{id}/historico` | Historico do leitor |

### Emprestimos (porta 8002)
| Metodo | Endpoint | Descricao |
|---|---|---|
| GET | `/api/emprestimos` | Listar emprestimos ativos (filtro: ?id_leitor=) |
| POST | `/api/emprestimos` | Registrar novo emprestimo |
| POST | `/api/emprestimos/{id}/devolver` | Registrar devolucao |
| POST | `/api/emprestimos/{id}/renovar` | Renovar emprestimo |
| GET | `/api/emprestimos/{id}/prazo` | Verificar prazo e multa |

## Estrutura do Projeto

```
lab4/
├── bibliomania/          # Configuracoes do projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│   └── asgi.py
├── leitor/               # Componente Leitor
│   ├── interfaces.py     # Interfaces abstratas (DI)
│   ├── repositories.py   # Implementacao do repositorio
│   ├── services.py       # Logica de negocio
│   ├── container.py      # Container de injecao de dependencia
│   ├── models.py         # Modelo de dados
│   ├── views.py          # Views Django (MVT)
│   ├── forms.py          # Formularios
│   ├── urls.py           # Rotas
│   ├── api.py            # Endpoints FastAPI
│   └── admin.py          # Admin Django
├── emprestimo/           # Componente Emprestimo
│   ├── interfaces.py     # Interfaces abstratas (DI)
│   ├── repositories.py   # Implementacao do repositorio
│   ├── services.py       # Logica de negocio
│   ├── container.py      # Container de injecao de dependencia
│   ├── models.py         # Modelo de dados
│   ├── views.py          # Views Django (MVT)
│   ├── forms.py          # Formularios
│   ├── urls.py           # Rotas
│   ├── api.py            # Endpoints FastAPI
│   └── admin.py          # Admin Django
├── livro/                # Componente Livro
│   ├── interfaces.py     # Interfaces abstratas (DI)
│   ├── repositories.py   # Implementacao do repositorio
│   ├── services.py       # Logica de negocio + Google Books API
│   ├── container.py      # Container de injecao de dependencia
│   ├── models.py         # Modelo de dados
│   ├── views.py          # Views Django (MVT)
│   ├── forms.py          # Formularios
│   ├── urls.py           # Rotas
│   ├── api.py            # Endpoints FastAPI
│   └── admin.py          # Admin Django
├── templates/            # Templates HTML
│   ├── base.html
│   ├── leitor/
│   ├── emprestimo/
│   └── livro/
├── requirements.txt
├── manage.py
├── .env.example
├── readmelab4.md
└── .gitignore
```

