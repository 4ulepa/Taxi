from django import forms
from .models import Brand, Auto


class SendEmailForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=30, required=False)
    email = forms.EmailField(label='Ваш email', required=False)
    comment = forms.CharField(label='Комментарий', required=False, widget=forms.Textarea)
    checkbox1 = forms.BooleanField(label='Чекбокс 1', required=False)
    checkbox2 = forms.BooleanField(label='Чекбокс 2', required=False)
    amount = forms.IntegerField(label='Сумма', required=False)
    variant = forms.ChoiceField(label='Один вариант', choices=(
        (1, 'Вариант 1'),
        (2, 'Вариант 2'),
        (3, 'Вариант 3'),
        (4, 'Вариант 4'),
    ))
    variants = forms.MultipleChoiceField(label='Несколько вариантов', choices=(
        (1, 'Множественный выбор 1'),
        (2, 'Множественный выбор 2'),
        (3, 'Множественный выбор 3'),
        (4, 'Множественный выбор 4'),
    ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите имя'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите email'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'rows': 3})
        self.fields['checkbox1'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['checkbox2'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['variant'].widget.attrs.update({'class': 'form-select'})
        self.fields['variants'].widget.attrs.update({'class': 'form-select', 'multiple': True})

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')

        check_successful = True

        msg = 'Это поле должно быть обязательно заполнено'
        if not name:
            self.add_error('name', msg)
            check_successful = False

        if not check_successful:
            raise forms.ValidationError('Форма содержит ошибки')

        return cleaned_data

    def clean_variants(self):
        variants = self.cleaned_data['variants']
        if len(variants) < 2:
            raise forms.ValidationError('Нужно выбрать минимум 2 варианта')
        else:
            return variants


class BrandCreationForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('title', 'logo')

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')

        if Brand.objects.filter(title=title).exists():
            raise forms.ValidationError(f'Бренд с названием {title} уже существует')

        return cleaned_data


class BrandUpdateForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('title', 'logo')


class AutoCreationForm(forms.ModelForm):
    class Meta:
        model = Auto
        exclude = ('brand', 'id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_form_select = ('number', 'year', 'options', 'auto_class')
        fields_form_control = ('number', 'year', 'description')
        for field in fields_form_select:
            self.fields[field].widget.attrs.update({'class': 'form-select'})
        for field in fields_form_control:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['options'].widget.attrs.update({'multiple': True})
        self.fields['description'].widget.attrs.update({'rows': 3})

    def clean_number(self):
        number = self.cleaned_data.get('number')
        if Auto.objects.filter(number=number).exists():
            raise forms.ValidationError(f'Машина с номером {number} уже существует')
        return number


class BaseAutoCreationFormSet(forms.BaseInlineFormSet):
    def get_queryset(self):
        return Auto.objects.none()

    def clean(self):
        """Проверим что добавляемые автомобили не имеют одинаковых номеров и выдаём ошибку, если формы не заполнены"""
        if any(self.errors):
            return

        all_forms_are_empty = True
        numbers = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                # если форма помечена как удаленная, то пропускаем ее
                continue
            all_forms_are_empty = all_forms_are_empty and not any(form.cleaned_data)
            number = form.cleaned_data.get('number')

            if number and number in numbers:
                raise forms.ValidationError(f'В наборе присутствуют машины с одинаковым номером: {number}')
            numbers.append(number)

        if all_forms_are_empty:
            raise forms.ValidationError('Все формы пустые. Заполните данные')


AutoFormset = forms.inlineformset_factory(Brand, Auto, form=AutoCreationForm,
                                          can_delete_extra=False, formset=BaseAutoCreationFormSet, extra=2)
