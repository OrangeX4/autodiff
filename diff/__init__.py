from subprocess import PIPE, Popen

exec_path = r'../input/4A/84822639.exe'
# open exec_path and set input = '2' and get output
p = Popen(exec_path, stdin=PIPE, stdout=PIPE, stderr=PIPE)
# output, err = p.communicate(b'2')
# print(output)
rc = p.returncode
print(rc)
output, err = p.communicate(b'2')
rc = p.returncode
print(rc)
