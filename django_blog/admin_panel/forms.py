from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Comment, Subscriber, Post, Tag, User
from .permissions import validate_strong_password


class LoginForm(forms.Form):
    """Custom login form"""
    username = forms.CharField(max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control','placeholder': 'Username','required': True}))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control','placeholder': 'Password','required': True}))


class CommentForm(forms.ModelForm):
    """Form for creating comments"""
    
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Comment',
                'rows': 4,
                'required': True
            }),
        }


class SubscribeForm(forms.ModelForm):
    """Form for newsletter subscription"""
    
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'required': True
            }),
        }


class PostForm(forms.ModelForm):
    """Form for creating/editing posts in admin panel"""
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'featured_image', 'tags', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Post Title'
            }),
            'content': CKEditorUploadingWidget(),
            # 'content': forms.Textarea(attrs={
            #     'class': 'form-control',
            #     'rows': 10,
            #     'placeholder': 'Post content...'
            # }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of the post'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'tags': forms.CheckboxSelectMultiple(),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class TagForm(forms.ModelForm):
    """Form for creating/editing tags"""
    
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tag Name'
            }),
        }


class UserForm(forms.ModelForm):
    """Form for creating/editing users"""
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'required': True
    }),
    validators=[validate_strong_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
        'required': True
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture', 'is_active', 'is_staff',
                  'is_superuser', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'required': True
            }),

            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required': True

        }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Bio',
                'required': True
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'is_superuser': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.replace('_', '').isalnum():
            raise forms.ValidationError('Username can only contain letters, numbers, and underscores.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            if profile_picture.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Image file size must be under 2MB.')
            if not profile_picture.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError('Only PNG and JPEG images are allowed.')
        return profile_picture

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

class SearchForm(forms.Form):
    """Form for search functionality"""
    q = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search posts...',
            'required': True
        })
    )

class EmailPostsForm(forms.Form):
    posts = forms.ModelMultipleChoiceField(queryset=Post.objects.filter(status='published'),
                                           widget=forms.CheckboxSelectMultiple,required=True, label='Select Posts to Send')
    send_to_all = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input'}),
                                     required=False,label='Send all Subscribers')
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Subject'}),
                               required=True,label='Email Subject', max_length=200)
    message = forms.CharField(required=True,widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                                                         'placeholder': 'Optional additional message'}))