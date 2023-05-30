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
  'http://localhost:8002/user/' \
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
  "access_token": "d672f730-4c50-4ff7-989b-7af1272555b6"
}
```
#### /record/ POST
Запрос:
```
curl -X 'POST' \
  'http://localhost:8002/record/?user_id=1&access_token=d672f730-4c50-4ff7-989b-7af1272555b6' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@test_audio.wav;type=audio/wav'
```
Ответ:
```
"http://localhost:8002/record?id=e9c33830-ef64-42fe-af77-37f54a3e40b5&user=1"
```
#### /record GET
Запрос:
```
curl -X 'GET' \
  'http://localhost:8002/record?id=e9c33830-ef64-42fe-af77-37f54a3e40b5&user=1' \
  -H 'accept: application/json'
```
Ответ:
![server_response](https://github.com/sat-brr/bewise-test-task2/assets/102415605/56514984-dafd-4e3c-b4b7-3b0998756c94)

### Установка и запуск в Docker
1. Склонировать репозиторий
```
git clone https://github.com/sat-brr/bewise-test-task2.git
cd bewise-test-task2
```
2. Создать файл .env и заполнить его.
```
POSTGRES_DB=Название БД
POSTGRES_USER=Имя Пользователя БД
POSTGRES_PASSWORD=Пароль от пользователя БД
APP_PORT=Порт, который будет обслуживать веб-сервис(по умолчанию указан 8000)
```
3. Построение контейнеров
```
make build
```
4. Запуск контейнеров
```
make run_app
```
