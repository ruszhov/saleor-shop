from django import forms
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.utils.translation import pgettext_lazy
from text_unidecode import unidecode

from ...product.models import Category, CategoryTranslation
from ...product.thumbnails import create_category_background_image_thumbnails
from ..seo.fields import SeoDescriptionField, SeoTitleField


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.parent_pk = kwargs.pop('parent_pk')
        super().__init__(*args, **kwargs)
        self.fields['seo_description'] = SeoDescriptionField(
            extra_attrs={'data-bind': self['description'].auto_id})
        self.fields['seo_title'] = SeoTitleField(
            extra_attrs={'data-bind': self['name'].auto_id})

    class Meta:
        model = Category
        exclude = ['slug', 'description_json']
        labels = {
            'name': pgettext_lazy('Item name', 'Name'),
            'description': pgettext_lazy('Description', 'Description'),
            'background_image': pgettext_lazy(
                'Category form',
                'Background Image'),
            'background_image_alt': pgettext_lazy(
                'Description of a category image', 'Image description')}

    def save(self, commit=True):
        self.instance.slug = slugify(unidecode(self.instance.name))

        if self.parent_pk:
            self.instance.parent = get_object_or_404(
                Category, pk=self.parent_pk)

        instance = super().save(commit=commit)

        if instance.pk and 'background_image' in self.changed_data:
            create_category_background_image_thumbnails.delay(instance.pk)

        return instance

class CategoryTranslationForm(forms.ModelForm):
    class Meta:
        model = CategoryTranslation
        fields = [
            'language_code', 'seo_title', 'seo_description',
            'name', 'description']
        labels = {
            'language_code': pgettext_lazy('Language Code', 'Language Code'),
            'seo_title': pgettext_lazy(
                'Seo Title', 'Title for SEO'),
            'seo_description': pgettext_lazy('Seo Description', 'Description for SEO'),
            'name': pgettext_lazy('Name', 'Name'),
            'description': pgettext_lazy(
                'Description', 'Description')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['language_code'].required = True
        self.fields['seo_title'].required = False
        self.fields['seo_description'].required = False
        self.fields['name'].required = True
        self.fields['description'].required = True

    def save(self, commit=True):
        # attributes = self.get_saved_attributes()
        # self.instance.attributes = attributes
        # attrs = self.instance.product.product_type.variant_attributes.all()
        # self.instance.name = get_name_from_attributes(self.instance, attrs)
        return super().save(commit=commit)
