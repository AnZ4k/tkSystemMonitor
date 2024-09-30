from flask import Flask
from core.sysinfo import get_system_info

app = Flask(__name__)


def main():
    app.run("0.0.0.0")

@app.route("/get-info", methods=["GET"])
def get_info():
    return get_system_info()

if __name__ == "__main__":
    main()