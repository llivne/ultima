# ultima file uploader

To run locally (without periodic task):
-------
1. git clone git@github.com:llivne/ultima.git
2. cd ultima
3. pip install -r ./requirements.txt
4. uvicorn main:app --host 0.0.0.0 --port 8000

To run a container of the service (including celery for periodic task):
----
1. git clone git@github.com:llivne/ultima.git 
2. cd ultima
3. docker-compose up --build

To send request
-----
example for request uploading all the files under /var/log that starts with the letter "a":

`curl -X POST --location "http://127.0.0.1:8000/uploader/" -H "Content-Type: application/json" -d "{ \"Upload_id\": \"1\", \"Source_folder\": \"/var/log\", \"Destination_bucket\": \"/tmp/ultima-dest\", \"Regex\": \"^a\" }"`

Note: if you are running the app from docker local root folder is located under /home/app/root 