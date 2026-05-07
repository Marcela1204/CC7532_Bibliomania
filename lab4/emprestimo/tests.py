from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone

from emprestimo.models import Emprestimo
from emprestimo.container import EmprestimoContainer
from emprestimo.forms import FiltroRelatorioEmprestimoForm
from leitor.models import Leitor
from livro.models import Livro


class FiltroRelatorioEmprestimoFormTest(TestCase):
    """Testa o formulario de filtro de relatorio."""

    def test_formulario_valido_vazio(self):
        """Testa se o formulario é valido quando vazio."""
        data = {
            'data_inicio': '',
            'data_fim': '',
            'status': '',
        }
        form = FiltroRelatorioEmprestimoForm(data)
        self.assertTrue(form.is_valid())

    def test_formulario_valido_com_datas(self):
        """Testa se o formulario é valido com datas preenchidas."""
        data = {
            'data_inicio': '2025-05-01',
            'data_fim': '2025-05-31',
            'status': 'ativo',
        }
        form = FiltroRelatorioEmprestimoForm(data)
        self.assertTrue(form.is_valid())

    def test_formulario_valido_com_datas_iguais(self):
        """Testa se o formulario é valido quando as datas são iguais."""
        data = {
            'data_inicio': '2025-05-15',
            'data_fim': '2025-05-15',
            'status': '',
        }
        form = FiltroRelatorioEmprestimoForm(data)
        self.assertTrue(form.is_valid())

    def test_formulario_invalido_data_fim_anterior(self):
        """Testa se o formulario rejeita quando data_fim é anterior a data_inicio."""
        data = {
            'data_inicio': '2025-05-31',
            'data_fim': '2025-05-01',
            'status': '',
        }
        form = FiltroRelatorioEmprestimoForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('data_fim', form.errors)
        self.assertIn('anterior', str(form.errors['data_fim']).lower())

    def test_formulario_valido_apenas_data_inicio(self):
        """Testa se o formulario é valido com apenas data_inicio preenchida."""
        data = {
            'data_inicio': '2025-05-01',
            'data_fim': '',
            'status': '',
        }
        form = FiltroRelatorioEmprestimoForm(data)
        self.assertTrue(form.is_valid())

    def test_formulario_valido_apenas_data_fim(self):
        """Testa se o formulario é valido com apenas data_fim preenchida."""
        data = {
            'data_inicio': '',
            'data_fim': '2025-05-31',
            'status': '',
        }
        form = FiltroRelatorioEmprestimoForm(data)
        self.assertTrue(form.is_valid())


class RelatorioEmprestimoServiceTest(TestCase):
    """Testa os servicos de relatorio de emprestimos."""

    def setUp(self):
        """Configura dados de teste."""
        self.leitor = Leitor.objects.create(
            nome='João Silva',
            email='joao@example.com',
            telefone='11999999999',
            ativo=True,
        )
        self.livro = Livro.objects.create(
            titulo='Django para Iniciantes',
            autores='William Vincent',
            isbn='978-1491905517',
            status='disponivel',
        )
        self.service = EmprestimoContainer.get_service()

    def test_gerar_relatorio_csv_vazio(self):
        """Testa geracao de relatorio CSV vazio."""
        csv_content = self.service.gerar_relatorio_csv()
        self.assertIn('ID Empréstimo', csv_content)
        self.assertIn('Leitor', csv_content)
        self.assertIn('Livro', csv_content)

    def test_gerar_relatorio_csv_com_emprestimo(self):
        """Testa geracao de relatorio CSV com emprestimos."""
        emprestimo = self.service.registrar_emprestimo(self.leitor.id, self.livro.id)

        csv_content = self.service.gerar_relatorio_csv()
        self.assertIn(self.leitor.nome, csv_content)
        self.assertIn(self.livro.titulo, csv_content)
        self.assertIn(str(emprestimo.id), csv_content)

    def test_gerar_relatorio_csv_com_filtro_data(self):
        """Testa geracao de relatorio CSV com filtro de data."""
        emprestimo = self.service.registrar_emprestimo(self.leitor.id, self.livro.id)

        data_inicio = timezone.now().date()
        data_fim = timezone.now().date()

        csv_content = self.service.gerar_relatorio_csv(data_inicio, data_fim)
        self.assertIn(self.leitor.nome, csv_content)

    def test_gerar_relatorio_csv_com_filtro_status(self):
        """Testa geracao de relatorio CSV com filtro de status."""
        emprestimo = self.service.registrar_emprestimo(self.leitor.id, self.livro.id)

        csv_content = self.service.gerar_relatorio_csv(status='ativo')
        self.assertIn(self.leitor.nome, csv_content)

    def test_gerar_relatorio_csv_bom(self):
        """Testa se o CSV contem BOM para compatibilidade Excel."""
        csv_content = self.service.gerar_relatorio_csv()
        self.assertTrue(csv_content.startswith('\ufeff'))


class RelatorioEmprestimoViewTest(TestCase):
    """Testa as views de relatorio de emprestimos."""

    def setUp(self):
        """Configura dados de teste."""
        self.client = Client()
        self.leitor = Leitor.objects.create(
            nome='Maria Santos',
            email='maria@example.com',
            telefone='11988888888',
            ativo=True,
        )
        self.livro = Livro.objects.create(
            titulo='Python Avançado',
            autores='Luciano Ramalho',
            isbn='978-8575225011',
            status='disponivel',
        )
        self.service = EmprestimoContainer.get_service()

    def test_relatorio_view_get(self):
        """Testa se a view de relatorio carrega corretamente."""
        response = self.client.get(reverse('emprestimo:relatorio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'emprestimo/relatorio.html')
        self.assertIsInstance(response.context['form'], FiltroRelatorioEmprestimoForm)

    def test_exportar_csv_sem_filtros(self):
        """Testa exportacao CSV sem filtros."""
        emprestimo = self.service.registrar_emprestimo(self.leitor.id, self.livro.id)

        response = self.client.get(reverse('emprestimo:exportar_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('relatorio_emprestimos.csv', response['Content-Disposition'])

    def test_exportar_csv_com_filtros(self):
        """Testa exportacao CSV com filtros."""
        emprestimo = self.service.registrar_emprestimo(self.leitor.id, self.livro.id)

        data = timezone.now().date()
        response = self.client.get(
            reverse('emprestimo:exportar_csv'),
            {
                'data_inicio': str(data),
                'data_fim': str(data),
                'status': 'ativo',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')

    def test_exportar_csv_com_datas_invalidas(self):
        """Testa exportacao CSV com datas inválidas."""
        response = self.client.get(
            reverse('emprestimo:exportar_csv'),
            {
                'data_inicio': '2025-05-31',
                'data_fim': '2025-05-01',
                'status': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'emprestimo/relatorio.html')
        self.assertFormError(response, 'form', None, 'A data final não pode ser anterior à data inicial')

    def test_exportar_csv_contem_dados(self):
        """Testa se o CSV exportado contem os dados do emprestimo."""
        emprestimo = self.service.registrar_emprestimo(self.leitor.id, self.livro.id)

        response = self.client.get(reverse('emprestimo:exportar_csv'))
        content = response.content.decode('utf-8')
        self.assertIn(self.leitor.nome, content)
        self.assertIn(self.livro.titulo, content)
