Скрипт, который запускается на компьютере и управляет внешним реле.

1. Создай папку с логами:

```
sudo mkdir /var/log/battery_saver
sudo chmod 777 /var/log/battery_saver
```

2. Установка:

```
pip install .
```

3. Просмотр логов

```
nvim /var/log/battery_saver/battery_saver_log.log
```
