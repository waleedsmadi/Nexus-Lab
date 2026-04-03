from django import forms
from .models import AuthUser
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator
from django.core.validators import FileExtensionValidator



class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=200,
        help_text="",
        label="",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email-login',
            'placeholder': 'Email...',
        })
    )



    password = forms.CharField(
        max_length=255,
        help_text="",
        label="",
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password-login',
            'placeholder': 'Password...',
        })
    )



    remember_me = forms.BooleanField(
        required=False,
        label='',
        help_text='',
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'remember-me-login',
        })

    )






class SignupModelForm(forms.ModelForm):

    re_password = forms.CharField(
        max_length=255,
        label='',
        help_text='',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password-signup',
        })
    )
    class Meta:
        model = AuthUser
        fields = ['email', 'first_name', 'last_name', 'password']

        widgets = {
            'email': forms.EmailInput(attrs={
                'id': 'email-signup',
                'class': 'form-control',
            }),

            'first_name': forms.TextInput(attrs={
                'id': 'first-name-signup',
                'class': 'form-control',
            }),

            'last_name': forms.TextInput(attrs={
                'id': 'last-name-signup',
                'class': 'form-control',
            }),


            'password': forms.PasswordInput(attrs={
                'id': 'password-signup',
                'class': 'form-control',
            }),


        }
        


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'email': 'Email...',
            'first_name': 'First Name...',
            'last_name': 'Last Name...',
            'password': 'Password...',
            're_password': 'Config Password...',
        }
        for name, field in self.fields.items():
            field.required = True
            field.help_text = ''
            field.label = ''
            field.widget.attrs.update({'placeholder': placeholders.get(name, '')})

            if name == "first_name" or name == 'last_name':
                field.max_length = 100
                field.validators.append(MinLengthValidator(2, 'must be at least 2 chars!'))
            if name == 'password':
                field.max_length = 255

    

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password, self.instance)
        return password





    def clean(self):
        cleaned_data =  super().clean()

        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password and password != re_password:
            raise ValidationError('Error: password and confirm password not matched!')
        
        return cleaned_data


    
    def save(self, commit=True):
        instance =  super().save(commit=False)
        instance.is_active = False
        instance.set_password(self.cleaned_data['password'])

        if commit:
            instance.save()
        
        return instance







class UpdateProfileForm(forms.ModelForm):
    img = forms.FileField(label='', help_text='', max_length=200, required=False, 
                          validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
                          error_messages={'img': 'Allowed extensions are: jpg, jpeg, png.'},
                          widget=forms.FileInput(attrs={
                        'style': "position: absolute; left: 0; top: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer;",
                        'id': 'file-input',
    }))
    class Meta:
        model = AuthUser
        fields = ['email', 'first_name', 'last_name', 'img']
        

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email...',
                
            }),

            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name...',
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name...',
            }),
        }

    




    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name != "img":
                field.required = True



    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name and len(first_name) < 3:
            raise ValidationError('Error: First name field must contains 3 chars at least!')
        return first_name
    

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name and len(last_name) < 3:
            raise ValidationError('Error: Last name field must contains 3 chars at least!')
        return last_name
    




class ChangePasswordForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


    password = forms.CharField(max_length=255, required=True, label='', help_text='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your old password...',
    }))


    new_password = forms.CharField(max_length=255, required=True, label='', help_text='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New password...',
    }))



    re_password = forms.CharField(max_length=255, required=True, label='', help_text='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm password...',
    }))



    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        validate_password(new_password, user=self.user)
        return new_password
    

    

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        new_password = cleaned_data.get('new_password')
        re_password = cleaned_data.get('re_password')

        if password and not self.user.check_password(password):
            self.add_error('password', 'Error: The old password is invalid!')
            

        if new_password and re_password and new_password != re_password:
            raise ValidationError('Error: The new password and the Confirm password fields do not match.')
        return cleaned_data
    


# for forgot password logic
class EmailForm(forms.Form):
    email = forms.CharField(
        max_length=200,
        label='',
        help_text='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email...',
        }),
        required=True
    )




class ResetPasswordForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


    new_password = forms.CharField(
        max_length=255,
        label='',
        help_text='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New password...',
        }),
        required=True
    )


    re_password = forms.CharField(
        max_length=255,
        label='',
        help_text='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password...',
        }),
        required=True
    )



    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        validate_password(new_password, self.user)
        return new_password
    

    def clean(self):
        cleaned_data = self.cleaned_data
        new_password = cleaned_data.get('new_password')
        re_password = cleaned_data.get('re_password')

        if new_password and re_password and new_password != re_password:
            raise ValidationError('Error: The new password and the Confirm password fields do not match.')
        return cleaned_data



    