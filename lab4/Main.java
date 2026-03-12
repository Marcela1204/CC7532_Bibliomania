/*Usada para testar as operações de leitor e empréstimo, 
garantindo que as funcionalidades estejam funcionando corretamente*/

import leitor.ILeitor;
import leitor.operacoesLeitor;

import emprestimo.IEmprestimo;
import emprestimo.operacoesEmprestimo;

public class Main {

    public static void main(String[] args) {

        ILeitor operacoesLeitor = new operacoesLeitor();

        operacoesLeitor.cadastrarLeitor("Maria");
        operacoesLeitor.cadastrarLeitor("João");

        System.out.println("\nLista de leitores:");

        for (String leitor : operacoesLeitor.listarLeitores()) {
            System.out.println(leitor);
        }

        IEmprestimo operacoesEmprestimo =
                new operacoesEmprestimo(operacoesLeitor);

        System.out.println("\nRegistrando empréstimos");

        operacoesEmprestimo.registrarEmprestimo(0, 101);
        operacoesEmprestimo.registrarEmprestimo(1, 202);

        System.out.println("\nEmpréstimos ativos do leitor 0:");

        for (String e : operacoesEmprestimo.visualizarEmprestimosAtivos(0)) {
            System.out.println(e);
        }

        System.out.println("\nHistórico do leitor 0:");

        operacoesLeitor.acessarHistoricoLeitor(0);
    }
}