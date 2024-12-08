format:
	poetry run ruff format .

run:
	poetry run python battery_saver.py

show_logs:
	cat /var/log/battery_saver/battery_saver_log.log

clear_logs:
	rm /var/log/battery_saver/battery_saver_log.log

up_grafana:
	docker compose up -d