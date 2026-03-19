# BPMN
[Diagrama](https://github.com/Marcela1204/CC7532_Bibliomania/blob/main/lab5/bpmn.jpg)

# Descrição das Tarefas (BPMN)
<img width="582" height="438" alt="image" src="https://github.com/user-attachments/assets/c730a288-fb63-4ad8-89ed-a9c4bf30a9e4" />

# Caso de Uso
<img width="358" height="301" alt="image" src="https://github.com/user-attachments/assets/ac6cc489-e2b2-4704-8f9e-54b46bf71553" />

---

# Regras de negócio

## RN01 - Verificar se o leitor está cadastrado
- O sistema deve garantir que o leitor esteja devidamente cadastrado antes de permitir a realização de um empréstimo.

## RN02 - Verificar se o leitor possui pendências
- O sistema deve verificar se o leitor possui pendências de empréstimos anteriores em seu nom. Caso existam, o empréstimo não deve ser permitido.

## RN03 - Verificar se o livro está disponível para empréstimo
- O sistema deve garantir que o livro esteja disponível no acervo, não estando emprestado ou reservado, antes de autorizar o empréstimo.

## RN04 - Verificar data de devolução
- O sistema deve atribuir automaticamente uma data de devolução no momento da realização do empréstimo e garantir que essa data seja respeitada, permitindo o controle de prazos.

## RN05 - Aplicar multas por atraso
- O sistema deve verificar se o leitor possui multas pendentes. Caso existam débitos em aberto, o empréstimo não deve ser autorizado até que a situação seja cobrando 1 real por dia indevido.

---

# Requisitos não funcionais
## Desempenho
- RNF01: O sistema deve verificar a disponibilidade do livro em até 2 segundos.
- RNF02: A validação do cadastro e situação do leitor deve ocorrer em até 3 segundos.
- RNF03: O registro completo do empréstimo deve ser finalizado em no máximo 5 segundos.

## Integridade dos dados
- RNF04: O sistema deve garantir que as informações de empréstimos sejam armazenadas de forma consistente e sem perdas.

## Disponibilidade do sistema
- RNF05: O sistema deve estar disponível pelo menos 99% do tempo durante o horário de funcionamento da biblioteca.

## Facilidade de uso
- RNF06: O sistema deve possuir uma interface intuitiva, permitindo que o usuário realize um empréstimo com o mínimo de etapas possível.
