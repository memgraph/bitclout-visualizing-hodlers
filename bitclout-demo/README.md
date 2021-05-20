# BitClout Demo

## Start the app

First, position yourself in the root folder of the project. Build the Docker image and run the application with the following commands:
```
docker-compose build
docker-compose up
```
If everything was successful, you can open it in your browser. The app will be listening on: http://localhost:5000/.

## Notes

The first time you run the container, leave everything as it is. Afterward, you don't have to load the BitClout data into Memgraph from CSV files 
because Docker volumes are used for persisting data. You can turn off the automatic loading on startup by changing the last line in `./Dockerfile` to:

```Dockerfile
ENTRYPOINT ["python3", "bitclout.py"]
```