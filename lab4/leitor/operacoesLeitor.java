package leitor;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class operacoesLeitor implements ILeitor {

    private List<String> leitores = new ArrayList<>();
    private Map<Integer, List<String>> historico = new HashMap<>();

    @Override
    public void cadastrarLeitor(String dadosLeitor) {
        leitores.add(dadosLeitor);
        System.out.println("Leitor cadastrado: " + dadosLeitor);
    }

    @Override
    public void atualizarLeitor(int idLeitor, String dadosLeitor) {

        if (idLeitor < leitores.size()) {
            leitores.set(idLeitor, dadosLeitor);
            System.out.println("Leitor atualizado para: " + dadosLeitor);
        } else {
            System.out.println("Leitor não encontrado.");
        }
    }

    @Override
    public List<String> listarLeitores() {
        return leitores;
    }

    @Override
    public void acessarHistoricoLeitor(int idLeitor) {

        if (!historico.containsKey(idLeitor)) {
            System.out.println("Nenhum histórico encontrado.");
            return;
        }

        System.out.println("Histórico do leitor " + leitores.get(idLeitor) + ":");

        for (String registro : historico.get(idLeitor)) {
            System.out.println(registro);
        }
    }

    public void adicionarHistorico(int idLeitor, String evento) {

        historico.putIfAbsent(idLeitor, new ArrayList<>());
        historico.get(idLeitor).add(evento);
    }
}