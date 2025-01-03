# OpenWeatherApp
Code for Streamlit App with OpenWeatherAPI functionalities

**Описание файлов** 
1. main_script.ipynb - скрипт, в котором идет обработка датасета, подсчет статистик, тестирование API подключения и методов рапараллеливания работы. Скрипт был написан в Google Colab
2. app.py - файл с реализцией Streamlit сервиса. Был написан в PyCharm.
3. stats.pkl - файл с сохраненным словарем со статистиками. В словаре для каждого города содержится информация о мин, макс, средней температуре, профиль по сезонам, аномалиям, тренду. Данные формируются в скрипте main_script.ipynb и используются дальше в app.py
4. requirements.txt - все установленные блоки и их версии

**Выводы про параллельность и многопоточность в работе**

Для подсчета статистик в первой части задания была создана функция, которая после была распараллелена с помощью ProcessPoolExecutor() по городам. То есть для каждого города был запущен свой процесс. 
Время работы подсчета без распараллеливания составило > 1c, в то время как распараллеливание дало 282ms (конкретно в сохранненом в гитхабе ране). На нескольких тестах распаралелливание дало лучший результат по времени, при этом мощности колаба хватило, чтобы запустить несколько процессов. Хотя при повторном ране время исполнения на обычной функции и при распараллеливании уже не отличалось так сильно.
Также был проведен тест по ассинхронному запуску (скорее в качестве технического теста реализации ассинхронных функций) - по времени как  ожидалось не вышло принципиального выигрыша.

Далее для реализации АПИ запросов была использована многопоточность. Под каждый город был создан свой поток, в рамках которого сначала производился запрос для получения координат города, а после фиальный запрос для получения данных о температуре.
В данном случае многопоточность дала принципиально лучший результат - вместо 5 секунд в одном потоке я получила 262ms на выполнение многопоточных запросов. АПИ может принимать не более 60 запросов в минуту, в текущем случае несколько потоков запросов к АПИ прошли в лимит, поэтому я не стала применять возможности по ограничению количество одновременных потоков.

**Примечание об ошибке:**

Почему-то при выводе статистик из словаря statistics в скрипте приложения значения несколько отличаются от значений в основном скрипте (при этом некритично, для каждого города значения похожи на те, что получены в основном скрипте), откуда этот словарь и был взят (в основном скрипте значения словаря совпадают со статистиками полного датасета). Ошибку в коде я не нашла, возможно, это связано с переносом данных из одного скрипта в другой в pikle файле. Прошу эти расхождения оценивать с учетом этого примечания :)
В будущем буду все делать в одном скрипте, чтобы не было переносов.


**Примечание об АПИ-ключе**

Мой ключ был стерт из основного скрипта. При необходимости для проверки могу его предоставить.


