/*Aqui vai o código da interfaces IEmprestimo*/
package emprestimo;

import java.util.List;

public interface IEmprestimo {

    void registrarEmprestimo(int idLeitor, int idLivro);

    void registrarDevolucao(int idEmprestimo);

    void renovarEmprestimo(int idEmprestimo);

    List<String> visualizarEmprestimosAtivos(int idLeitor);

    boolean validaLeitor(int idLeitor);

    boolean validarPrazo(int idEmprestimo);

}