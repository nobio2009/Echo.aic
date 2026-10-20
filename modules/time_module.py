from datetime import datetime

def register(assistant):
    def get_time(_=""):
        now=datetime.now()
        return now.strftime("It is %H:%M on %A, %d %B %Y.")
    assistant.command("time", "Tell the current local time and date.", get_time)
