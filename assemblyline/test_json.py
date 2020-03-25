import json

def as_complex(dct):
    print(dct)
    if '__complex__' in dct:
        return complex(dct['real'],dct['imag'])
    return dct
res = json.loads('{"__complex1__": false, "real": 1, "imag": 2}',object_hook=as_complex)
print(res)

dct = {'key':"值"}
print(json.dumps(dct,ensure_ascii=False))

param_list=[]
param_list.append(('a','a'))
param_list.append(('a','a'))
param_list.append(('a','a'))
param_list.append(('a','a'))

if __name__ == "__main__":
    for k,v in param_list:
        print(k,v)