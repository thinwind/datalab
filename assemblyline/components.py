

def identity_text_generator(source):
    return source

class Param:
    def __init__(self,key,source=None,title='参数',generator=identity_text_generator):
        self.key = key
        self.source = source
        self.title = title
        self.generator = generator
        self.value =generator(source)