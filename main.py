'''
-*- coding: utf-8 -*-
@Author  : zhouys
@Time    : 2021/11/15 23:14
@Software: PyCharm
@File    : main.py
'''


from core.server import create_app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    # 输出所有的路由
    for route in app.routes:
        if hasattr(route, "methods"):
            print({'path': route.__dict__['path'], 'name': route.__dict__['name'], 'methods': route.__dict__['methods']})

    uvicorn.run(app='main:app', host="127.0.0.1", port=8010, reload=True, debug=True)