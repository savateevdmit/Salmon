## Краткое описание:
* В этом проекте планируется создать развлекательного Discord-бота с несколькими мини-играми, музыкой и возможностью управления голосом.
## Техническое задание:
В боте должны быть реализованы:

* __Проигрывание музыки__
  - Проигрывание музыки должно происходить при написании в чат команды `!play (композиция)`.
  - Остановка - при написании `!stop`.
* __Голосовое управление ботом__ 
  - Чтобы управлять ботом  с помощью голоса, зайдите в любой голосовой канал и напишите `!join`, бот зайдёт к вам. 
  - Скажите `(Название музыки, автор)`, и бот проиграет нужную песню.
* __Мини-игры__
   - В боте должна быть реализована игра _"Быки и коровы"_.
     - Напишите в чат `!bc` для запуска игры.
     - Напишите `!stop game`, и игра прекратится.
   - Также с помощью команды `!meme` бот должен показать рандомный мем из интернета.
   - Возможно будет реализована игра с угадыванием логотипа на время.
     - Для её запуска планируется использовать команду `!logo`.
     - Для остановки - `!stop game`.
## Пояснительная записка:
Функции, доступные для использования в нашем боте:

* I. __Музыка__
  - Чтобы проиграть музыку, напишите `!play (композиция)`, пауза, продолжить и стоп будут на кнопках.
  - Если вы закажете свою музыку, пока играет другая, ваша будет автоматически добавлена в очередь.
  - Посмотреть очередь песен можно командой `!queue`.
  - Чтобы посмотреть топ-10 песен из чарта Яндекс Музыки, напишите `!chart`.
  - Чтобы проиграть песни из чарта Яндекс Музыки, напишите `!play_chart`.
  - Для скачивания абсолютно любой музыки напишите `!dw (название песни)`. Данная функция доступна только пользователям с **👑Salmon pro**[^spro].
* II. __Фильмы__ 
  - Чтобы посмотреть информацию о фильме, а также получить ссылку на его просмотр на Кинопоиске, напишите `!film (фильм)`.
* III. __Мини-игры__
   - В боте реализована игра _"Быки и коровы"_.
     - Напишите в чат `!bc` для запуска игры.
     - Напишите `!stop_game`, и игра прекратится.
   - Также сделана игра _"Угадайка логотип"_.
     - Для её запуска используйте команду `!logo`.
     - Для остановки - `!stop_game`.
   - Чтобы сыграть с ботом в "Ним", напишите `!nim`, и игра начнётся.
     - Ним - игра, в которой два игрока по очереди берут предметы, разложенные на несколько кучек. За один ход может быть взято любое количество предметов (большее нуля) из одной кучки. Игрок, взявший последний предмет, проигрывает.
     - Для остановки используйте также `!stop_game`.
* IV. __👑Salmon pro__
  - С помощью этой подписки вы сможете без труда скачивать любую музыку, просто напишите боту `!dw (песни)`, и бот автоматически начнёт поиск и скачивание, а потом отправит её вам в личные сообщения. Вся процедура займёт не более 15 секунд, что намного быстрее, чем ручной поиск!
    - Чтобы получить информацию о подписке напишите боту `!spro`.
* V. __Другое__
  - Чтобы посмотреть информацию о любом человеке на сервере, напишите `!info (@<упомяните человека, информацию о котором хотите посмотреть>)`
  - Если вы напишите команду `!wn (город)`, то сможете посмотреть погоду в этом городе сегодня, также вам будет доступна кнопочка (`Погода на завтра ⛅`), кликнув по которой, вы сможете узнать погоду на следующий день в том же городе.
  - С помощью команды `!news` вы можете прочитать последние новости к этому часу, также вам будет доступна кнопка (`▶ Больше новостей ◀`), при нажимании на неё бот пришлёт больше новостей.
  - Если вы не знаете, как построить график функции или хотите себя проверить, то напишите `!graf (функция)`, бот его построит и пришлёт вам картинку с ним.
---

* __Для подробного описания напишите `!help` в чат с ботом__
[^spro]: Привелегированная подписка на бота (подробно описано в  пункте IV)
