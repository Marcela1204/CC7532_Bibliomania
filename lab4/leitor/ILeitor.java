/*Aqui vai o código da interfaces ILeitor*/
package leitor;

import java.util.List;

public interface ILeitor {

    void cadastrarLeitor(String dadosLeitor);

    void atualizarLeitor(int idLeitor, String dadosLeitor);

    List<String> listarLeitores();

    void acessarHistoricoLeitor(int idLeitor);

}