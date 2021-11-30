import os


py_dir, tex_dir = '../../py', '../../tex_BA'
char_count, word_count = 0, 0

def foo(dir_path):

    for i in os.listdir(dir_path):
        file_path = os.path.join(dir_path, i)

        if os.path.isdir(file_path):
            foo(file_path)
            if file_path.endswith('__pycache__') or file_path.endswith('.ipynb_checkpoints'):
                continue
            print(file_path)
        elif os.path.isfile(file_path):
            if not (file_path.endswith('.py') or file_path.endswith('.tex')):
                continue
            print(file_path)
            with open(file_path) as fp:
                content = fp.readlines()
            global char_count
            global word_count
            char_count += len(' '.join(content))
            word_count += len(' '.join(content).split(' '))


for dir_path in [py_dir, tex_dir]:
    foo(dir_path)

print(char_count, word_count)
