<h1> Тестовое задание </h1>

<h2>🫖🍵☕️</h2>

<p>Данная программа реализует работу чайника, взаимодейтвие просходит с измользованием командной строки</p>
<p>После запуска - python new_teapot.py, необходимо налить определенное количество воды, для этого необходимо использовать тип float, количество воды ограничено объемом чайника, который можно изменить в файле .env</p>
Далее программа определяет режим работы чайника, если необходимо вскепятить воду, то она будет нагрета до 100 градусов, также можно задать температуру, до которой воду необходимо нагреть
Работа чайника реализована с помощью потоков, что делает возможным отлючить нагрев, не дожидаясь достижения необходимой температуры для этого во время работы чайника необходимо отправить команду - stop
После того, как чайник закончит работу, его можно отключить командой off
По окончанию работы чайника в БД будут записаны данные о его выполненной работете
