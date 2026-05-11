# Урок 12. Комментарии и улучшение UX (Messages)

**Тип занятия:** Лекция + Воркшоп  
**Продолжительность:** 3 астрономических часа  
**Сложность:** Высокая (Много кода в одном месте)  

## Цели урока

1. Спроектировать модель `Comment` (связь с `User` и `Item`).
2. Создать форму для комментария (`ModelForm`).
3. Реализовать добавление комментария на странице детального просмотра (вложенная форма).
4. Использовать `django.contrib.messages` для обратной связи с пользователем.
5. Понять, что такое `related_name` и как получить комментарии к посту (`item.comments.all()`).

---

## Часть 1. Конспект лекции

### 1. Модель Комментария

Комментарий не существует сам по себе. Он всегда привязан к:

1. **Автору** (`ForeignKey` на `User`).
2. **Объекту** (`ForeignKey` на `Item/Post`).
3. Имеет **текст** (`TextField`).
4. Имеет **дату** (`created_at`).

### 2. Обратная связь (`related_name`)

Когда мы пишем `post = models.ForeignKey(Post, related_name='comments')`, мы говорим Django:
"У поста появится виртуальное поле `.comments`, в котором будут лежать все комментарии к нему".
Без `related_name` пришлось бы писать `post.comment_set.all()`.

### 3. Вложенная форма (Form on Detail Page)

Часто форму комментария размещают прямо под статьей.
Это значит, что одна View-функция (`item_detail`) должна обрабатывать и показ статьи (GET), и отправку формы (POST).
Или (проще для новичков) — отдельная View (`add_comment`) только для обработки POST, которая потом редиректит обратно на деталку. Мы выберем этот путь.

### 4. Сообщения (`messages`)

После отправки комментария пользователь хочет знать: "Ушло или нет?".
Django имеет встроенный фреймворк сообщений.

* `messages.success(request, 'Ваш комментарий добавлен!')`
* `messages.error(request, 'Ошибка валидации.')`
В шаблоне мы просто перебираем их циклом и выводим красивые плашки.

---

## Часть 2. Практика (Live Coding)

*Преподаватель создает систему комментариев с нуля.*

### Шаг 1. Модель (models.py)

```python
class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.item}'
```

*Миграции:* `makemigrations`, `migrate`.

### Шаг 2. Форма (forms.py)

```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text'] # Автор и Товар подставятся автоматически
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
```

### Шаг 3. View (Добавление комментария)

В `views.py`:

```python
@login_required
def add_comment(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.item = item
        comment.author = request.user
        comment.save()
        messages.success(request, 'Ваш комментарий успешно добавлен!')
    else:
        messages.error(request, 'Ошибка при добавлении комментария.')
        
    return redirect('item_detail', pk=pk)
```

В `urls.py`: `path('item/<int:pk>/comment/', views.add_comment, name='add_comment')`.

### Шаг 4. Шаблон (item_detail.html)

1. **Вывод сообщений:**

    ```html
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    ```

2. **Список комментариев:**

    ```html
    <h3>Комментарии ({{ item.comments.count }})</h3>
    {% for comment in item.comments.all %}
        <div class="card mb-2">
            <div class="card-body">
                <strong>{{ comment.author }}</strong> <small>{{ comment.created_at }}</small>
                <p>{{ comment.text }}</p>
            </div>
        </div>
    {% empty %}
        <p>Пока нет комментариев.</p>
    {% endfor %}
    ```

3. **Форма добавления:**

    ```html
    {% if user.is_authenticated %}
        <form action="{% url 'add_comment' item.pk %}" method="post">
            {% csrf_token %}
            {{ comment_form.as_p }} <!-- Форму надо передать в контекст item_detail -->
            <button class="btn btn-primary">Отправить</button>
        </form>
    {% else %}
        <p><a href="{% url 'login' %}">Войдите</a>, чтобы оставить комментарий.</p>
    {% endif %}
    ```

---

## Часть 3. Домашнее задание №12

**Тема:** Реализация комментариев и уведомлений.  
**Срок выполнения:** 1 неделя.  
**Максимальный балл:** 8 баллов.  

### Описание задания

Вам необходимо "оживить" ваш проект, позволив пользователям обсуждать контент. Реализуйте модель комментариев, форму их добавления и вывод списка под каждой записью. Также добавьте всплывающие уведомления об успехе/ошибке действий.

### Техническое задание (ТЗ)

1. **Модель Comment:**
    * Создайте модель с полями: `text`, `created_at`, `author` (ForeignKey на User), `post` (ForeignKey на вашу основную модель).
    * Используйте `related_name='comments'` для удобного доступа.

2. **Форма и View:**
    * Создайте `CommentForm` (только поле текста).
    * Реализуйте view-функцию `add_comment`, которая принимает `pk` поста.
    * **Важно:** Не забудьте привязать автора (`request.user`) и пост к комментарию перед сохранением (`commit=False`).

3. **Интеграция в шаблон:**
    * На странице детального просмотра выведите список всех комментариев к текущему посту.
    * Над списком (или под ним) выведите форму добавления.
    * Скройте форму для незарегистрированных пользователей (покажите ссылку на вход).

4. **UX: Сообщения (Messages):**
    * В `base.html` (или в блоке контента) добавьте код для вывода `messages`.
    * Добавьте вызов `messages.success(...)` при успешном создании комментария, товара или регистрации.
    * Добавьте вызов `messages.error(...)`, если форма не валидна.

5. **Bootstrap Alerts:**
    * Стилизуйте сообщения, используя классы `alert alert-success` и `alert alert-danger`.

6. **Результат работы влейте в main с коммитом "Task 12 ready."**

### Критерии оценивания (Аддитивная система)

Максимум: **8 баллов**.

| Критерий | Баллы | Описание |
| :--- | :---: | :--- |
| **Модель Комментария** | **+2** | Модель создана, связи прописаны верно. Миграции применены. |
| **Добавление (POST)** | **+2** | Комментарий сохраняется в БД с привязкой к текущему юзеру и посту. |
| **Вывод списка** | **+1** | Комментарии отображаются на странице поста. |
| **Сообщения (Messages)** | **+2** | Реализован вывод уведомлений (Success/Error). Они исчезают после перезагрузки. |
| **Защита** | **+1** | Аноним не видит форму отправки или перенаправляется на логин при попытке отправить. |

### Штрафы

* **-2 балла:** Ошибка 500 при отправке комментария (не привязали автора или пост).
* **-1 балл:** Комментарии отображаются не к тому посту (забыли фильтрацию или неправильно использовали `related_name`).
* **-1 балл:** Сообщения выводятся без стилей (просто текст), их трудно заметить.

---

### Полезные материалы

* [The messages framework (Django Docs)](https://docs.djangoproject.com/en/5.0/ref/contrib/messages/)
* [Adding comments to a Django blog (Tutorial)](https://djangocentral.com/creating-comments-system-with-django/) — (на английском) хороший пример.
