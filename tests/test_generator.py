from generator import Generator

def test_generate_from_txt():
    input = 'int(1,10) int(1, 10) char string( 1 , 3 )'
    assert len(Generator.generate_from_txt(input).split()) == 4

    input = 'int(1,  2)'
    assert Generator.generate_from_txt(input) == '1' or Generator.generate_from_txt(input) == '2'

    input = 'int(1,1) int(2, 2)'
    assert Generator.generate_from_txt(input) == '1 2'

    input = 'int(1,1) int(2,2) int(3 ,3)'
    assert Generator.generate_from_txt(input) == '1 2 3'

    input = 'string(1,10)'
    assert 1 <= len(Generator.generate_from_txt(input)) <= 10

    input = 'string(1,   10)'
    assert Generator.generate_from_txt(input).isalpha()

    input = 'char'
    assert Generator.generate_from_txt(input) in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    input = 'string(1,1)'
    assert Generator.generate_from_txt(input) in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    input = 'string(1,1) char string(1,1)'
    assert all([i in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' for i in Generator.generate_from_txt(input).split()])

    input = 'int(1,1)int(2,2)int(3,3)'
    assert Generator.generate_from_txt(input) == '123'
