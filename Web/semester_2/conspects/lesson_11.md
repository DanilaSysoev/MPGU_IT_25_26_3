# Урок 11. Медиа-файлы и связи моделей (ForeignKey, ManyToMany)

**Тип занятия:** Лекция + Воркшоп  
**Продолжительность:** 3 астрономических часа  
**Сложность:** Средняя (Настройка путей)  

## Цели урока

1. Понять разницу между **Static** (стили, скрипты разработчика) и **Media** (контент пользователей).
2. Настроить `MEDIA_URL` и `MEDIA_ROOT` в `settings.py`.
3. Использовать поле `ImageField` (библиотека `Pillow`).
4. Настроить отображение загруженных картинок в шаблонах.
5. Реализовать связь `ManyToMany` (на примере Тегов).

---

## Часть 1. Конспект лекции

### 1. Static vs Media

* **Static:** Файлы, которые лежат в репозитории (логотип сайта, `style.css`, `jquery.js`). Они не меняются во время работы сервера.
* **Media:** Файлы, которые загружают пользователи (аватарки, фото товаров). Они хранятся в отдельной папке на сервере и **никогда** не попадают в Git.

### 2. Настройка Media

В `settings.py`:

```python
MEDIA_URL = '/media/'  # URL, по которому браузер будет просить картинку
MEDIA_ROOT = BASE_DIR / 'media' # Папка на диске, куда Django будет сохранять файлы
```

В `urls.py` (только для режима `DEBUG=True`):

```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 3. ImageField

Требует установки библиотеки `Pillow` (`pip install Pillow`).
В модели:

```python
image = models.ImageField(upload_to='items/', blank=True, null=True)
# upload_to='items/' — сохранит в media/items/
# blank=True — поле необязательное в форме
# null=True — поле может быть пустым в БД
```

### 4. Загрузка файлов (HTML Form)

Важный нюанс! Форма отправки файлов должна иметь атрибут `enctype="multipart/form-data"`.
Без него браузер отправит только имя файла текстом, а не сам файл.
В шаблоне:

```html
<form method="post" enctype="multipart/form-data">
    ...
</form>
```

Во view:

```python
form = MyForm(request.POST, request.FILES) # Обязательно передать request.FILES!
```

### 5. ManyToMany (Многие ко многим)

Пример: Теги. Одна статья может иметь теги "Спорт", "Новости". Один тег "Спорт" может быть у тысячи статей.
В БД создается **промежуточная таблица** (`article_tags`), где хранятся пары `article_id` - `tag_id`.
Django делает это скрыто.

---

## Часть 2. Практика (Live Coding)

*Преподаватель добавляет картинку к модели и создает модель Tag.*

**Шаг 1. Установка Pillow**
`pip install Pillow`.
`pip freeze > requirements.txt`.

**Шаг 2. Доработка модели (ImageField)**
В `models.py`:

```python
class Item(models.Model):
    # ...
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', blank=True)
```

Создаем и применяем миграции (`makemigrations`, `migrate`).

**Шаг 3. Доработка формы (Template & View)**
В `item_form.html` добавляем `enctype`.
В `views.py` в `create_item` и `update_item` добавляем `request.FILES`.
В `item_detail.html` выводим картинку:

```html
{% if item.image %}
    <img src="{{ item.image.url }}" alt="{{ item.title }}" class="img-fluid">
{% else %}
    <img src="{% static 'img/default.jpg' %}" alt="No image">
{% endif %}
```

**Шаг 4. ManyToMany (Теги)**
Создаем модель `Tag`:

```python
class Tag(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    # ...
    tags = models.ManyToManyField(Tag, blank=True, related_name='items')
```

Регистрируем `Tag` в админке.
Создаем пару тегов.
Привязываем теги к товарам через админку (в `ItemForm` появится множественный выбор, виджет `SelectMultiple`).

---

## Часть 3. Домашнее задание №11

**Тема:** Работа с файлами и сложными связями.  
**Срок выполнения:** 1 неделя.  
**Максимальный балл:** 8 баллов.  

### Описание задания

Вам необходимо реализовать возможность прикрепления изображений к вашим записям (товарам/статьям) и классифицировать их с помощью системы тегов или категорий.

### Техническое задание (ТЗ)

1. **Настройка Media:**
    * Установите `Pillow`.
    * Пропишите `MEDIA_URL` и `MEDIA_ROOT` в настройках.
    * Добавьте маршрут для раздачи медиа-файлов в `urls.py`.
    * **Важно:** Добавьте папку `media/` в `.gitignore`! Мы не храним пользовательские файлы в репозитории кода.

2. **ImageField:**
    * Добавьте поле `image` в вашу основную модель.
    * Обновите формы создания и редактирования:
        * Добавьте `enctype="multipart/form-data"` в HTML.
        * Передайте `request.FILES` в конструктор формы во View.

3. **Отображение картинок:**
    * В списке товаров (`index.html`) выведите миниатюру изображения.
    * На детальной странице (`detail.html`) выведите полное изображение.
    * Предусмотрите заглушку (placeholder), если картинка не загружена пользователем.

4. **Связь ManyToMany (Теги):**
    * Создайте модель `Tag` (или `Category`, если хотите `ForeignKey`, но лучше `ManyToMany` для практики).
    * Добавьте поле `tags` в основную модель.
    * Выведите список тегов на странице детального просмотра товара (через цикл `{% for tag in item.tags.all %}`).

5. **Фильтрация по тегу (Bonus):**
    * Сделайте теги ссылками.
    * При клике на тег должна открываться страница со списком всех товаров, имеющих этот тег.

6. **Результат работы влейте в main с коммитом "Task 11 ready."**

### Критерии оценивания (Аддитивная система)

Максимум: **8 баллов**.

| Критерий | Баллы | Описание |
| :--- | :---: | :--- |
| **Media Settings** | **+1** | Настройки `MEDIA_ROOT` и `URL` корректны. Маршрут в `urls.py` работает. |
| **Загрузка (Upload)** | **+2** | Можно загрузить картинку через форму на сайте. Она сохраняется в папку `media/`. |
| **Вывод (Template)** | **+2** | Картинка отображается на сайте. Есть проверка `{% if item.image %}`. |
| **ManyToMany** | **+2** | Модель `Tag` создана и связана. Теги можно назначать через админку или форму. |
| **Вывод тегов** | **+1** | Список тегов отображается в карточке товара. |

### Штрафы

* **-2 балла:** Картинки загружаются, но не отображаются (ошибка 404, неправильный URL).
* **-1 балл:** Папка `media` попала в коммит Git. Это засоряет репозиторий.
* **-1 балл:** Отсутствие атрибута `enctype` в форме (файл не отправляется).

---

### Полезные материалы

* [Managing files (Django Docs)](https://docs.djangoproject.com/en/5.0/topics/files/)
* [Model field reference: ImageField](https://docs.djangoproject.com/en/5.0/ref/models/fields/#imagefield)
* [Many-to-many relationships](https://docs.djangoproject.com/en/5.0/topics/db/examples/many_to_many/)
