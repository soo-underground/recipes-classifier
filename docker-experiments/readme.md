docker-compose build

docker-compose up

docker ps

docker exec -it docker-experiments_flask-api python train-model.py

curl --location --request POST 'http://127.0.0.1:5000/iris_post' \
--header 'Content-Type: application/json' \
--data-raw '{"flower":"1,2,3,5"}'