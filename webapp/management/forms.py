from django import forms
from .models import ManagerEvaluation

# Creating form for evaluation
class EvaluationOneForm(forms.ModelForm):

    # Form field vars

    # Captions
    answer_one_caption_one = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Caption One', 'rows' : '8', 'class' : 'form-control', 'style' : 'margin-top:10px' }))
    answer_one_caption_two = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Caption Two', 'rows' : '8', 'class' : 'form-control', 'style' : 'margin-top:10px'  }))
    answer_one_caption_three = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Caption Three', 'rows' : '8', 'class' : 'form-control', 'style' : 'margin-top:10px'  }))

    class Meta:
        model = ManagerEvaluation
        fields = [ "answer_one_caption_one", "answer_one_caption_two", "answer_one_caption_three" ]

# Creating form for clients to post jobs
class EvaluationTwoForm(forms.ModelForm):
    def clean_image(self):  
        image = self.cleaned_data.get('answer_two_img', False)
        if image:
            if image.size > 4*1024*1024:
                raise ValidationError("Image file too large ( > 4mb )")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")

    # Form field vars

    # Captions
    answer_two_caption = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Enter caption here.', 'rows' : '8', 'class' : 'form-control', 'style' : 'margin-top:10px' }))
    answer_two_what_are_problems = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Notice any problems with these post? List them here.', 'rows' : '8', 'class' : 'form-control', 'style' : 'margin-top:10px'  }))
    class Meta:
        model = ManagerEvaluation
        fields = [ "answer_two_caption", "answer_two_what_are_problems", "answer_two_img" ]

# Creating form for clients to post jobs
class EvaluationThreeForm(forms.ModelForm):
    def clean_image(self):  
        image = self.cleaned_data.get('answer_three_img', False)
        if image:
            if image.size > 4*1024*1024:
                raise ValidationError("Image file too large ( > 4mb )")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")

    # Form field vars

    # Captions
    answer_three_caption = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Enter caption here.', 'rows' : '8', 'class' : 'form-control', 'style' : 'margin-top:10px' }))
    class Meta:
        model = ManagerEvaluation
        fields = [ "answer_three_caption", "answer_three_img" ]