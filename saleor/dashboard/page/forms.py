from django import forms
from django.utils.translation import pgettext_lazy

from ...page.models import Page, PageTranslation
from ..product.forms import RichTextField
from ..seo.fields import SeoDescriptionField, SeoTitleField
from ..seo.utils import prepare_seo_description


class PageForm(forms.ModelForm):
    content = RichTextField(
        label=pgettext_lazy('Page form: page content field', 'Content'),
        required=True)

    class Meta:
        model = Page
        exclude = ['created', 'content_json']
        widgets = {
            'slug': forms.TextInput(attrs={'placeholder': 'example-slug'})}
        labels = {
            'title': pgettext_lazy(
                'Page form: title field', 'Title'),
            'slug': pgettext_lazy('Page form: slug field', 'Slug'),
            'available_on': pgettext_lazy(
                'Page form: available on which date field', 'Available on'),
            'is_published': pgettext_lazy(
                'Page form: publication status indicator', 'Is published')}
        help_texts = {
            'slug': pgettext_lazy(
                'Form field help text',
                'Slug is being used to create page URL')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['seo_description'] = SeoDescriptionField(
            extra_attrs={
                'data-bind': self['content'].auto_id,
                'data-materialize': self['content'].html_name})
        self.fields['seo_title'] = SeoTitleField(
            extra_attrs={'data-bind': self['title'].auto_id})

    def clean_slug(self):
        # Make sure slug is not being written to database with uppercase.
        slug = self.cleaned_data.get('slug')
        slug = slug.lower()
        return slug

    def clean_seo_description(self):
        seo_description = prepare_seo_description(
            seo_description=self.cleaned_data['seo_description'],
            html_description=self.data['content'],
            max_length=self.fields['seo_description'].max_length)
        return seo_description

class PageTranslationForm(forms.ModelForm):
    class Meta:
        model = PageTranslation
        fields = [
            'language_code', 'seo_title', 'seo_description',
            'title', 'content']
        labels = {
            'language_code': pgettext_lazy('Language Code', 'Language Code'),
            'seo_title': pgettext_lazy(
                'Seo Title', 'Title for SEO'),
            'seo_description': pgettext_lazy('Seo Description', 'Description for SEO'),
            'title': pgettext_lazy('Title', 'Title'),
            'content': pgettext_lazy(
                'Content', 'Content')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['language_code'].required = True
        self.fields['seo_title'].required = False
        self.fields['seo_description'].required = False
        self.fields['title'].required = True
        self.fields['content'].required = True

    def save(self, commit=True):
        # attributes = self.get_saved_attributes()
        # self.instance.attributes = attributes
        # attrs = self.instance.product.product_type.variant_attributes.all()
        # self.instance.name = get_name_from_attributes(self.instance, attrs)
        return super().save(commit=commit)
