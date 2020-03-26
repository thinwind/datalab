from operator import methodcaller
from faker import Faker
import jsonpath
import requests
import json

_GENERATOR_CLS_REGISTRY = {}
_GENERATOR_FUN_REGISTRY = {}
_FAKER_REGISTRY = {}
_ENGINE_REGISTR = {}

PRODUCT_MODE_MERGE = 'merge'
PRODUCT_MODE_REPLACE = 'replace'


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
        if type_name:
            register_generator_cls(type_name, cls)
        return cls


class BaseGenerator(GeneratorMeta):
    type_name = None

    def __init__(self, source=None, value=None):
        self.value = value

    def add_source(self):
        pass


class IdentityGenerator(BaseGenerator):
    type_name = 'text'

    def generate(self):
        return self.value


class FakerGenerator(BaseGenerator):
    type_name = 'faker'
    default_locale = 'zh_CN'

    def generate(self):
        meta_data = json.loads(self.value, encoding="UTF-8")
        lang_locale = meta_data.get("lang")
        if not lang_locale:
            lang_locale = default_locale
        _faker = get_fakser(lang_locale)
        return methodcaller(meta_data['fun_name'])(_faker)


class JsonPathGenerator(BaseGenerator):
    type_name = 'jsonpath'

    def __init__(self, source=None, value=None):
        self.source = source
        self.value = value

    def generate(self):
        if self.source:
            return jsonpath.jsonpath(self.source, self.value)
        else:
            return self.value

    def add_source(self, source):
        if self.source:
            self.source.update(source)
        else:
            self.source = source


class Param:
    def __init__(self, value=None, param_type='text'):
        self.value = value
        self.param_type = param_type
        self._create_generator()

    def _create_generator(self):
        generator_cls = _GENERATOR_CLS_REGISTRY.get(self.param_type)
        if generator_cls:
            generator = generator_cls.generate
        else:
            generator_fun = _GENERATOR_FUN_REGISTRY.get(self.param_type)
            if not generator_fun:
                raise ValueError('未知的参数类型')
            generator = generator_fun
        self.generator = generator(value=self.value)

    def generate_value(self, source=None):
        if source:
            self.generator.add_source(source)
        self.generated_value = self.generator.generate()
        return self.generated_value

    def add_source(self, source):
        self.generator.add_source(source)

    def __str__(self):
        return "[type]:"+self.param_type+"  [value]:"+self.generator.generate()

    def __repr__(self):
        return "<Param> "+str(self)


def generate_params(param_str, generate_value=True):
    if not param_str:
        return {}
    param_json = json.loads(param_str)
    _params = {}
    if param_json:
        # 初始化入参
        for k, v in param_json:
            param = Param(v.get('value'), v.get('param_type'))
            if generate_value:
                param = param.generate_value()
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


class EngineMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        type_name = class_dict['engine_type']
        if type_name:
            register_engine(type_name, cls)
        return cls


class BaseEngine(metaclass=EngineMeta):
    engine_type = None

    def __init__(self, engine_body):
        self.engine_body = engine_body

    def run(self, input_params):
        pass


class IdentityEngine(BaseEngine):
    engine_type = 'identity'

    def run(self, input_params):
        return input_params


class HttpEngine(BaseEngine):
    engine_type = 'http'

    def run(self, input_params):
        if input_params:
            engine_str = self.engine_body.format(**input_params)
        else:
            engine_str = self.engine_body
        engine_meta = json.loads(engine_str, encoding='UTF-8')
        method = engine_meta['method']
        url = engine_meta['url']
        headers = engine_meta.get('headers')
        data = engine_meta.get('data')
        params = engine_meta.get('params')
        json = engine_meta.get('json')
        proxies = engine_meta.get('proxies')
        timeout = engine_meta.get('timeout', 30)
        add_params = engine_meta.get('add_params')
        if add_params:
            if params:
                params.update(input_params)
            else:
                params = input_params
        return requests.request(method, url, params=params, headers=headers, data=data, json=json,
                                proxies=proxies, timeout=timeout)


class ProductPackage:
    def __init__(self, success=True, product_sn=None, product=None, errmsg=None, errcode=None):
        self.success = success
        self.product_sn = product_sn
        self.product = product
        self.errmsg = errmsg
        self.errcode = errcode


class WorkMachine:
    def __init__(self, input_params_str=None, output_params_str=None,
                 engine_type=None, engine_body=None, product_mode=PRODUCT_MODE_MERGE):
        self.input_params_str = input_params_str
        self.output_params_str = output_params_str
        self.engine_type = engine_type
        self.engine_body = engine_body
        self.product_mode = product_mode

    def run(self,inputs):
        engine_cls = _ENGINE_REGISTR[self.engine_type]
        self.engine = engine_cls(self.engine_body)
        self.input_params = generate_params(self.input_params_str)
        self.output_params = generate_params(self.output_params_str, False)
        self.prepare_engine()
        self.input_params.update(inputs)
        try:
            self.inter_product = self.engine.run(self.input_params)
        finally:
            self.engine.stop()
        self.make_product()

    def make_product(self):
        if self.product_mode == PRODUCT_MODE_MERGE:
            result = self.input_params.update(self.inter_product)
        else:
            result = self.inter_product
        if not self.output_params:
            self.product = result
        else:
            self.product = {k: v.generate_value(
                result) for k, v in self.output_params.items()}

STATUS_FAILED="failed"
STATUS_SUCCESS='success'
STATUS_CANCELLED='cancelled'

class WorkAssemblyLine:
    def __init__(self,input_params_str=None,output_params_str=None,machines=None,workerline=None):
        self.input_params_str = input_params_str
        self.output_params_str = output_params_str
        self.machines = machines
        self.workerline = workerline

    def produce(self):
        self.input_params = generate_params(self.input_params_str)
        self.output_params = generate_params(self.output_params_str, False)
        inter_product = input_params
        for machine in self.machines:
            worker = machine.worker
            model = machine.model
            try:
                worker.run(inter_product)
                model.product = worker.product
                model.save()
                inter_product.update(worker.product)
            except Exception as e:
                self.workerline.status = STATUS_FAILED
                self.workerline.last_machine_id = model.id
                errmsg = str(e)
                self.workerline.product = errmsg
                model.product = errmsg
                model.save()
                self.workerline.save()
                return
        self.workerline.product = inter_product
        self.workerline.last_machine_id = self.machines[-1].id
        self.workerline.save()
