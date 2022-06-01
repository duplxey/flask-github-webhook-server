# flask-github-webhook-server

A simple CI/CD server written in [Flask](https://flask.palletsprojects.com/en/2.1.x/) that listens for [GitHub webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks/about-webhooks), verifies the signature, and performs an action.

## Setup guide

### GitHub setup

1. Navigate to your repository > "Settings" > "Webhooks" > "Add a webhook".
2. Generate a new secret (e.g. `ruby -rsecurerandom -e 'puts SecureRandom.hex(20)'`).
3. Add the newly generated secret to the webhook.
4. Store the secret somewhere safe.

### Project setup

1. Clone the project.
2. Create a new virtual environment.
3. Install the requirements using `pip install -r requirements.txt`.
4. Create a `.env` file inside the project root with the following content:
    ```
    # this information is displayed when visting the index page (/)
    API_NAME=flask-github-webhook-server
    API_DESCRIPTION=made by duplxey
    API_VERSION=1.0
   
    # this command is going to run everytime you receive a webhook message
    DEPLOY_COMMAND=bash ./deploy.sh

    GITHUB_WEBHOOK_SECRET=<your_secret>
    ```
5. Add custom commands/functionality to *deploy.sh*.
6. Run the server `flask run --host 0.0.0.0 --port 5000`.
7. Navigate to [http://localhost:5000/](http://localhost:5000/).

### Production/server setup

For production setup follow [How To Serve Flask Applications with Gunicorn and Nginx on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04) or find a similar tutorial.