
__GENERATOR_CLS_REGISTRY__ = {} 
__GENERATOR_FUN_REGISTRY__ = {}


class GeneratorMeta(type):
    def __new__(meta,name,bases,class_dict):
        cls = type.__new__(meta,name,bases,class_dict)
        type_name = class_dict.get('type_name')
        if not type_name:
            type_name = name
        __GENERATOR_CLS_REGISTRY__[type_name] = cls

class IndentityGenerator(metaclass=GeneratorMeta):
    type_name = 'text'

    @classmethod
    def generate(cls,source):
        return source


class Param:
    def __init__(self, key, source=None, title='参数', param_type='text'):
        self.key = key
        self.source = source
        self.title = title
        self.param_type = param_type
        generator_cls = __GENERATOR_CLS_REGISTRY__.get(self.param_type)
        if generator_cls:
            self.generator = generator_cls.generate
        else :
            generator_fun = __GENERATOR_FUN_REGISTRY__.get(self.param_type)
            if not generator_fun:
                raise ValueError('未知的参数类型')
            self.generator = generator_fun
        
    def generate_value(self):
        self.value = self.generator(self.source)
        return self.value

if __name__ == "__main__":
    param = Param('p1','value1')
    param.generate_value()
    print(param.value)