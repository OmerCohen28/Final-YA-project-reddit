
class message:

    def __init__(self,sent_by:str,comments:list[str],msg:str) -> None:
        self.sent_by = sent_by
        self.comments = comments
        self.msg = msg
        self.rating = 0
