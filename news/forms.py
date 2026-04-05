from .models import Article
from django.forms import Form, ModelForm, CharField, TextInput
import datetime

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "image", "content"]

        # widgets = {
        #     "field": TextInput(attrs={
        #         "attribute": "value"
        #     })
        # }

    # def save(self, commit=True):
    #     article = super().save(commit=False)
    #     article.date = datetime.datetime.now()
    #
    #     if commit:
    #         article.save()
    #     return article


class SearchForm(Form):
    search_query = CharField(max_length=100)
    search_query.label = "Поиск по названию"
    search_query.required = False


class CombinedFilterForm(Form):
    date_range = CharField(
        label='диапазон дат',
        max_length=40,
        required=False,
        widget=TextInput(
            attrs={'class': 'form-control date-range-picker', 'placeholder': 'Диапазон дат', 'autocomplete': 'off'}
        )
    )

