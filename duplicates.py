import collections
import argparse
import os


def get_all_files(dirpath):
    files_dict = collections.defaultdict(set)
    file_info = collections.namedtuple(
        'FileInfo',
        ('file_name', 'file_size'),
    )
    for dir_name, subdirs_list, files_list in os.walk(dirpath):
        for file_name in files_list:
            try:
                file_path = os.path.join(dir_name, file_name)
                file_abs_path = os.path.abspath(file_path)
                file_size = os.path.getsize(file_path)
                files_dict[file_info(file_name, file_size)].add(file_abs_path)
            except FileNotFoundError:
                pass
    return files_dict


def get_duplicates(files_dict):
    duplicates_dict = {}
    for file_info, file_path in files_dict.items():
        if len(files_dict[file_info]) > 1:
            duplicates_dict[file_info] = file_path
    return duplicates_dict


def print_duplicates(duplicate_dict):
    if duplicate_dict:
        print('\nDuplicates found:')
        for file_info in duplicate_dict:
            for path in duplicate_dict[file_info]:
                print(path)
            print('-'*20)
    else:
        print('No duplicates were found.')


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'dir_path',
        help='directory where search will be effected',
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = get_arguments()
    if not os.path.exists(args.dir_path):
        print('Incorrect dir path')
        exit()
    all_files_dict = get_all_files(args.dir_path)
    duplicates_dict = get_duplicates(all_files_dict)
    print_duplicates(duplicates_dict)
