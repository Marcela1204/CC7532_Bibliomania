# Condições dos componentes

## Interface IEmprestimo
## Operação registrarEmprestimo
### Pré-condição:
* O livro precisa estar disponível
* O leitor não pode estar em debito com a biblioteca
### Pós-condição
* Emprestimo registrado ou emprestimo não registrado

---

## Interface ILeitor
## Operação cadastrarLeitor
### Pré-condição
* O leitor deve haver documento válido
* O leitor não deve haver cadastro anterior
### Pós-condição
* O leitor é cadastrado ou o leitor não é cadastrado

---

## Interface ILivro
## Operação cadastrarLivro
### Pré-condição
* O ISBN deve ser válido
### Pós-condição
* O livro é cadastrado no acervo ou o livro não é cadastrado no acervo
