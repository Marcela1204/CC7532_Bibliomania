package emprestimo;

import leitor.ILeitor;
import leitor.operacoesLeitor;

import java.util.ArrayList;
import java.util.List;

public class operacoesEmprestimo implements IEmprestimo {

    private ILeitor operacoesLeitor;

    private List<String> emprestimos = new ArrayList<>();

    public operacoesEmprestimo(ILeitor operacoesLeitor) {
        this.operacoesLeitor = operacoesLeitor;
    }

    @Override
    public void registrarEmprestimo(int idLeitor, int idLivro) {

        if (!validaLeitor(idLeitor)) {
            System.out.println("Leitor inválido.");
            return;
        }

        String registro = "Emprestimo ID " + emprestimos.size() +
                " | Leitor " + idLeitor +
                " | Livro " + idLivro;

        emprestimos.add(registro);

        System.out.println("Empréstimo registrado.");

        if (operacoesLeitor instanceof operacoesLeitor) {
            ((operacoesLeitor) operacoesLeitor)
                    .adicionarHistorico(idLeitor, "Pegou livro " + idLivro);
        }
    }

    @Override
    public void registrarDevolucao(int idEmprestimo) {

        if (idEmprestimo < emprestimos.size()) {
            System.out.println("Devolução registrada para " + emprestimos.get(idEmprestimo));
        } else {
            System.out.println("Empréstimo não encontrado.");
        }
    }

    @Override
    public void renovarEmprestimo(int idEmprestimo) {

        if (validarPrazo(idEmprestimo)) {
            System.out.println("Empréstimo renovado.");
        } else {
            System.out.println("Prazo expirado, não pode renovar.");
        }
    }

    @Override
    public List<String> visualizarEmprestimosAtivos(int idLeitor) {

        List<String> ativos = new ArrayList<>();

        for (String e : emprestimos) {
            if (e.contains("Leitor " + idLeitor)) {
                ativos.add(e);
            }
        }

        return ativos;
    }

    @Override
    public boolean validaLeitor(int idLeitor) {

        return idLeitor < operacoesLeitor.listarLeitores().size();
    }

    @Override
    public boolean validarPrazo(int idEmprestimo) {

        return idEmprestimo < emprestimos.size();
    }
}