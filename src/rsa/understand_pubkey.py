import base64

file_content = open('key.pub', 'r').read()
print(file_content)

content = base64.b64decode(file_content.split(' ')[1]).encode("hex")
print(content)

string_length = int(content[:8], 16)
print(string_length)

string_end_pos = 8 + string_length * 2
string = content[8: string_end_pos].decode('hex')
print(string)

exp_length = int(content[string_end_pos: string_end_pos + 8], 16)
print(exp_length)

exp_end_pos = string_end_pos + 8 + exp_length * 2
exp = int(content[string_end_pos + 8: exp_end_pos], 16)
print(exp)

n_length = int(content[exp_end_pos: exp_end_pos + 8], 16)
print(n_length)

n = int(content[exp_end_pos + 8: exp_end_pos + 8 + 2 * n_length], 16)
print(n)
