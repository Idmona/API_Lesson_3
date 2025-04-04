# VK Link Shortener

Этот скрипт позволяет сокращать ссылки и получать статистику по кликам с помощью API VK.

## Установка

1. Убедитесь, что у вас установлен Python 3.
    
2. Установите необходимые библиотеки:
    
    ```
    pip install -r requirements.txt
    ```
    
3. Создайте файл `.env` и добавьте в него ваш токен доступа VK API:
    
    ```
    VK_API_TOKEN=ваш токен
    ```
    

## Использование

Скрипт принимает URL-адрес и определяет, является ли он уже сокращённой ссылкой. Если да, он выводит количество кликов по этой ссылке. Если нет — сокращает её.

### Сокращение ссылки

```
python main.py https://example.com
```

**Вывод:**

```
Сокращённая ссылка: https://vk.cc/abc123
```

### Подсчёт кликов

```
python main.py https://vk.cc/abc123
```

**Вывод:**

```
Общее количество кликов за всё время: 150
```

## Описание работы

Сначала скрипт проверяет, является ли переданная ссылка уже сокращённой. Если она была ранее сокращена, программа запрашивает данные о количестве кликов по этой ссылке и выводит их пользователю.

Если ссылка ещё не была сокращена, скрипт отправляет запрос к API VK для её сокращения и выдаёт пользователю новый короткий вариант ссылки.

После получения сокращённой ссылки или данных о кликах скрипт завершает работу. В случае возникновения ошибок, например, при недоступности API или неправильном вводе данных, выводятся соответствующие сообщения.

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).