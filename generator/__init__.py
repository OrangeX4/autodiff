import re
from random import randint

class Generator:

    def __init__(self):
        pass

    def generate(self, input: str) -> str:
        '''
        int(a, b): a <= value(int) <= b
        char: 随机大小写字母
        string(a, b): 由 char 组成, a <= length(string) <= b
        '''
        def get_char():
            return chr(randint(97, 122) if randint(0, 1) else randint(65, 90))

        # 将 int(a, b), char, string(a, b) 替换为对应的值
        input = re.sub(r'int\(\s*(\d+)\s*,\s*(\d+)\s*\)', lambda x: str(randint(int(x.group(1)), int(x.group(2)))), input)
        input = re.sub(r'char', lambda x: get_char(), input)
        input = re.sub(r'string\(\s*(\d+)\s*,\s*(\d+)\s*\)', lambda x: ''.join([get_char() for _ in range(randint(int(x.group(1)), int(x.group(2))))]), input)
        return input

def unit_test():
    generator = Generator()
    input = 'int(1,10) int(1, 10) char string( 1 , 3 )'
    print(generator.generate(input))

if __name__ == '__main__':
    unit_test()


