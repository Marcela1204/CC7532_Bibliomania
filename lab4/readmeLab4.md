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
A comunicação entre os componentes ocorre através de interfaces.   

O componente Emprestimo recebe uma referência da interface ILeitor em seu construtor. Assim, quando precisa validar um leitor ou acessar informações relacionadas a ele, utiliza os métodos definidos nessa interface.      

Exemplo conceitual da comunicação:

- Emprestimo → usa → ILeitor

Isso permite que o componente Emprestimo utilize funcionalidades do componente Leitor sem conhecer sua implementação interna.   

# Justificativa de como foi evitado o acoplamento direto
O baixo acoplamento foi obtido através da utilização de interfaces.   

O componente Emprestimo não depende diretamente da classe operacoesLeitor. Em vez disso, ele depende da interface ILeitor.   

Isso traz diversas vantagens:

1. Permite substituir a implementação do componente Leitor sem alterar o componente Emprestimo
2. Facilita manutenção e evolução do sistema
3. Melhora a modularidade da aplicação
4. Segue o princípio de programar para interfaces, não para implementações

# Instruções para execução do projeto
## Estrutura dos códigos
src <br>
├── emprestimo <br>
│ ├── IEmprestimo.java <br>
│ └── OperacoesEmprestimo.java <br>
│ <br>
├── leitor <br>
│ ├── ILeitor.java <br>
│ └── operacoesLeitor.java <br>
│ <br>
└── Main.java

## Como executar
1. Abra o codespace do github
2. Entre na pasta do laboratório 4. Digite no terminal: cd .\CC7532_Bibliomania\lab4
3. Compile o arquivo Main.java. Digite no terminal: javac Main.java
4. Execute o arquivo Main.java. Digite no terminal: java Main

