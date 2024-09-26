import os
import re
import javalang
import random

repos_directory = 'projects'
corpus = []

def remove_comments(code):
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    code = re.sub(r'//.*?\n', '', code)
    return code

def tokenize_code(code):
    tokens = []
    try:
        tokenizer = javalang.tokenizer.tokenize(code)
        tokens = [token.value for token in tokenizer]
    except javalang.tokenizer.LexerError as e:
        print(f"Error tokenizing code: {e}")
    return tokens

def extract_methods_from_file(java_file_path):
    methods = []
    with open(java_file_path, 'r', encoding='utf-8') as file:
        code = file.read()
        clean_code = remove_comments(code)
        try:
            tree = javalang.parse.parse(clean_code)
            for _, node in tree.filter(javalang.tree.MethodDeclaration):
                method_name = node.name
                if node.body is not None:
                    start_pos = node.position.line - 1
                    end_pos = max(node.body[-1].position.line, start_pos + 1)
                    method_code_lines = clean_code.splitlines()[start_pos:end_pos]
                    method_code = ' '.join(method_code_lines)
                    tokenized_body = tokenize_code(method_code)
                    method_body = ' '.join(tokenized_body)
                else:
                    method_body = "No method body"
                methods.append(f'{method_name}: {method_body}')
        except javalang.parser.JavaSyntaxError:
            print(f"Skipping {java_file_path}, syntax error detected.")
        except Exception as e:
            print(f"Error processing {java_file_path}: {e}")
    return methods

def parse_java_projects(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.java'):
                java_file_path = os.path.join(subdir, file)
                methods = extract_methods_from_file(java_file_path)
                corpus.extend(methods)

parse_java_projects(repos_directory)

# shuffling the corpus
random.shuffle(corpus)

# 70% training, 10% validation, and 20% testing
total_size = len(corpus)
train_size = int(0.7 * total_size)
val_size = int(0.1 * total_size)
test_size = total_size - train_size - val_size

train_data = corpus[:train_size]
val_data = corpus[train_size:train_size + val_size]
test_data = corpus[train_size + val_size:]

# Save the splits into files
with open('java_methods_train.txt', 'w', encoding='utf-8') as train_file:
    for method in train_data:
        train_file.write(method + '\n')

with open('java_methods_val.txt', 'w', encoding='utf-8') as val_file:
    for method in val_data:
        val_file.write(method + '\n')

with open('java_methods_test.txt', 'w', encoding='utf-8') as test_file:
    for method in test_data:
        test_file.write(method + '\n')

print(f"Total methods: {total_size}")
print(f"Training data: {train_size} methods")
print(f"Validation data: {val_size} methods")
print(f"Testing data: {test_size} methods")

