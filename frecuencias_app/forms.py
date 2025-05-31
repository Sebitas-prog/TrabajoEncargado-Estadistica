from django import forms

class CargaArchivoForm(forms.Form):
    archivo = forms.FileField(label='Selecciona un archivo Excel')
    tipo_variable = forms.ChoiceField(
        label='Tipo de variable',
        choices=[('cualitativa', 'Cualitativa'), ('cuantitativa', 'Cuantitativa')]
    )
