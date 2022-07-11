python中使用casbin进行权限管理
安装 
```python
pip install casbin
```
配合数据库进行使用
安装 
```python
pip install casbin_sqlalchemy_adapter
```

demo
```
import casbin_sqlalchemy_adapter
import casbin

adapter = casbin_sqlalchemy_adapter.Adapter('sqlite:///test.db')

e = casbin.Enforcer('path/to/model.conf', adapter, True)

sub = "alice"  # the user that wants to access a resource.
obj = "data1"  # the resource that is going to be accessed.
act = "read"  # the operation that the user performs on the resource.

if e.enforce(sub, obj, act):
    # permit alice to read data1casbin_sqlalchemy_adapter
    pass
else:
    # deny the request, show an error
    pass

```