import subprocess


def clean_text(text):
    return str(text).replace('"', '\\"')


def send_notification(title, message):
    title = clean_text(title)
    message = clean_text(message)

    script = f'display notification "{message}" with title "{title}"'

    subprocess.run(["osascript", "-e", script])