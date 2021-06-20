This is a backend part of the JobAdvisor project.

The application requires a PostgreSQL service. After that, you need to define the environment variables from the `example.env` file according to your environment.

To start the project, you need to install dependencies from the `requirements.txt` file and start the server using the `uwsgi --ini uwsgi.ini` command or use the Docker image of the application from the registry of the project.