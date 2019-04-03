测试celery和Signal
---
- 安装依赖包(部分包在本程序是无用的，其他demo会用到)
```bash
aiocache                0.10.0     
aiofiles                0.4.0      
aiohttp                 3.5.4      
amqp                    2.4.2      
apipkg                  1.5        
appdirs                 1.4.3      
asn1crypto              0.24.0     
aspy.yaml               1.2.0      
astroid                 2.2.5      
async-generator         1.10       
async-timeout           3.0.1      
asynctest               0.12.2     
atomicwrites            1.3.0      
attrs                   19.1.0     
billiard                3.5.0.5    
cached-property         1.5.1      
celery                  4.2.1      
certifi                 2019.3.9   
cffi                    1.12.2     
cfgv                    1.6.0      
chardet                 3.0.4      
coverage                4.4.2      
crypto                  1.4.1      
cryptography            2.6.1      
Cython                  0.26.1     
defusedxml              0.5.0      
Django                  1.11.16    
django-celery-beat      1.1.1      
django-extensions       1.9.8      
django-querysetsequence 0.10       
django-redis            4.8.0      
djangorestframework     3.8.2      
docutils                0.14       
DotAgent                1.0        
execnet                 1.6.0      
fakeredis               0.9.0      
Geohash                 1.0        
httptools               0.0.13     
identify                1.4.1      
idna                    2.6        
idna-ssl                1.1.0      
isodate                 0.6.0      
isort                   4.3.16     
Kivy                    1.11.0.dev0
Kivy-Garden             0.1.4      
kombu                   4.4.0      
lazy-object-proxy       1.3.1      
lxml                    4.3.3      
M2Crypto                0.32.0     
mccabe                  0.6.1      
more-itertools          7.0.0      
multidict               4.5.2      
mysqlclient             1.3.13     
Naked                   0.1.31     
nodeenv                 1.3.3      
numpy                   1.14.3     
pandas                  0.23.0     
Pillow                  5.1.0      
pip                     19.0.3     
pluggy                  0.9.0      
pre-commit              1.11.1     
psycopg2-binary         2.7.5      
py                      1.8.0      
pyasn1                  0.4.5      
pycparser               2.19       
pycryptodome            3.8.0      
pycryptodomex           3.8.0      
pyDes                   2.0.1      
Pygments                2.3.1      
pylint                  2.1.1      
pymongo                 3.6.0      
pyOpenSSL               17.5.0     
pytest                  4.4.0      
pytest-django           3.1.2      
pytest-forked           1.0.2      
pytest-sanic            0.1.13     
pytest-xdist            1.22.0     
python-dateutil         2.7.3      
python-geohash          0.8.5      
python-json-logger      0.1.8      
python-Levenshtein      0.12.0     
pytz                    2018.4     
PyYAML                  5.1        
redis                   3.2.1      
requests                2.18.4     
requests-toolbelt       0.9.1      
retrying                1.3.3      
rsa                     3.4.2      
sanic                   0.7.0      
setuptools              39.0.1     
shellescape             3.4.1      
shortuuid               0.5.0      
six                     1.12.0     
splunk-handler          2.0.7      
SQLAlchemy              1.2.7      
toml                    0.10.0     
typed-ast               1.3.1      
typing                  3.6.6      
typing-extensions       3.7.2      
ujson                   1.35       
urllib3                 1.22       
uvloop                  0.12.2     
uWSGI                   2.0.15     
vine                    1.3.0      
virtualenv              16.4.3     
websockets              7.0        
wrapt                   1.11.1     
xlwt                    1.3.0      
yarl                    1.3.0      
zeep                    2.5.0
```
- 启动django 
```bash
python manage runserver 127.0.0.1:9090
```
- 打开网页,访问 http://127.0.0.1:9090/index/
- 打开网页,访问 http://127.0.0.1:9090/signature/
- 查看terminal
```bash
我已经做完了工作.现在我发送一个信号出去,给那些指定的接收器.
我在2019-04-03 01:42:11时间收到来自<function create_signal at 0x10745a7b8>的信号,请求url为/signature/
[03/Apr/2019 01:42:11] "GET /signature/ HTTP/1.1" 200 6
```

