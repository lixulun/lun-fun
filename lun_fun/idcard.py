import click
import unittest
from . import main_commands
from .misc import try_import

def _validate(idn):
    """
    idn - ['int' * 18]  idn[-1] in [0~10]
    """
    ratios = [2**i%11 for i in range(18)][:0:-1]
    mapping = [1, 0, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    m = sum([x*y for x, y in zip(idn[:-1], ratios)]) % 11
    return idn[-1] == mapping[m]

def str2list(id_number):
    id_number = list(id_number.strip())
    if id_number[-1] in ('x', 'X', 'Ⅹ'):
        id_number[-1] = 10
    return list(map(int, id_number))

@main_commands.command()
@click.argument('id_number')
def idcard(id_number):
    """验证身份证号"""
    if len(id_number) != 18:
        raise ValueError("输入的身份证号码不是18位")
    result = _validate(str2list(id_number))
    print(result)

class IdCardTest(unittest.TestCase):

    def test_function(self):
        self.assertTrue(_validate(str2list('110101199003070978')))
        self.assertTrue(_validate(str2list('140110200007066666')))
        self.assertTrue(_validate(str2list('513436200002218976')))
        self.assertTrue(_validate(str2list('513436200002219012')))
        self.assertTrue(_validate(str2list('220102198403173383')))
        self.assertTrue(_validate(str2list('220102198403171409')))
        self.assertTrue(_validate(str2list('430102199710111231')))
        self.assertTrue(_validate(str2list('430102199710116876')))
        self.assertTrue(_validate(str2list('14011020000706402X')))
        self.assertTrue(_validate(str2list('110101199003072391')))
        self.assertFalse(_validate(str2list('110101199003072291')))
        self.assertFalse(_validate(str2list('220002198403173383')))
        self.assertFalse(_validate(str2list('111101199003071970')))
        self.assertFalse(_validate(str2list('140105200203075018')))
        self.assertFalse(_validate(str2list('140105200203078924')))
        self.assertFalse(_validate(str2list('140105300203071357')))
        self.assertFalse(_validate(str2list('310101199909136423')))
        self.assertFalse(_validate(str2list('310101199909233767')))
        self.assertFalse(_validate(str2list('310101199909030564')))
        self.assertFalse(_validate(str2list('22010230030307517X')))
