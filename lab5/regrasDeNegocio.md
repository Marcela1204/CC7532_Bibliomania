# Descrição das Tarefas (BPMN)
<img width="582" height="438" alt="image" src="https://github.com/user-attachments/assets/c730a288-fb63-4ad8-89ed-a9c4bf30a9e4" />


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
