from django import forms
from .models import ManagerEvaluation

# Creating form for clients to post jobs
class EvaluationOneForm(forms.ModelForm):

    # Form field vars

    # Captions
    answer_one_caption_one = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Caption One', 'rows' : '8', 'class' : 'form-control', 'style' : 'margin-top:10px' }))
    answer_one_caption_two = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Caption Two', 'rows' : '8', 'class' : 'form-control', 'style' : 'margin-top:10px'  }))
    answer_one_caption_three = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Caption Three', 'rows' : '8', 'class' : 'form-control', 'style' : 'margin-top:10px'  }))

    class Meta:
        model = ManagerEvaluation
        fields = [ "answer_one_caption_one", "answer_one_caption_two", "answer_one_caption_three" ]
