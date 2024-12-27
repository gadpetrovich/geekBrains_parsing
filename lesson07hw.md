# сбор почты через selenium

## url

https://mail.ru

## описание

извлечь список писем и их содержимое

## конфигурация

в файле lesson07hw.ini задаются настройки

```ini
[lesson07hw]
login=username@mail.ru
password=password
mails_count=кол-во_писем
```

## проблемы

1. Не удается добраться до поля имени пользователя. xpath: "//input" просто не работает. Использовал ```driver.switch_to.frame(frame_reference=driver.find_element(By.XPATH, '//iframe[@class="ag-popup__frame__layout__iframe"]'))``` для перехода в iframe окна аутентификации.
2. Не идет скроллинг сраницы `driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")`. По подсказке преподавателя использовал хоткеи для прохода по письмам.
