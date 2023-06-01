[![flake8](https://github.com/sat-brr/bewise-test-task2/actions/workflows/flake8.yml/badge.svg)](https://github.com/sat-brr/bewise-test-task2/actions/workflows/flake8.yml)

# WAVtoMP3-converter

## Описание
Данный веб-сервис предназначен для конвертирования аудиозаписей формата WAV в формат MP3.

### REST Эндпоинты
| Маршрут | Метод | Описание |
| ------- | ----- | -------- |
| /user/ | POST | Создаёт пользователя в БД, возвращает ID и Токен доступа |
| /record/ | POST | Конвертирует аудиозапись в MP3, сохраняет конвертированную аудиозапись в БД. Возвращает ссылку для скачивания аудиозаписи |
| /record?id=record_id&user=user_id | GET | Предоставляет возможность скачать аудиофайл по ссылке |

### Примеры REST запросов
#### /user/ POST
Запрос:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/user/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "testname"
}'
```
Ответ:
```
{
  "id": 1,
  "access_token": "8d9b31e3-09af-490e-baa4-fcc07f15a327"
}
```
#### /record/ POST
Запрос:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/record/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'user_id=1' \
  -F 'access_token=8d9b31e3-09af-490e-baa4-fcc07f15a327' \
  -F 'file=@test_audio.wav;type=audio/wav'
```
Ответ:
```
{
  "download_url": "http://127.0.0.1:8000/record?id=2a8915c4-4f6b-404d-acef-b23bc43538f0&user=1"
}
```
#### /record GET
Запрос:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/record?id=2a8915c4-4f6b-404d-acef-b23bc43538f0&user=1' \
  -H 'accept: application/json'
```
Ответ:
![server_response](https://github.com/sat-brr/bewise-test-task2/assets/102415605/56514984-dafd-4e3c-b4b7-3b0998756c94)

### Установка и запуск веб-сервиса в Docker
1. Склонировать репозиторий
```
git clone https://github.com/sat-brr/wav-to-mp3-converter.git
```
2. Создать файл .env в корневой папке проекта и заполнить его.
```
POSTGRES_DB=Имя БД
POSTGRES_USER=Имя Пользователя БД
POSTGRES_PASSWORD=Пароль от пользователя БД
APP_PORT=Порт, который будет обслуживать веб-сервис(по умолчанию указывать 8000)
```
3. Собрать контейнеры
```
cd wav-to-mp3-converter/
make build
```
4. Запуск контейнеров
```
cd wav-to-mp3-converter/
make run_app
```
