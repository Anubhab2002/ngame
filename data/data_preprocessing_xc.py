import random
import string

train_file_path = 'train_queries_ddc.txt'
test_file_path = 'test_queries_ddc.txt'

def remove_punctuation(text):
    # print("before: ", text)
    # Remove punctuations using string.punctuation
    translator = str.maketrans('', '', string.punctuation+'’')
    text = text.translate(translator)
    text = ' '.join(text.split())
    # print("after: ", text)
    return text

def split_sentence(sentence):
    sentence = remove_punctuation(sentence).strip()
    print(2, sentence)
    
    if len(sentence) == 1:
        return f'{sentence}<SEP>{sentence}'
    # Randomly choose the split index
    if len(sentence.strip()) <= 6 :
        result = f'{sentence[0]}<SEP>{sentence[1:]}'
        # print(result)
        return result
    
    split_index = random.randint(3, len(sentence) - 3)

    # Split the sentence at the chosen index
    segment1 = sentence[:split_index]
    segment2 = sentence[split_index:]

    # Join the segments with a tab separator
    result = f"{segment1}<SEP>{segment2}"
    print(3, result)
    return result

lines_train = []
lines_test = []

for line in open(train_file_path, 'r'):
    line = line.strip()
    if len(line.strip()) <= 1:
        continue
    line = split_sentence(line)
    lines_train.append(line)
    
for line in open(test_file_path, 'r'):
    line = line.strip()
    if len(line.strip()) <= 1:
        continue
    line = split_sentence(line)
    lines_test.append(line)

def get_label_ids(lines, next_label_id=0):
    label_id_mapping = {}

    for line in lines:
        line = line.strip()
        if len(line.strip()) <= 1:
            continue
        print("line: ", line, len(line))
        # line = split_sentence(line)
        _, labels = line.strip().split('<SEP>')
        for label in labels.split(','):
            if label not in label_id_mapping:
                label_id_mapping[label] = next_label_id
                next_label_id += 1

    return label_id_mapping


def convert_to_xc_format(lines, output_file, label_id_mapping):
    with open(output_file, 'w') as output_file:
        for line in lines:
            line = line.strip()
            if len(line.strip()) <= 1:
                continue
            # line = split_sentence(line)
            input_data, label = line.strip().split('<SEP>')
            print(input_data, label)
            label_id = f"{label_id_mapping[label]}:1.0"
            output_file.write(f"{label_id}\n")

# write a function to take input_file as input and return only the input not the lable
def get_input_file(lines, output_file):
    with open(output_file, 'w') as output_file:
        for line in lines:
            line = line.strip()
            if len(line.strip()) <= 1:
                continue
            # line = split_sentence(line)
            input_data, _ = line.strip().split('<SEP>')
            output_file.write(f"{input_data}\n")

def write_labels_to_file(lines_train, lines_test):
    with open('lbl.raw.txt', 'w') as file:
        for label in lines_train:
            x = label.split('<SEP>')[1]
            print(x)
            file.write(f'{x}\n')
        for label in lines_test:
            x = label.split('<SEP>')[1]
            print(x)
            file.write(f'{x}\n')

trn_x_y_file_path = 'trn_X_Y.txt'
tst_x_y_file_path = 'tst_X_Y.txt'
trn_x_file_path = 'trn.raw.txt'
tst_x_file_path = 'tst.raw.txt'

# Obtain label IDs
label_id_mapping = get_label_ids(lines_train)
label_id_mapping.update(get_label_ids(lines_test, len(label_id_mapping)))

# Convert train.txt to trn_X_Y.txt
convert_to_xc_format(lines_train, trn_x_y_file_path, label_id_mapping)

# Convert test.txt to tst_X_Y.txt
convert_to_xc_format(lines_test, tst_x_y_file_path, label_id_mapping)

# get input only files 
get_input_file(lines_train, trn_x_file_path)
get_input_file(lines_test, tst_x_file_path)

# get raw labels file
write_labels_to_file(lines_train, lines_test)