# blog_server

#### 介绍
1.  该博客项目使用的是go+vue+ts语法
2.  mysql数据存储+redis缓存+rabbitMQ+es+fastdfs

#### 版本
python3.8
mysql8.0


## 数据库设计

### 用户权限设计

- **账号表（account）**：记录登录账号信息
- **用户表（user）**：记录用户基本信息和密码
- **权限表（permission）**：记录权限信息
- **角色表（role）**：记录角色信息，即定义权限组
- **用户—角色表（user_role）**：记录每个用户拥有哪些角色信息
- **角色—权限表（role_permission）**：记录每个角色拥有哪些权限信息
- **角色组（role_group）**：解决的是权限的分组，减少了权限的重复分配
- **用户组（user_group）**：解决的是用户的分组，减少了用户的重复授权

###  账号表（account）

在我们的系统中，会有各种各样的登录方式，如手机号、邮箱地址、身份证号码和微信登录等。因此该表**主要是用来记录每一种登录方式的信息，但不包含密码信息**，因为各种登录方式都会使用同一个密码。每一条记录都会关联到唯一的一条用户记录。

### 用户表（user）

主要是用来记录用户的基本信息和密码信息。其中禁用状态（state）主要是在后台管理控制非法用户使用系统；密码加盐（salt）则是用于给每个用户的登录密码加一把唯一的锁，即使公司加密公钥泄露后，也不会导致全部用户的密码泄露。

用户账号表（account）和用户表（user）组合在一起，就完成了用户账号模块的设计。如果还想再细分，则可以将两张表拆为以下三张表：

- **用户信息表（user）**：只存储用户基本信息（不包括密码）
- **账号表（account）**：只存储账号相关信息（如密码、注册来源、注册 IP，但不包括登录账号）
- **登录账号表（login_account）**：用来存储每一种登录方式的信息（不包括密码信息）

当然，如果用户信息的字段太多，则可以适当拆分为多张不同领域的用户信息表，这里不再介绍

### 权限表（permission）

有了用户之后，我们希望不同的用户能操作和查看不同的功能（如页面、菜单和按钮等）。因此需要定义一张表来存储权限相关的信息。包括权限之前还有父子关系，分配了父级后，应该拥有所有的子级权限。同时权限的信息也会分配至前端页面来控制，因此需要提供一个唯一标识（code），有人会问 id 不行吗？当然可以，只是我们的 ID 是自动生成，每个环境都不一样，重新生成后也不一样，因此才单独使用了一个字段来标识。

其实，再加一张 **用户权限表（user_permission）** 即可组成一个用户权限中心了，但这样做是不好的。比如我们设想：有 200 个权限点，1 亿个用户，每个人平均配置 100 个权限，则 user_permission 表将会有 100 亿条记录，而且每当我们新增 1 个权限点时，可能需要添加上亿条记录。简而言之会有以下弊端：

- 中间数据量庞大
- 新增或编辑时，操作数据量的数据量也是非常庞大
- 维护起来也很麻烦

因此，我们会引入一张角色表（role）来解决问题。

### 角色表（role）

为了解决维护起来方便，我们会对权限表中的记录进行分组，将相关的一些权限分配为同一组，称之为角色。角色表的作用是为了将零散的权限进行聚合，然后方便对相关的一组进行统一处理（即小范围批量处理）。该表的增加可谓是大大减少了上述维护困难的问题。

### 用户—角色表（user_role）

该表主要是用来存储每个用户拥有哪些角色。一般情况，每个用户只会有几个角色，因此数据量从 100 亿变成 10 亿或更少。

### 角色 - 权限表（role_permission）

该表则是用来定义每个角色组中有哪些权限。该表的数量则更少（基本都在 1 万条以内）

### 用户组表（user_group）

上述虽然增加了角色表（role）后，把数据量从 100 亿降低至 10 亿，但 10 倍的数据量依然还是很多。而且大部分的用户（主体用户。如学生系统，学生就是主体）都会分配相同的角色组。用户组和角色组的区别：

### 用户组—用户表（user_group_user）

该表用来记录每个用户组下有哪些用户。

### 用户组—角色表（user_group_role）

该表用来记录每个用户组下拥有哪些用户角色。

sqlalchemy模型迁移

步骤：

第一步：安装依赖

```
pip install alembic
```

第二步：初始化  在项目目录下面执行下面命令

```
alembic init alembic
```

生成如下文件夹alembic

![alembic](H:\golang\blog_server\doc\img\alembic.png)

```
alembic/
	versions
		8ccf12...这是迁移时生成的迁移文件
	env.py
	README
	script.py.mako
	
```

修改后的文件如下

```python
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from db.base import Base
from core.config.development_config import settings

target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url")
    # context.configure(
    #     url=url,
    #     target_metadata=target_metadata,
    #     literal_binds=True,
    #     dialect_opts={"paramstyle": "named"},
    # )
    #SQLALCHEMY_DATABASE_URL  这里修改成自己的mysql配置
    context.configure(
        url=settings.SQLALCHEMY_DATABASE_URL, target_metadata=target_metadata,
        literal_binds=True, compare_type=True
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.SQLALCHEMY_DATABASE_URL
    connectable = engine_from_config(
        configuration, prefix="sqlalchemy.", poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

```

settings.py  (SQLALCHEMY_DATABASE_URL)

```
'''
-*- coding: utf-8 -*-
@Author  : zhouys
@Time    : 2021/11/16 23:20
@Software: PyCharm
@File    : development_config.py
'''
"""
开发环境配置
"""
import os

from typing import Union, Optional

from pydantic import AnyHttpUrl, BaseSettings, IPvAnyAddress


class Settings(BaseSettings):
    # 开发模式配置
    DEBUG: bool = True
    # 项目文档
    TITLE: str = "FastAPI+MySQL项目生成"
    DESCRIPTION: str = "更多FastAPI知识，请关注我的个人网站 https://www.charmcode.cn/"
    # 文档地址 默认为docs
    DOCS_URL: str = "/api/docs"
    # 文档关联请求数据接口
    OPENAPI_URL: str = "/api/openapi.json"
    # redoc 文档
    REDOC_URL: Optional[str] = "/api/redoc"

    # token过期时间 分钟
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # 生成token的加密算法
    ALGORITHM: str = "HS256"

    # 生产环境保管好 SECRET_KEY
    SECRET_KEY: str = 'aeq)s(*&(&)()WEQasd8**&^9asda_asdasd*&*&^+_sda'

    # 项目根路径
    BASE_PATH: str = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))

    # 配置你的Mysql环境
    # MYSQL_USERNAME: str = "用户名"
    # MYSQL_PASSWORD: str = "密码"
    # MYSQL_HOST: Union[AnyHttpUrl, IPvAnyAddress] = "IP"
    # MYSQL_PORT: int = 3306
    # MYSQL_DATABASE: str = 'blog'

    # Mysql地址

    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@" \
                              f"{MYSQL_HOST}/{MYSQL_DATABASE}?charset=utf8mb4"

    # redis配置
    REDIS_HOST: str = "ip"
    REDIS_PASSWORD: str = "密码"
    REDIS_DB: int = 1
    REDIS_PORT: int = 6379
    REDIS_URL: str = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}?encoding=utf-8"
    REDIS_TIMEOUT: int = 5  # redis连接超时时间

    CASBIN_MODEL_PATH: str = "./resource/rbac_model.conf"


settings = Settings()
```







#### 框架fastapi

```python
pip install fastapi
pip install uvicorn[standard]
```

```python
'''
-*- coding: utf-8 -*-
@Author  : zhouys
@Time    : 2021/11/20 16:00
@Software: PyCharm
@File    : models.py

用户表
'''

from db.base_class import Base, gen_uuid
from sqlalchemy import Column, Boolean, Integer, String, VARCHAR, BIGINT, \
    ForeignKey


# 用户表
class User(Base):
    __tablename__ = "user"
    state = Column(Integer, default=False, comment="用户状态:0=正常,1=禁用",
                   server_default="0")
    name = Column(VARCHAR(64), unique=True, nullable=False,
                  comment="用户名")
    head_img_url = Column(VARCHAR(255), comment="用户图像地址")
    mobile = Column(VARCHAR(11), unique=True, index=True, nullable=True,
                    comment="手机号")
    salt = Column(VARCHAR(64), comment="用户密码加盐")
    hashed_password = Column(VARCHAR(128), nullable=False, comment="密码")
    creator = Column(VARCHAR(36), nullable=False, comment="创建人")
    editor = Column(VARCHAR(36), nullable=False, comment="修改人")
    __table_args__ = ({'comment': '用户表'})


# 权限表
class Permission(Base):
    __tablename__ = "permission"
    parent_id = Column(VARCHAR(32), default=gen_uuid, unique=True,
                       comment="所属父级权限ID")
    code = Column(VARCHAR(32), comment="权限唯一CODE代码")
    name = Column(VARCHAR(32), comment="权限名称")
    intro = Column(VARCHAR(32), comment="权限介绍")
    category = Column(VARCHAR(32), comment="权限类别")
    uri = Column(VARCHAR(255), comment="URL规则")
    creator = Column(VARCHAR(32), comment="创建人")
    editor = Column(VARCHAR(32), comment="修改人")
    __table_args__ = ({'comment': '权限表'})


# 角色表
class Role(Base):
    __tablename__ = "role"
    parent_id = Column(VARCHAR(32), default=gen_uuid, comment="所属父级角色ID")
    code = Column(VARCHAR(32), comment="角色唯一CODE代码")
    name = Column(VARCHAR(32), comment="角色名称")
    intro = Column(VARCHAR(255), comment="角色介绍")
    creator = Column(VARCHAR(32), comment="创建人")
    editor = Column(VARCHAR(32), comment="修改人")
    __table_args__ = ({'comment': '角色表'})


# 用户组
class UserGroup(Base):
    __tablename__ = "user_group"
    parent_id = Column(VARCHAR(32), comment="所属父级用户组ID")
    name = Column(VARCHAR(32), comment="用户组名称")
    code = Column(VARCHAR(32), comment="用户组CODE唯一代码")
    intro = Column(VARCHAR(32), comment="用户组介绍")
    creator = Column(VARCHAR(32), comment="创建人")
    editor = Column(VARCHAR(32), comment="修改人")
    __table_args__ = ({'comment': '用户组'})


# 用户账号表
class Account(Base):
    __tablename__ = "account"
    user_id = Column(Integer, ForeignKey("user.id"))  # 与用户表进行关联
    open_code = Column(VARCHAR(255), unique=True, nullable=True,
                       comment="登录账号，如手机号 微信号等")
    category = Column(Integer, comment="账号类别", nullable=True)
    creator = Column(VARCHAR(36), nullable=False, comment="创建人")
    editor = Column(VARCHAR(36), nullable=False, comment="修改人")
    __table_args__ = ({'comment': '账号表'})


# 用户角色关联表
class UserRole(Base):
    __tablename__ = "user_role"
    user = Column(Integer, ForeignKey("user.id"), comment="用户ID")
    role = Column(Integer, ForeignKey("role.id"), comment="角色ID")
    creator = Column(VARCHAR(32), comment="创建人")
    editor = Column(VARCHAR(32), comment="修改人")
    __table_args__ = ({'comment': '用户角色关联表'})

# 用户组角色表
class UserGroupRole(Base):
    __tablename__ = "user_group_role"
    user_group = Column(Integer, ForeignKey("user_group.id"), comment="用户组ID")
    role = Column(Integer, ForeignKey("role.id"), comment="角色ID")
    creator = Column(VARCHAR(32), comment="创建人")
    editor = Column(VARCHAR(32), comment="修改人")
    __table_args__ = ({'comment': ' 用户组—角色表'})

# 用户组用户表
class UserGroupUser(Base):
    __tablename__ = "user_group_user"
    user_group = Column(Integer, ForeignKey("user_group.id"),
                        comment="用户组ID")
    role = Column(Integer, ForeignKey("role.id"), comment="角色ID")
    creator = Column(VARCHAR(32), comment="创建人")
    editor = Column(VARCHAR(32), comment="修改人")
    __table_args__ = ({'comment': ' 用户组—用户表'})


# 角色权限关联表
class RolePermission(Base):
    __tablename__ = "role_permission"
    role = Column(Integer, ForeignKey("role.id"), comment="角色权限管理ID")
    permission = Column(Integer, ForeignKey("permission.id"), comment="角色权限管理")
    creator = Column(VARCHAR(32), comment="创建人")
    editor = Column(VARCHAR(32), comment="修改人")
    __table_args__ = ({'comment': '角色权限关联表'})


```



使用casbin进行权限管理

第一步安装依赖

```
pip install casbin
pip install casbin_sqlalchemy_adapter
```

例子：

```
'''
-*- coding: utf-8 -*-
@Author  : zhouys
@Time    : 2021/11/17 23:20
@Software: PyCharm
@File    : test_casbin.py
'''
import os
from unittest import TestCase

import casbin
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

from casbin_sqlalchemy_adapter import Adapter
from casbin_sqlalchemy_adapter import Base
from casbin_sqlalchemy_adapter import CasbinRule
from casbin_sqlalchemy_adapter.adapter import Filter


def get_fixture(path):
    dir_path = os.path.split(os.path.realpath(__file__))[0] + "/"
    return os.path.abspath(dir_path + path)


def get_enforcer():
        engine = create_engine('mysql+pymysql://用户名:密码@ip:3306/数据库?charset=utf8mb4')
        adapter = Adapter(engine, CustomRule)

    session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    s = session()
    s.query(CasbinRule).delete()
    s.add(CasbinRule(ptype="p", v0="alice", v1="data1", v2="read"))
    s.add(CasbinRule(ptype="p", v0="bob", v1="data2", v2="write"))
    s.add(CasbinRule(ptype="p", v0="data2_admin", v1="data2", v2="read"))
    s.add(CasbinRule(ptype="p", v0="data2_admin", v1="data2", v2="write"))
    s.add(CasbinRule(ptype="g", v0="alice", v1="data2_admin"))
    s.commit()
    s.close()

    return casbin.Enforcer(get_fixture("model.conf"), adapter)


class TestConfig(TestCase):
    def test_custom_db_class(self):
        class CustomRule(Base):
            __tablename__ = "casbin_rule2"

            id = Column(Integer, primary_key=True)
            ptype = Column(String(255))
            v0 = Column(String(255))
            v1 = Column(String(255))
            v2 = Column(String(255))
            v3 = Column(String(255))
            v4 = Column(String(255))
            v5 = Column(String(255))
            not_exist = Column(String(255))

        engine = create_engine('mysql+pymysql://用户名:密码@ip:3306/数据库?charset=utf8mb4')
        adapter = Adapter(engine, CustomRule)

        session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        s = session()
        s.add(CustomRule(not_exist="NotNone"))
        s.commit()
        self.assertEqual(s.query(CustomRule).all()[0].not_exist, "NotNone")

    def test_enforcer_basic(self):
        e = get_enforcer()

        self.assertTrue(e.enforce("alice", "data1", "read"))
        self.assertFalse(e.enforce("alice", "data1", "write"))
        self.assertFalse(e.enforce("bob", "data1", "read"))
        self.assertFalse(e.enforce("bob", "data1", "write"))
        self.assertTrue(e.enforce("bob", "data2", "write"))
        self.assertFalse(e.enforce("bob", "data2", "read"))
        self.assertTrue(e.enforce("alice", "data2", "read"))
        self.assertTrue(e.enforce("alice", "data2", "write"))

    def test_add_policy(self):
        e = get_enforcer()

        self.assertFalse(e.enforce("eve", "data3", "read"))
        res = e.add_policies((("eve", "data3", "read"), ("eve", "data4", "read")))
        self.assertTrue(res)
        self.assertTrue(e.enforce("eve", "data3", "read"))
        self.assertTrue(e.enforce("eve", "data4", "read"))

    def test_add_policies(self):
        e = get_enforcer()

        self.assertFalse(e.enforce("eve", "data3", "read"))
        res = e.add_permission_for_user("eve", "data3", "read")
        self.assertTrue(res)
        self.assertTrue(e.enforce("eve", "data3", "read"))

    def test_save_policy(self):
        e = get_enforcer()
        self.assertFalse(e.enforce("alice", "data4", "read"))

        model = e.get_model()
        model.clear_policy()

        model.add_policy("p", "p", ["alice", "data4", "read"])

        adapter = e.get_adapter()
        adapter.save_policy(model)
        self.assertTrue(e.enforce("alice", "data4", "read"))

    def test_remove_policy(self):
        e = get_enforcer()

        self.assertFalse(e.enforce("alice", "data5", "read"))
        e.add_permission_for_user("alice", "data5", "read")
        self.assertTrue(e.enforce("alice", "data5", "read"))
        e.delete_permission_for_user("alice", "data5", "read")
        self.assertFalse(e.enforce("alice", "data5", "read"))

    def test_remove_policies(self):
        e = get_enforcer()

        self.assertFalse(e.enforce("alice", "data5", "read"))
        self.assertFalse(e.enforce("alice", "data6", "read"))
        e.add_policies((("alice", "data5", "read"), ("alice", "data6", "read")))
        self.assertTrue(e.enforce("alice", "data5", "read"))
        self.assertTrue(e.enforce("alice", "data6", "read"))
        e.remove_policies((("alice", "data5", "read"), ("alice", "data6", "read")))
        self.assertFalse(e.enforce("alice", "data5", "read"))
        self.assertFalse(e.enforce("alice", "data6", "read"))

    def test_remove_filtered_policy(self):
        e = get_enforcer()

        self.assertTrue(e.enforce("alice", "data1", "read"))
        e.remove_filtered_policy(1, "data1")
        self.assertFalse(e.enforce("alice", "data1", "read"))

        self.assertTrue(e.enforce("bob", "data2", "write"))
        self.assertTrue(e.enforce("alice", "data2", "read"))
        self.assertTrue(e.enforce("alice", "data2", "write"))

        e.remove_filtered_policy(1, "data2", "read")

        self.assertTrue(e.enforce("bob", "data2", "write"))
        self.assertFalse(e.enforce("alice", "data2", "read"))
        self.assertTrue(e.enforce("alice", "data2", "write"))

        e.remove_filtered_policy(2, "write")

        self.assertFalse(e.enforce("bob", "data2", "write"))
        self.assertFalse(e.enforce("alice", "data2", "write"))

        # e.add_permission_for_user('alice', 'data6', 'delete')
        # e.add_permission_for_user('bob', 'data6', 'delete')
        # e.add_permission_for_user('eve', 'data6', 'delete')
        # self.assertTrue(e.enforce('alice', 'data6', 'delete'))
        # self.assertTrue(e.enforce('bob', 'data6', 'delete'))
        # self.assertTrue(e.enforce('eve', 'data6', 'delete'))
        # e.remove_filtered_policy(0, 'alice', None, 'delete')
        # self.assertFalse(e.enforce('alice', 'data6', 'delete'))
        # e.remove_filtered_policy(0, None, None, 'delete')
        # self.assertFalse(e.enforce('bob', 'data6', 'delete'))
        # self.assertFalse(e.enforce('eve', 'data6', 'delete'))

    def test_str(self):
        rule = CasbinRule(ptype="p", v0="alice", v1="data1", v2="read")
        self.assertEqual(str(rule), "p, alice, data1, read")
        rule = CasbinRule(ptype="p", v0="bob", v1="data2", v2="write")
        self.assertEqual(str(rule), "p, bob, data2, write")
        rule = CasbinRule(ptype="p", v0="data2_admin", v1="data2", v2="read")
        self.assertEqual(str(rule), "p, data2_admin, data2, read")
        rule = CasbinRule(ptype="p", v0="data2_admin", v1="data2", v2="write")
        self.assertEqual(str(rule), "p, data2_admin, data2, write")
        rule = CasbinRule(ptype="g", v0="alice", v1="data2_admin")
        self.assertEqual(str(rule), "g, alice, data2_admin")

    def test_repr(self):
        rule = CasbinRule(ptype="p", v0="alice", v1="data1", v2="read")
        self.assertEqual(repr(rule), '<CasbinRule None: "p, alice, data1, read">')
        engine = create_engine("sqlite://")

        session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        s = session()

        s.add(rule)
        s.commit()
        self.assertRegex(repr(rule), r'<CasbinRule \d+: "p, alice, data1, read">')
        s.close()

    def test_filtered_policy(self):
        e = get_enforcer()
        filter = Filter()

        filter.ptype = ["p"]
        e.load_filtered_policy(filter)
        self.assertTrue(e.enforce("alice", "data1", "read"))
        self.assertFalse(e.enforce("alice", "data1", "write"))
        self.assertFalse(e.enforce("alice", "data2", "read"))
        self.assertFalse(e.enforce("alice", "data2", "write"))
        self.assertFalse(e.enforce("bob", "data1", "read"))
        self.assertFalse(e.enforce("bob", "data1", "write"))
        self.assertFalse(e.enforce("bob", "data2", "read"))
        self.assertTrue(e.enforce("bob", "data2", "write"))

        filter.ptype = []
        filter.v0 = ["alice"]
        e.load_filtered_policy(filter)
        self.assertTrue(e.enforce("alice", "data1", "read"))
        self.assertFalse(e.enforce("alice", "data1", "write"))
        self.assertFalse(e.enforce("alice", "data2", "read"))
        self.assertFalse(e.enforce("alice", "data2", "write"))
        self.assertFalse(e.enforce("bob", "data1", "read"))
        self.assertFalse(e.enforce("bob", "data1", "write"))
        self.assertFalse(e.enforce("bob", "data2", "read"))
        self.assertFalse(e.enforce("bob", "data2", "write"))
        self.assertFalse(e.enforce("data2_admin", "data2", "read"))
        self.assertFalse(e.enforce("data2_admin", "data2", "write"))

        filter.v0 = ["bob"]
        e.load_filtered_policy(filter)
        self.assertFalse(e.enforce("alice", "data1", "read"))
        self.assertFalse(e.enforce("alice", "data1", "write"))
        self.assertFalse(e.enforce("alice", "data2", "read"))
        self.assertFalse(e.enforce("alice", "data2", "write"))
        self.assertFalse(e.enforce("bob", "data1", "read"))
        self.assertFalse(e.enforce("bob", "data1", "write"))
        self.assertFalse(e.enforce("bob", "data2", "read"))
        self.assertTrue(e.enforce("bob", "data2", "write"))
        self.assertFalse(e.enforce("data2_admin", "data2", "read"))
        self.assertFalse(e.enforce("data2_admin", "data2", "write"))

        filter.v0 = ["data2_admin"]
        e.load_filtered_policy(filter)
        self.assertTrue(e.enforce("data2_admin", "data2", "read"))
        self.assertTrue(e.enforce("data2_admin", "data2", "read"))
        self.assertFalse(e.enforce("alice", "data1", "read"))
        self.assertFalse(e.enforce("alice", "data1", "write"))
        self.assertFalse(e.enforce("alice", "data2", "read"))
        self.assertFalse(e.enforce("alice", "data2", "write"))
        self.assertFalse(e.enforce("bob", "data1", "read"))
        self.assertFalse(e.enforce("bob", "data1", "write"))
        self.assertFalse(e.enforce("bob", "data2", "read"))
        self.assertFalse(e.enforce("bob", "data2", "write"))

        filter.v0 = ["alice", "bob"]
        e.load_filtered_policy(filter)
        self.assertTrue(e.enforce("alice", "data1", "read"))
        self.assertFalse(e.enforce("alice", "data1", "write"))
        self.assertFalse(e.enforce("alice", "data2", "read"))
        self.assertFalse(e.enforce("alice", "data2", "write"))
        self.assertFalse(e.enforce("bob", "data1", "read"))
        self.assertFalse(e.enforce("bob", "data1", "write"))
        self.assertFalse(e.enforce("bob", "data2", "read"))
        self.assertTrue(e.enforce("bob", "data2", "write"))
        self.assertFalse(e.enforce("data2_admin", "data2", "read"))
        self.assertFalse(e.enforce("data2_admin", "data2", "write"))

        filter.v0 = []
        filter.v1 = ["data1"]
        e.load_filtered_policy(filter)
        self.assertTrue(e.enforce("alice", "data1", "read"))
        self.assertFalse(e.enforce("alice", "data1", "write"))
        self.assertFalse(e.enforce("alice", "data2", "read"))
        self.assertFalse(e.enforce("alice", "data2", "write"))
        self.assertFalse(e.enforce("bob", "data1", "read"))
        self.assertFalse(e.enforce("bob", "data1", "write"))
        self.assertFalse(e.enforce("bob", "data2", "read"))
        self.assertFalse(e.enforce("bob", "data2", "write"))
        self.assertFalse(e.enforce("data2_admin", "data2", "read"))
        self.assertFalse(e.enforce("data2_admin", "data2", "write"))

        filter.v1 = ["data2"]
        e.load_filtered_policy(filter)
        self.assertFalse(e.enforce("alice", "data1", "read"))
        self.assertFalse(e.enforce("alice", "data1", "write"))
        self.assertFalse(e.enforce("alice", "data2", "read"))
        self.assertFalse(e.enforce("alice", "data2", "write"))
        self.assertFalse(e.enforce("bob", "data1", "read"))
        self.assertFalse(e.enforce("bob", "data1", "write"))
        self.assertFalse(e.enforce("bob", "data2", "read"))
        self.assertTrue(e.enforce("bob", "data2", "write"))
        self.assertTrue(e.enforce("data2_admin", "data2", "read"))
        self.assertTrue(e.enforce("data2_admin", "data2", "write"))

        filter.v1 = []
        filter.v2 = ["read"]
        e.load_filtered_policy(filter)
        self.assertTrue(e.enforce("alice", "data1", "read"))
        self.assertFalse(e.enforce("alice", "data1", "write"))
        self.assertFalse(e.enforce("alice", "data2", "read"))
        self.assertFalse(e.enforce("alice", "data2", "write"))
        self.assertFalse(e.enforce("bob", "data1", "read"))
        self.assertFalse(e.enforce("bob", "data1", "write"))
        self.assertFalse(e.enforce("bob", "data2", "read"))
        self.assertFalse(e.enforce("bob", "data2", "write"))
        self.assertTrue(e.enforce("data2_admin", "data2", "read"))
        self.assertFalse(e.enforce("data2_admin", "data2", "write"))

        filter.v2 = ["write"]
        e.load_filtered_policy(filter)
        self.assertFalse(e.enforce("alice", "data1", "read"))
        self.assertFalse(e.enforce("alice", "data1", "write"))
        self.assertFalse(e.enforce("alice", "data2", "read"))
        self.assertFalse(e.enforce("alice", "data2", "write"))
        self.assertFalse(e.enforce("bob", "data1", "read"))
        self.assertFalse(e.enforce("bob", "data1", "write"))
        self.assertFalse(e.enforce("bob", "data2", "read"))
        self.assertTrue(e.enforce("bob", "data2", "write"))
        self.assertFalse(e.enforce("data2_admin", "data2", "read"))
        self.assertTrue(e.enforce("data2_admin", "data2", "write"))

    def test_update_policy(self):
        e = get_enforcer()
        example_p = ["mike", "cookie", "eat"]

        self.assertTrue(e.enforce("alice", "data1", "read"))
        e.update_policy(["alice", "data1", "read"], ["alice", "data1", "no_read"])
        self.assertFalse(e.enforce("alice", "data1", "read"))

        self.assertFalse(e.enforce("bob", "data1", "read"))
        e.add_policy(example_p)
        e.update_policy(example_p, ["bob", "data1", "read"])
        self.assertTrue(e.enforce("bob", "data1", "read"))

        self.assertFalse(e.enforce("bob", "data1", "write"))
        e.update_policy(["bob", "data1", "read"], ["bob", "data1", "write"])
        self.assertTrue(e.enforce("bob", "data1", "write"))

        self.assertTrue(e.enforce("bob", "data2", "write"))
        e.update_policy(["bob", "data2", "write"], ["bob", "data2", "read"])
        self.assertFalse(e.enforce("bob", "data2", "write"))

        self.assertTrue(e.enforce("bob", "data2", "read"))
        e.update_policy(["bob", "data2", "read"], ["carl", "data2", "write"])
        self.assertFalse(e.enforce("bob", "data2", "write"))

        self.assertTrue(e.enforce("carl", "data2", "write"))
        e.update_policy(["carl", "data2", "write"], ["carl", "data2", "no_write"])
        self.assertFalse(e.enforce("bob", "data2", "write"))

    def test_update_policies(self):
        e = get_enforcer()

        old_rule_0 = ["alice", "data1", "read"]
        old_rule_1 = ["bob", "data2", "write"]
        old_rule_2 = ["data2_admin", "data2", "read"]
        old_rule_3 = ["data2_admin", "data2", "write"]

        new_rule_0 = ["alice", "data_test", "read"]
        new_rule_1 = ["bob", "data_test", "write"]
        new_rule_2 = ["data2_admin", "data_test", "read"]
        new_rule_3 = ["data2_admin", "data_test", "write"]

        old_rules = [old_rule_0, old_rule_1, old_rule_2, old_rule_3]
        new_rules = [new_rule_0, new_rule_1, new_rule_2, new_rule_3]

        e.update_policies(old_rules, new_rules)

        self.assertFalse(e.enforce("alice", "data1", "read"))
        self.assertTrue(e.enforce("alice", "data_test", "read"))

        self.assertFalse(e.enforce("bob", "data2", "write"))
        self.assertTrue(e.enforce("bob", "data_test", "write"))

        self.assertFalse(e.enforce("data2_admin", "data2", "read"))
        self.assertTrue(e.enforce("data2_admin", "data_test", "read"))

        self.assertFalse(e.enforce("data2_admin", "data2", "write"))
        self.assertTrue(e.enforce("data2_admin", "data_test", "write"))

if __name__ == '__main__':
    test = TestConfig()
    test.test_add_policy()
```

