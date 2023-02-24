import os


def main():
    python_file_paths = []
    for path, subdirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                python_file_paths.append(os.path.join(path, file))
    with open('python_file_paths.txt', 'w') as f:
        f.write('\n'.join(python_file_paths))


if __name__ == '__main__':
    main()
