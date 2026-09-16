from django import forms
from .models import TareaPersonal, EventoCalendario, NotaRapida, Meta, Mensaje


class TareaForm(forms.ModelForm):
    class Meta:
        model = TareaPersonal
        fields = ['titulo', 'descripcion', 'categoria', 'prioridad', 'fecha_limite']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Título de la tarea'}),
            'descripcion': forms.Textarea(attrs={'class': 'input', 'rows': 3, 'placeholder': 'Descripción'}),
            'categoria': forms.Select(attrs={'class': 'input'}),
            'prioridad': forms.Select(attrs={'class': 'input'}),
            'fecha_limite': forms.DateTimeInput(attrs={'class': 'input', 'type': 'datetime-local'}),
        }


class EventoForm(forms.ModelForm):
    class Meta:
        model = EventoCalendario
        fields = ['titulo', 'descripcion', 'tipo', 'fecha_inicio', 'fecha_fin', 'ubicacion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Título del evento'}),
            'descripcion': forms.Textarea(attrs={'class': 'input', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'input'}),
            'fecha_inicio': forms.DateTimeInput(attrs={'class': 'input', 'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'class': 'input', 'type': 'datetime-local'}),
            'ubicacion': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Ubicación'}),
        }


class NotaForm(forms.ModelForm):
    class Meta:
        model = NotaRapida
        fields = ['titulo', 'contenido', 'color']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Título'}),
            'contenido': forms.Textarea(attrs={'class': 'input', 'rows': 4, 'placeholder': 'Contenido'}),
            'color': forms.Select(attrs={'class': 'input'}),
        }


class MetaForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = ['tipo', 'descripcion', 'objetivo', 'progreso', 'periodo', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'input'}),
            'descripcion': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Ej: Vender 50 iPhone'}),
            'objetivo': forms.NumberInput(attrs={'class': 'input', 'placeholder': '100'}),
            'progreso': forms.NumberInput(attrs={'class': 'input', 'placeholder': '0'}),
            'periodo': forms.Select(attrs={'class': 'input'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
        }


class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['destinatario', 'asunto', 'contenido', 'tipo']
        widgets = {
            'destinatario': forms.Select(attrs={'class': 'input'}),
            'asunto': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Asunto del mensaje'}),
            'contenido': forms.Textarea(attrs={'class': 'input', 'rows': 5, 'placeholder': 'Escribe tu mensaje...'}),
            'tipo': forms.Select(attrs={'class': 'input'}),
        }