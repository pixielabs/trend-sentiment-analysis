# trends-sentiment-analysis

## Setup

You will need access to the project over on the Google Cloud Platform, and a key for the service account in json format. To get this, head to https://console.cloud.google.com, navigate to the project folder and then go to APIs -> Credentials -> Create credentials -> Service account key. Select 'ml-app' and save the key locally.

Next install direnv, for automatically loading the environment when you navigate to the project folder.

```bash
brew install direnv
```

Follow the setup instructions over at https://direnv.net/ to configure direnv to work with your shell. Once this is done create a `.envrc` file, copying over from `.envrc.sample` and adding the necessary information. Run `direnv allow` to give direnv permission to load your environment.

Finally you can install dependencies:

```bash
pip install -r requirements.txt
```

To run the app:

```bash
python3 app.py
```
