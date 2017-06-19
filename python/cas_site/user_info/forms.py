from django import forms
from .models import User, Dir, Group, Proj, Level, Repos

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)

class ProjForm(forms.ModelForm):
    class Meta:
        model = Proj
        fields = ('name',)

class ReposForm(forms.ModelForm):
    class Meta:
        model = Repos
        fields = ('name',)

class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = ('name',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'repos', 'proj', 'level', 'group')
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['repos'] = forms.ModelChoiceField(
            queryset=Repos.objects.all(),
            required=True,
            label="Repository",
            widget=forms.Select(
               attrs={
                    'style':'width:auto; height:25px; border-radius: 4px',
                }
            ),
        )
        self.fields['proj'] = forms.ModelChoiceField(
            queryset=Proj.objects.all(),
            required=True,
            label="Project",
            widget=forms.Select(
               attrs={
                    'style':'width:auto; height:25px; border-radius: 4px',
                }
            ),
        )
        self.fields['group'] = forms.ModelChoiceField(queryset=Group.objects.all(),
            required=True,
            widget=forms.Select(
                attrs={
                    'style':'width:auto; height:25px; border-radius: 4px',
                }
            ),
        )
        self.fields['level'] = forms.ModelChoiceField(queryset=Level.objects.all(),
            required=True,
            widget=forms.Select(
                attrs={
                    'style':'width:auto; height:25px; border-radius: 4px',
                }
            ),
        )

class DirForm(forms.ModelForm):
    class Meta:
        model = Dir
        fields = ('name', 'repos', 'proj', 'auth', 'level', 'group')
