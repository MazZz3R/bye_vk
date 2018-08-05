# Bye vk

Причины выпилиться из соц.сетей могут быть разными:
 * Каждый день в России заводят уголовные дела за лайки, репосты и картинки в ВК и Одноклассниках.
 Если Вы считаете, что Вас не за что привлечь, пройдёмте, гражданин, [по ссылочке](https://medialeaks.ru/2907bva-idyom-na-posadku/), там расскажут
 ![](static/hello.jpg)
 * Более глобальная [причина](https://vc.ru/43175-pochemu-stoit-udalit-vse-akkaunty-v-socialnyh-setyah): нежелание быть лабораторной крысой для алгоритмов предсказания/предопределения поведения людей

Данный набор скриптов позволяет:
1. Выгрузить все переписки вместе с фото (видео только по ссылке)
1. Выгрузить всю стену с фото
1. [TODO] Выгрузить альбомы
1. Удалить все переписки
1. [TODO] Удалить стену
1. [TODO] Удалить альбомы
1. [TODO] Удалить лайки
1. Отрисовать переписки как простейшие html-страницы

Код частично заимствован, сделан на тяп-ляп. python3

Первоочередная задача -- выкачать всё ценное и удалить из вк, а уж отрисовать историю,
чтобы предаться ностальгическим чувствам -- дело десятое. Кстати, помощь приветствуется, пока что рендерится большой html под каждый диалог, который выглядит примерно так:

![](static/wall2.png)

## Установка

1. Для работы необходим интерпретатор языка python 3 [Скачать](https://www.python.org/) (Downloads -> Ваша ОС -> Latest Python 3 Release)
![](static/python1.png)

2. Скачиваем [архив с кодом программы](https://github.com/neseleznev/bye_vk/archive/master.zip), распаковываем

3. Можно ввести свои данные в credentials.ini, а можно кликнуть по bye_vk.bat и набрать их во время работы программы

![Credentials](static/work0.png)

![Запуск](static/work1.png)

![Диалоги](static/work2.png)

![Диалог](static/work3.png)

## Для продвинутых

```
$ git clone https://github.com/neseleznev/bye_vk
$ python3 bye_vk.py
```


______________________________________________________

           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004

Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.

