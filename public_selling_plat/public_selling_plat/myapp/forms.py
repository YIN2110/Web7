from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'  # 或者指定需要的字段列表

from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text']

