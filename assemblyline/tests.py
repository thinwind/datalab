from django.test import TestCase
from .components import BaseEngine,IdentityEngine
import json

# Create your tests here.

ips = [
  ['key',{"value":"param_value","title":"参数显示名称","param_type":"text"}],
  ['key',{"value":"param_value","title":"参数显示名称","param_type":"text"}],
  ['key',{"value":"param_value","title":"参数显示名称","param_type":"text"}],
  ['key2',{"value":"param_value2","title":"参数显示名称2","param_type":"text"}],
  ['key3',{"value":"param_value3","title":"参数显示名称3","param_type":"text"}],
]


input_param_str=json.dumps(ips)

ops = [
  ['key0',{"value":"param_value","title":"参数显示名称","param_type":"text"}],
  ['key',{"value":"param_value","title":"参数显示名称","param_type":"text"}],
  ['key',{"value":"param_value","title":"参数显示名称","param_type":"text"}],
  ['key2',{"value":"param_value2","title":"参数显示名称2","param_type":"text"}],
  ['key3',{"value":"param_value3","title":"参数显示名称3","param_type":"text"}],
]

output_param_str=json.dumps(ops)


if __name__ == "__main__":
    engine = IdentityEngine(input_param_str,output_param_str)
    engine.prepare_params()
    print(engine.input_params)
    print(engine.output_params)
