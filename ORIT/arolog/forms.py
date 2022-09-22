from .models import AROLogModel
from django.forms import ModelForm, TextInput, Textarea

'''

class AROLogModelForm(ModelForm):
    class Meta:
        model = AROLogModel

        widgets = {
            "mo": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер истории болезни'
            }),
            "mo_unit": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите возраст пациента (число полных лет)'
            }),
            "sex": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пол пациента'
            }),
            "mkb10_diagnose": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите диагноз по МКБ-10'
            }),
            "notes": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Примечания (статус COVID-19 и т.д.)'
            })
        }
'''