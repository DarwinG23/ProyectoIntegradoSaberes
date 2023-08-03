import django.forms as forms



class CompetenciaForm( forms.Form ):
    nombre = forms.CharField( label='Nombre', max_length=50 )
    descripcion = forms.CharField( label='Descripcion', max_length=200)