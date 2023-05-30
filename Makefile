lint: # проверка приложения линтером
	flake8 app

install: # установка зависимостей
	pip3 install -r requirements.txt

build: # сборка приложения и БД в контейнеры
	sudo docker-compose build

run_app: # запуск контейнеров
	sudo docker-compose up -d
