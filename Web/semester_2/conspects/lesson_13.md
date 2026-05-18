# Урок 13. Class-Based Views (CBV). Рефакторинг

**Тип занятия:** Лекция + Воркшоп (Рефакторинг)  
**Продолжительность:** 3 астрономических часа  
**Сложность:** Высокая (ООП, Наследование, Mixins)  

## Цели урока

1. Понять разницу между FBV (функции) и CBV (классы).
2. Изучить основные **Generic Views**: `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`.
3. Научиться подключать классы в `urls.py` через `.as_view()`.
4. Разобраться с миксинами (Mixins) вместо декораторов (`LoginRequiredMixin`).
5. Переопределить метод `form_valid`, чтобы добавлять автора к посту (автоматически).

---

## Часть 1. Конспект лекции

### 1. Зачем нам классы?

Посмотрите на функции `create_item` и `update_item` из прошлых уроков. Они на 90% одинаковые! Мы проверяем метод POST, валидируем форму, сохраняем, редиректим.
**CBV (Class-Based Views)** — это готовые "шаблоны" поведения.

* Хотите просто вывести список из БД? Берите `ListView`.
* Хотите создать объект? Берите `CreateView`.

### 2. Основные Generic Views

Django дает нам "дженерики" — классы, которые решают стандартные задачи.

* **ListView:** Делает `model.objects.all()`, пагинацию и отдает список в шаблон `app/model_list.html`.
* **DetailView:** Делает `get_object_or_404(pk=pk)` и отдает объект в шаблон `app/model_detail.html`.
* **CreateView / UpdateView:** Сами создают форму из модели, сами проверяют `is_valid()`, сами сохраняют и делают редирект.
* **DeleteView:** Показывает страницу подтверждения ("Вы уверены?"), удаляет и редиректит.

### 3. Mixins (Примеси)

Декоратор `@login_required` нельзя повесить на класс.
Вместо этого мы используем множественное наследование.

```python
class ItemCreateView(LoginRequiredMixin, CreateView):
    # ...
```

**Важно:** Миксин всегда должен стоять **слева** (первым родителем), чтобы проверка сработала до запуска логики View.

### 4. Метод `form_valid` (Магия перехвата)

В `CreateView` мы не видим момент сохранения формы `.save()`. Он спрятан.
Но что делать, если нам нужно присвоить автора (`instance.author = request.user`)?
Мы переопределяем метод `form_valid`:

```python
def form_valid(self, form):
    form.instance.author = self.request.user # Внедряемся в процесс
    return super().form_valid(form)          # Отдаем управление обратно Django
```

---

## Часть 2. Практика (Live Coding)

*Преподаватель берет код прошлого урока и переписывает его на классы.*

**Шаг 1. ListView (Главная страница)**
*Было:* Функция `index`.
*Стало:*

```python
from django.views.generic import ListView

class HomeView(ListView):
    model = Item
    template_name = 'index.html'
    context_object_name = 'items' # Чтобы в шаблоне писать items, а не object_list
    ordering = ['-created_at']    # Сортировка
```

В `urls.py`: `path('', HomeView.as_view(), name='home')`.

**Шаг 2. DetailView (Детальная страница)**
*Было:* Функция `item_detail`.
*Стало:*

```python
from django.views.generic import DetailView

class ItemDetailView(DetailView):
    model = Item
    template_name = 'item_detail.html'
    # context_object_name по умолчанию = 'item' (или имя модели строчными)
```

**Шаг 3. CreateView (Создание)**
*Было:* Функция `create_item`.
*Стало:*

```python
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'item_form.html'
    success_url = reverse_lazy('home') # Редирект после успеха (требует import reverse_lazy)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

**Шаг 4. UpdateView (Редактирование)**
Почти копия CreateView, но умеет принимать `pk` и заполнять форму данными.

```python
from django.views.generic import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'item_form.html'

    def test_func(self):
        # Защита: редактировать может только автор!
        obj = self.get_object()
        return obj.author == self.request.user
```

**Шаг 5. DeleteView (Удаление)**
*Создаем шаблон `item_confirm_delete.html`:* "Вы точно хотите удалить {{ object }}?"

```python
from django.views.generic import DeleteView

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('home')
    template_name = 'item_confirm_delete.html'
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
```

---

## Часть 3. Домашнее задание №13

**Тема:** Рефакторинг проекта на Class-Based Views.  
**Срок выполнения:** 1 неделя.  
**Максимальный балл:** 8 баллов.  

### Описание задания

Вам необходимо переписать основные View-функции вашего проекта на классы (Generic Views). Это сократит количество кода и сделает проект более профессиональным. Функционал сайта измениться не должен.

### Техническое задание (ТЗ)

1. **Главная страница (ListView):**
    * Замените функцию отображения списка на класс `ListView`.
    * Настройте `ordering`, чтобы новые записи были сверху.

2. **Детальная страница (DetailView):**
    * Замените функцию детального просмотра на `DetailView`.

3. **Создание и Редактирование (Create/Update View):**
    * Замените функции создания и редактирования на `CreateView` и `UpdateView`.
    * Используйте `LoginRequiredMixin` для защиты страниц.
    * **Важно:** Переопределите метод `form_valid` в классе создания, чтобы автоматически проставлять текущего пользователя как автора.

4. **Удаление (DeleteView):**
    * Реализуйте класс для удаления записи.
    * Создайте шаблон подтверждения удаления (стандартное имя `модель_confirm_delete.html`).
    * Добавьте кнопку "Удалить" на страницу детального просмотра (только для автора).

5. **Защита (UserPassesTestMixin):**
    * Добавьте проверку `UserPassesTestMixin` в классы Update и Delete.
    * Реализуйте метод `test_func`, чтобы удалять/редактировать запись мог только ее автор.

6. **Результат работы влейте в main с коммитом "Task 13 ready."**

### Критерии оценивания (Аддитивная система)

Максимум: **8 баллов**.

| Критерий | Баллы | Описание |
| :--- | :---: | :--- |
| **ListView & DetailView** | **+2** | Списки и просмотр работают через классы. В `urls.py` используется `.as_view()`. |
| **CreateView** | **+2** | Создание работает. Автор присваивается автоматически (метод `form_valid`). |
| **UpdateView** | **+1** | Редактирование работает. Форма предзаполняется старыми данными. |
| **DeleteView** | **+1** | Реализовано удаление с подтверждением. |
| **Mixins (Защита)** | **+2** | Использованы `LoginRequiredMixin` и `UserPassesTestMixin` (или аналог проверки авторства). Чужой пост удалить нельзя. |

### Штрафы

* **-2 балла:** `AttributeError` при запуске (забыли `.as_view()` в urls).
* **-2 балла:** Сломалось присвоение автора (пост создается без автора или падает ошибка IntegrityError).
* **-1 балл:** Миксин `LoginRequiredMixin` стоит ПОСЛЕ `CreateView` (наследование справа), из-за чего защита не работает.

---

### Полезные материалы

* [Classy Class-Based Views](https://ccbv.co.uk/) — **Самый полезный сайт по Django**. Показывает все методы и атрибуты классов в удобном виде.
* [Built-in class-based views API](https://docs.djangoproject.com/en/5.0/ref/class-based-views/) — Официальная документация.
