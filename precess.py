import argparse
import os
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def read_data(path):
    # Read text file from path
    # with open(path, 'r') as file:
    #     text = file.readlines()
    # return text
    lines = []
    with open(path, 'r') as file:
        for line in tqdm(file):
            # delete . , ! ? and so on
            line = line.replace(',', '')
            line = line.replace('!', '')
            line = line.replace('?', '')
            line = line.replace('.', '')
            line = line.replace(';', '')
            line = line.replace(':', '')
            line = line.replace('(', '')
            line = line.replace(')', '')
            line = line.replace('[', '')
            line = line.replace(']', '')
            line = line.replace('{', '')
            line = line.replace('}', '')
            line = line.replace('"', '')
            line = line.replace('\'', '')
            line = line.replace('�', '')
            lines.append(line)
    return lines
    

    
def get_frequency(text):
    word_frequency = {}
    for line in text:
        words = line.strip().split()
        for word in words:
            # 将单词转换为小写，以避免大小写的差异影响统计结果
            word = word.lower()
            
            # 统计单词出现的频率
            if word in word_frequency:
                word_frequency[word] += 1
            else:
                word_frequency[word] = 1
    return word_frequency
        

def write_data(path, word_frequency, opt):
    print('begin write')
    
    # # Write word frequency to path
    # with open(path, 'w') as file:
    #     for word, frequency in word_frequency.items():
    #         file.write('{} {}\n'.format(word, frequency))
    
    # sort the frequency and output them
    print('sort the frequency and output them')
    sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
    print(sorted_word_frequency[:10])
    # calculate the sum of frequency
    sum_frequency = 0
    word_count = 0
    total_length = 0
    length_number = np.zeros(50)
    # for word, frequency in sorted_word_frequency:
    #     sum_frequency += frequency
    #     total_length += len(word) * frequency
    #     word_count += 1
    #     length_number[len(word)] += frequency
    # average_length = total_length / word_count
    # use tqdm
    for word, frequency in tqdm(sorted_word_frequency):
        sum_frequency += frequency
        total_length += len(word) * frequency
        word_count += 1
        length_number[len(word)] += frequency
    average_length = total_length / sum_frequency
    # plot and save the length distribution with histogram
    plt.bar(range(30), length_number[:30])
    plt.savefig(opt.unique_name + '_length_distribution.png')
    plt.close()
    # plot and save the word frequency with histogram
    plt.bar(range(100), [frequency for word, frequency in sorted_word_frequency[:100]])
    plt.savefig(opt.unique_name + '_word_frequency.png')
    plt.close()
    
    
    # output sorted word frequency to path
    with open(path, 'w') as file:
        # output the sum of frequency
        file.write('sum_frequency: {}\n'.format(sum_frequency))
        file.write('word_count: {}\n'.format(word_count))
        file.write('average_length: {}\n'.format(average_length))
        # output the length distribution
        file.write('length distribution:\n')
        for i in range(50):
            file.write('{} {}\n'.format(i, length_number[i]))
        for word, frequency in sorted_word_frequency:
            file.write('{} {}\n'.format(word, frequency))
 

def main(opt):
    # Read text file from path
    opt.data_path = os.path.join('corpus', opt.unique_name + '.txt')
    opt.output_path = opt.unique_name + '_output.txt'
    text = read_data(opt.data_path)
    # text = prepocess(text)
    
    # Get word frequency
    word_frequency = get_frequency(text)
    
    # Write word frequency to path
    write_data(opt.output_path, word_frequency, opt)
    
    return 

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Preprocess data')
    parser.add_argument('--unique_name', type=str, default='dl', help='dl or hp')
    parser.add_argument('--data_path', type=str, default='corpus/dl.txt', help='data directory')
    parser.add_argument('--output_path', type=str, default='dl_output.txt', help='output directory')
    opt = parser.parse_args()
    
    
    main(opt)
    opt.unique_name = 'hp'
    main(opt)