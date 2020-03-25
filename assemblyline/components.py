import json
from operator import methodcaller
from faker import Faker

_GENERATOR_CLS_REGISTRY = {}
_GENERATOR_FUN_REGISTRY = {}
_FAKER_REGISTRY = {}
_ENGINE_REGISTR = {}


def register_generator_cls(type_name, cls):
    _GENERATOR_CLS_REGISTRY[type_name] = cls


def register_generator_fun(type_name, func):
    _GENERATOR_FUN_REGISTRY[type_name] = func


def register_engine(engine_type, engine_cls):
    _ENGINE_REGISTR[engine_type] = engine_cls


def get_fakser(lang_locale):
    _faker = _FAKER_REGISTRY.get(lang_locale)
    if not _faker:
        _faker = Faker([lang_locale])
        _FAKER_REGISTRY[lang_locale] = _faker
    return _faker


def indentity_text_generator(source):
    return source


register_generator_fun('text', indentity_text_generator)


class GeneratorMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        type_name = class_dict.get('type_name')
        if not type_name:
            type_name = name
        register_generator_cls(type_name, cls)
        return cls


class IdentityGenerator(metaclass=GeneratorMeta):
    type_name = 'text'

    @classmethod
    def generate(cls, source):
        return source


class FakerGenerator(metaclass=GeneratorMeta):
    type_name = 'faker'
    default_locale = 'zh_CN'

    @classmethod
    def generate(cls, source):
        meta_data = json.loads(source, encoding="UTF-8")
        lang_locale = meta_data.get("lang")
        if not lang_locale:
            lang_locale = cls.default_locale
        _faker = get_fakser(lang_locale)
        return methodcaller(meta_data['fun_name'])(_faker)


class Param:
    def __init__(self, key, source=None, title='参数', param_type='text'):
        self.key = key
        self.source = source
        self.title = title
        self.param_type = param_type
        generator_cls = _GENERATOR_CLS_REGISTRY.get(self.param_type)
        if generator_cls:
            self.generator = generator_cls.generate
        else:
            generator_fun = _GENERATOR_FUN_REGISTRY.get(self.param_type)
            if not generator_fun:
                raise ValueError('未知的参数类型')
            self.generator = generator_fun
        self.generate_value()

    def generate_value(self):
        self.value = self.generator(self.source)
        return self.value

    def __str__(self):
        return "[type]:"+self.param_type+"  [value]:"+self.value

    def __repr__(self):
        return "<Param> "+str(self)


class EngineMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        type_name = class_dict['engine_type']
        if type_name:
            register_engine(type_name, cls)
        return cls


def generate_params(self, param_str):
    param_json = json.loads(param_str)
    _params = {}
    if param_json:
        # 初始化入参
        for k, v in param_json:
            param = Param(k, v.get('value'), v.get(
                'title'), v.get('param_type'))
            if k in _params:
                params = _params[k]
                if isinstance(params, list):
                    params.append(param)
                else:
                    params = [params]
                    params.append(param)
                    _params[k] = params
            else:
                _params[k] = param
    return _params


class BaseEngine(metaclass=EngineMeta):
    engine_type = None


class IdentityEngine(BaseEngine):
    engine_type = 'identity'
    pass

PRODUCT_MODE_MERGE = 'merge'
PRODUCT_MODE_REPLACE = 'replace'

class ProductPackage:
    def __init__(self,success=True,product_sn=None,product=None,errmsg=None,errcode=None):
        self.success = success
        self.product_sn = product_sn
        self.product = product
        self.errmsg = errmsg
        self.errcode = errcode

class WorkMachine:
    def __init__(self, input_params_str=None, output_params_str=None, meta_data=None):
        self.input_params_str = input_params_str
        self.output_params_str = output_params_str
        self.meta_data = meta_data
        
    def prepare_engine(self):
        if not self.meta_data:
            #没有元数据，默认直接输出
            self.engine = _ENGINE_REGISTR['identity']()
        else:
            engine_cls = _ENGINE_REGISTR[self.meta_data['engine_type']]
            self.engine = engine_cls(self.meta_data.get('engine_body'))
    
    def run(self):
        self.input_params = generate_params(self.input_params_str)
        self.output_params = generate_params(self.output_params_str)
        self.prepare_engine()
        try:
            self.inter_product = self.engine.run(self.input_params)
        except Exception as e:
            return ProductPackage(False,errmsg=str(e))
        finally:
            self.engine.stop()
        
        
        
        