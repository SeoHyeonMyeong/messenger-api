
class Message():
    
    def __init__(self, dict):
        self.title = dict["title"]
        self.content = dict["content"]
    
    def get_content(self):
        return self.content
    
    def get_data(self):
        data = {
            "title": self.title,
            "content": self.content,
        }
        return data