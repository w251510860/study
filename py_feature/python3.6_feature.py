# PEP498 - 字符串插值
from typing import List, Dict

f = 'hello '.format('word')
g = f'hello word'

# PEP 526: 变量注释语法
# PEP 484引入了函数参数的类型注释的标准，又名类型提示
primes: List[int] = []
captain: str  # Note: no initial value!


class StarShip:
    stats: Dict[str, int] = {}


# PEP 515: 数值文字中的下划线
v_int = 1_000_000_000
v_int1 = 1000000000
print('yes') if v_int == v_int else print('no')
