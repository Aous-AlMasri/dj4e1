from django import forms
from pics.models import Pic
from django.core.files.uploadedfile import InMemoryUploadedFile

class CreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024

    picture = forms.FileField(required=False, label="File to upload <= 2 MB")
    upload_field_name = 'picture'

    class Meta:
        model = Pic
        fields = ['title', 'text', 'picture']
    
    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', 'File must be < 2 MB')
    
    def save(self, commit=True):
        instance = super(CreateForm, self).save(commit=False)
        f = instance.picture
        
        if isinstance(f, InMemoryUploadedFile):
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr
        
        if commit:
            instance.save()
        
        return instance
