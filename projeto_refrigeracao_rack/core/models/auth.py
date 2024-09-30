class Auth:
    def __init__(self, required: bool, usr: str, pwd: str) -> None:
        self.required = required
        self.usr = usr
        self.pwd = pwd