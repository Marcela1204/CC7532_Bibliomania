from django import forms

from leitor.models import Leitor
from livro.models import Livro


class RegistrarEmprestimoForm(forms.Form):
    id_leitor = forms.ModelChoiceField(
        queryset=Leitor.objects.none(),
        label='Leitor',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Selecione um leitor',
    )
    id_livro = forms.ModelChoiceField(
        queryset=Livro.objects.none(),
        label='Livro',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Selecione um livro',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_leitor'].queryset = Leitor.objects.filter(ativo=True)
        self.fields['id_livro'].queryset = Livro.objects.filter(status='disponivel')


class FiltroRelatorioEmprestimoForm(forms.Form):
    data_inicio = forms.DateField(
        label='Data Inicial',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
    )
    data_fim = forms.DateField(
        label='Data Final',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
    )
    status = forms.ChoiceField(
        label='Status',
        choices=[
            ('', 'Todos os status'),
            ('ativo', 'Ativo'),
            ('devolvido', 'Devolvido'),
            ('atrasado', 'Atrasado'),
            ('renovado', 'Renovado'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    def clean(self):
        """Valida se o periodo de datas é valido."""
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')

        if data_inicio and data_fim:
            if data_fim < data_inicio:
                raise forms.ValidationError(
                    'A data final não pode ser anterior à data inicial. '
                    'Verifique o período selecionado.'
                )

        return cleaned_data