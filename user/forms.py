from django import forms
from . models  import user

class RegistrationForm(forms.ModelForm ):
    password = forms.CharField(widget = forms.PasswordInput(attrs={
        # 'placeholder' : 'Enter Password',
        'class' : 'form-control',
        }))
    confirm_password = forms.CharField(widget = forms.PasswordInput(attrs={
        'class':'form-control',
        }))
    class Meta:
        model = user
        fields = ['first_name','last_name','phone_number','email','password']

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name']
        self.fields['last_name']
        self.fields['phone_number']
        self.fields['email']
       

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Password does not matching..!')
        
    def clean_phone(self):
        cleaned_data = super(RegistrationForm,self).clean()
        phone = cleaned_data.get['phone_number']
        if ' ' in phone:
            raise forms.ValidationError('Phone number should not contain any spaces.')
        return phone
    


class VerifyForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ['code']
    code = forms.CharField(max_length=6,required=True,help_text='Enter Code')

    code = forms.CharField(widget = forms.PasswordInput(attrs={
        'class':'form-control',
        }))


class EditProfileForm(forms.ModelForm):
    class Meta:
          model = user
          fields = ['first_name','last_name']

    first_name = forms.CharField(widget = forms.TextInput(attrs={
        'class':'form-control',
        }))
    
    last_name = forms.CharField(widget = forms.TextInput(attrs={
        'class':'form-control',
        }))
  