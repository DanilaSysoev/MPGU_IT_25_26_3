# Урок 9. ModelForms: Создание и редактирование объектов

**Тип занятия:** Лекция + Live Coding  
**Продолжительность:** 3 астрономических часа  
**Сложность:** Высокая (Логика обработки форм)  

## Цели урока

1. Понять отличие `forms.Form` (из Урока 8) от `forms.ModelForm`.
2. Создать форму на основе модели (автоматическая генерация полей).
3. Реализовать **Create View**: создание новой записи в БД через веб-интерфейс.
4. Реализовать **Update View**: редактирование существующей записи.
5. Понять, зачем нужен аргумент `instance` при инициализации формы.

---

## Часть 1. Конспект лекции

### 1. Проблема дублирования (DRY)

На прошлом уроке мы вручную писали: `name = forms.CharField(...)`.
Но у нас уже есть модель `Product` с полем `name`. Зачем писать одно и то же дважды? Если мы изменим модель (сделаем поле необязательным), нам придется помнить и менять форму. Это источник багов.

### 2. Решение: ModelForm

Это класс, который "читает" вашу модель и сам создает поля формы.

```python
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description'] # Или '__all__'
```

Django сам поймет: "Ага, `title` в модели — это `CharField`, значит я нарисую `<input type="text">`".

### 3. Метод `.save()`

В обычной форме (Урок 8) нам приходилось писать:
`Product.objects.create(**form.cleaned_data)`.
В `ModelForm` метод `.save()` уже встроен. Он сам знает, в какую таблицу писать.

### 4. Создание (Create) vs Редактирование (Update)

Форма одна, а действий два. Как Django понимает разницу?

* **Create:** `form = ProductForm(request.POST)`
  * У формы нет "привязки" к ID. Метод `.save()` сделает SQL `INSERT`.
* **Update:** `form = ProductForm(request.POST, instance=existing_item)`
  * Мы передаем `instance` (объект из БД). Django понимает: "Мы меняем ЭТОТ объект". Метод `.save()` сделает SQL `UPDATE`.

### 5. Паттерн обработки формы (Standard Boilerplate)

Это код, который студенты будут писать тысячи раз. Его нужно запомнить наизусть.

```python
# 1. Получить данные (или None, если это GET)
form = MyForm(request.POST or None, instance=obj)

# 2. Проверить
if form.is_valid():
    form.save()
    return redirect('success')

# 3. Отдать шаблон
return render(request, 'template.html', {'form': form})
```

*(Примечание: `request.POST or None` — это трюк, позволяющий сократить `if request.method == 'POST'`)*.

---

## Часть 2. Практика (Live Coding)

*Преподаватель реализует полный цикл CRUD (без Delete пока).*

### Шаг 1. Форма (forms.py)

```python
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'image'] # image покажем, если успеем, или оставим на урок 11
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
```

### Шаг 2. Вьюха создания (views.py)

```python
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save() # save возвращает созданный объект
            # Редирект на страницу только что созданного товара
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm()
    
    return render(request, 'item_form.html', {'form': form, 'title': 'Создание товара'})
```

### Шаг 3. Вьюха редактирования (views.py)

```python
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk) # Сначала достаем объект
    
    if request.method == 'POST':
        # Передаем instance! Иначе создастся дубликат
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_detail', pk=item.pk)
    else:
        # Заполняем форму текущими данными
        form = ItemForm(instance=item)
        
    return render(request, 'item_form.html', {'form': form, 'title': 'Редактирование товара'})
```

### Шаг 4. Универсальный шаблон (`item_form.html`)

Используем один шаблон для обоих действий. Меняем только заголовок.

```html
{% extends 'base.html' %}

{% block content %}
    <h2>{{ title }}</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-success">Сохранить</button>
    </form>
{% endblock %}
```

---

## Часть 3. Домашнее задание №9

**Тема:** Реализация функционала добавления и редактирования контента.  
**Срок выполнения:** 1 неделя.  
**Максимальный балл:** 8 баллов.  

### Описание задания

Вам необходимо превратить ваш сайт из "музея" (только просмотр) в полноценный инструмент. Реализуйте возможность добавлять новые записи (товары/статьи) и редактировать уже существующие через веб-интерфейс.

### Техническое задание (ТЗ)

1. **ModelForm:**
    * В `forms.py` создайте класс формы, связанный с вашей основной моделью.
    * В классе `Meta` перечислите поля, которые пользователь может заполнять (не включайте туда `created_at` или `views_count`, они должны заполняться автоматически).
    * Добавьте виджеты (CSS-классы `form-control`), чтобы форма была красивой.

2. **Create View (Добавление):**
    * Создайте View-функцию для создания объекта.
    * Обработайте `POST`-запрос (сохранение) и `GET`-запрос (пустая форма).
    * После успешного сохранения сделайте редирект на страницу списка или детальную страницу нового объекта.
    * В шаблоне списка (`index.html`) добавьте кнопку "Добавить новый товар".

3. **Update View (Редактирование):**
    * Создайте View-функцию, принимающую `pk` (id объекта).
    * Получите объект через `get_object_or_404`.
    * Инициализируйте форму с аргументом `instance=obj`.
    * В шаблоне детального просмотра (`detail.html`) добавьте кнопку "Редактировать", ведущую на эту страницу.

4. **Шаблон формы:**
    * Создайте файл `form.html` (или используйте имя типа `product_form.html`).
    * Выведите форму, токен CSRF и кнопку "Сохранить".
    * Сделайте так, чтобы заголовок страницы менялся в зависимости от контекста ("Создание..." или "Редактирование...").

5. **Результат работы влейте в main с коммитом "Task 9 ready."**

### Критерии оценивания (Аддитивная система)

Максимум: **8 баллов**.

| Критерий | Баллы | Описание |
| :--- | :---: | :--- |
| **ModelForm** | **+2** | Использован класс `ModelForm`, поля подтянулись из модели автоматически. Код чистый (DRY). |
| **Создание (Create)** | **+2** | Новые записи успешно добавляются в БД через сайт. Редирект работает. |
| **Редактирование (Update)** | **+2** | Старые записи изменяются, а не дублируются. При открытии страницы редактирования поля уже заполнены старыми данными (`instance`). |
| **UI/UX** | **+1** | На сайте есть кнопки "Добавить" и "Редактировать". Формы стилизованы (Bootstrap widgets). |
| **Валидация** | **+1** | Нельзя сохранить пустую форму (если поля обязательны). Ошибки выводятся пользователю (стандартный механизм Django). |

### Штрафы

* **-2 балла:** Дублирование записей при редактировании (забыли передать `instance` в POST-запросе).
* **-1 балл:** Ручное присвоение полей во view (`item.title = form.cleaned_data['title']...`) вместо `form.save()`. Мы используем ModelForm именно чтобы этого избежать.
* **-1 балл:** Отсутствие защиты CSRF.

---

### Полезные материалы

* [Creating forms from models (Django Docs)](https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/)
* [Styling Django Forms with Bootstrap](https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html) — (на английском) как сделать красиво.
