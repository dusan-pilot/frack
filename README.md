# frack
Frame and Slack integration

Frack is simple service which enables user to send Slack command to start a default browser with embedded Frame terminal that will autostart a Frame application and open file that was specified. It is limited to .jpg and .txt file formats.

## Install

Install requirements.
```bash
pip install -r requirements.txt
```

## Run
Once the requirements have been installed, start server using **gunicorn**:
```bash
gunicorn -w 4 app:app
```

## Tests
Run python script.
```bash
python tests.py
```
