format:
	poetry run black .

run:
	poetry run python battery_saver.py


show_logs:
	cat /var/log/battery_saver/battery_saver_log.log

clear_logs:
	rm /var/log/battery_saver/battery_saver_log.log