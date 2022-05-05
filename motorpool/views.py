from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import ProcessFormView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Brand
from .forms import SendEmailForm, BrandCreationForm, BrandUpdateForm, AutoFormset


def send_email_view(request):
    if request.method == 'POST':
        # Если метод запрос POST (нажата кнопка Отправить e-mail),
        # то создаем экземпляр формы с данными из запроса
        form = SendEmailForm(request.POST)
        if form.is_valid():
            # получаем поля формы, прошедшие валидацию
            cd = form.cleaned_data
            email = cd.get('email', '')
            comment = cd.get('comment', '')
            checkbox1 = cd.get('checkbox1', False)
            checkbox2 = cd.get('checkbox2', False)
            variant = int(cd.get('variant', 1))
            variants = cd.get('variants', [])
        else:
            print(form.errors)
            messages.error(request, form.non_field_errors())
    else:
        # Если метод запрос GET (страница открыта в браузере),
        # то создаем пустой экземпляр формы
        form = SendEmailForm()

    # Передаем форму в контекст с именем form
    return render(request, 'motorpool/send_email.html', {'form': form})


# Вероятнее всего следует выносить миксины в отдельный файл
class LoginRequiredMixin:
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('admin:login'))
        return super().get(request, *args, **kwargs)


class BrandDetailView(DetailView):
    model = Brand
    template_name = 'motorpool/brand_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = self.object.cars.all()
        return context


class BrandListView(ListView):
    model = Brand
    template_name = 'motorpool/brand_list.html'
    context_object_name = 'brand_list'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand_number'] = Brand.objects.count()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('title')


class BrandCreateView(LoginRequiredMixin, CreateView):
    model = Brand
    template_name = 'motorpool/brand_create.html'
    form_class = BrandCreationForm
    success_url = reverse_lazy('motorpool:brand_list')

    def form_valid(self, form):
        messages.success(self.request, 'Новый бренд создан успешно')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)


class BrandUpdateView(UpdateView):
    model = Brand
    template_name = 'motorpool/brand_update.html'
    form_class = BrandUpdateForm
    success_url = reverse_lazy('motorpool:brand_list')

    def form_valid(self, form):
        messages.success(self.request, f'Бренд {self.object} успешно обновлён')
        return super().form_valid(form)


class BrandDeleteView(DeleteView):
    model = Brand
    template_name = 'motorpool/brand_delete.html'
    success_url = reverse_lazy('motorpool:brand_list')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f'Бренд {self.object} удален')
        return result

# Оставляю для себя для сравнения
# def auto_create_view(request, brand_pk):
#     brand = get_object_or_404(Brand, pk=brand_pk)
#     formset = AutoFormset(instance=brand)
#     if request.method == 'POST':
#         formset = AutoFormset(request.POST, request.FILES, instance=brand)
#         if formset.is_valid():
#             formset.save()
#
#     return render(request, 'motorpool/auto-create.html', {'formset': formset, 'brand': brand})


class AutoCreationView(LoginRequiredMixin, ProcessFormView, TemplateView):
    template_name = 'motorpool/auto-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = get_object_or_404(Brand, pk=self.kwargs.get('brand_pk', ''))
        if self.request.method == 'POST':
            formset = AutoFormset(self.request.POST, self.request.FILES, instance=brand)  # так же передаём бренд если метод POST
        else:
            formset = AutoFormset(instance=brand)  # instance добавляет в форму начальное значение
        context['formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        brand = get_object_or_404(Brand, pk=self.kwargs.get('brand_pk', ''))
        formset = AutoFormset(self.request.POST, self.request.FILES, instance=brand)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(brand.get_absolute_url())
        return super().get(request, *args, **kwargs)
