django + Graphql demo
---
#### 基本配置

settings.py
```python
INSTALLED_APPS = [
    # ...
    'graphene_django'
]
GRAPHENE = {
    'SCHEMA': 'django_graphql.schema.schema'
}
```
迁移数据库
```bash
python manage.py migrate
```
创建超级用户
```bash
python manage.py createsuperuser
```
运行
```bash
python manage.py runserver 0.0.0.0:8080
```
在浏览器里搜索 127.0.0.1:8080/graphql/
在页面内输入graphql查询语句
```graphql
{
  users {
    id
    username
    email
    dateJoined
  }
}
```
右边框里显示结果
```graphql
{
  "data": {
    "users": [
      {
        "id": "1",
        "username": "***",
        "email": "********@qq.ocm",
        "dateJoined": "2019-04-08T10:59:00.250081+00:00"
      }
    ]
  }
}
```