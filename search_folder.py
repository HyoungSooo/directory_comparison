import os
from typing import List


class SearchFolder:
    TEST_ROOT_FOLDER_NAME = ''
    REAL_ROOT_FOLDER_NAME = ''
    test_folder_dict = {}
    real_folder_dict = {}
    diff = {'T': [], 'R': [], 'X': []}

    def __file_search(directory: str):
        """주어진 디렉토리의 모든 파일을 순차 탐색합니다."""
        files = set()
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                files.add(file)
        return files

    def __dir_search(directory: str):
        """주어진 디렉토리안에 다른 폴더가 있는지 탐색합니다."""
        for folder in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, folder)):
                yield folder

    @classmethod
    def __insert_differences(cls, directory: List):
        """주어진 디렉토리를 diff 딕셔너리에 저장합니다."""
        while directory:
            node = directory.pop()

            if cls.test_folder_dict.get(node, None):
                path = os.path.join(cls.TEST_ROOT_FOLDER_NAME, node)
                tag = 'T'
                cls.diff[tag].extend(map(lambda x: os.path.join(
                    path, x), cls.test_folder_dict[node]))
            else:
                path = os.path.join(cls.REAL_ROOT_FOLDER_NAME, node)
                tag = 'R'
                cls.diff[tag].extend(map(lambda x: os.path.join(
                    path, x), cls.real_folder_dict[node]))

            cls.diff[tag].append(path)

    def __intersect(set1: set, set2: set):
        """두 set의 교집합을 반환합니다."""
        return set1.intersection(set2)

    def __difference(set1: set, set2: set):
        """두 set의 차집합을 각각 반환합니다."""
        return set1.difference(set2), set2.difference(set1)

    def __wrap_compare_files(real_base: str, test_base: str):
        """filter 함수를 적용하기 위해 최상위 폴더 이름을 인자로 받습니다."""
        def __compare_files(file_path: str):
            """
              두개의 파일을 읽어서 다른 점이 있으면 True를 반환합니다
              같은 방식으로 포맷팅 한 경우에만 유효한 결과를 도출합니다.
            """
            try:
                with open(os.path.join(real_base, file_path), 'r', encoding='utf-8') as file1, open(os.path.join(test_base, file_path), 'r', encoding='utf-8') as file2:
                    content1 = file1.read()
                    content2 = file2.read()

                    if content1 != content2:
                        return True
                return False
            except (IOError, UnicodeDecodeError):
                pass
        return __compare_files

    @classmethod
    def __insert_file_differneces(cls, directory: str, files: List, tag: str, base_path: str):
        while files:
            file = files.pop()
            cls.diff[tag].append(os.path.join(base_path, directory, file))

    @classmethod
    def __file_check(cls, directory: str, files: set):
        """주어진 디렉토리의 파일들을 비교합니다."""
        filter_function = cls.__wrap_compare_files(
            cls.REAL_ROOT_FOLDER_NAME, cls.TEST_ROOT_FOLDER_NAME)

        result = filter(filter_function, map(
            lambda x: os.path.join(directory, x), files))

        cls.diff['X'].extend(
            map(lambda x: os.path.join(cls.REAL_ROOT_FOLDER_NAME, x), result))

    @classmethod
    def __search(cls, directory: str, flag: bool = True):
        """주어진 디렉토리 기준으로 하위 폴더를 모두 탐색합니다."""
        next_dir = cls.__dir_search(directory)

        for dir in next_dir:
            cls.__search(os.path.join(directory, dir), flag)

        changed_directory = "" if directory == cls.TEST_ROOT_FOLDER_NAME or directory == cls.REAL_ROOT_FOLDER_NAME else directory

        if flag:
            changed_directory = changed_directory.replace(
                f'{cls.TEST_ROOT_FOLDER_NAME}\\', '')
            cls.test_folder_dict[changed_directory] = cls.__file_search(
                directory)
        else:
            changed_directory = changed_directory.replace(
                f'{cls.REAL_ROOT_FOLDER_NAME}\\', '')
            cls.real_folder_dict[changed_directory] = cls.__file_search(
                directory)

    @classmethod
    def search(cls, directory: str, flag: bool = True):
        if flag:
            cls.TEST_ROOT_FOLDER_NAME = directory
        else:
            cls.REAL_ROOT_FOLDER_NAME = directory

        cls.__search(directory, flag)

    @classmethod
    def check(cls, test: str, real: str):
        """주어진 디렉토리들의 하위 폴더들을 비교합니다."""
        cls.search(test)
        cls.search(real, False)

        folder_path_intersect = cls.__intersect(
            set(cls.test_folder_dict.keys()), set(cls.real_folder_dict.keys()))

        only_test, only_real = cls.__difference(set(cls.test_folder_dict.keys()),
                                                set(cls.real_folder_dict.keys()))

        cls.__insert_differences(list(only_test.union(only_real)))

        for path in folder_path_intersect:
            file_intersect = cls.__intersect(set(list(cls.test_folder_dict[path])), set(
                list(cls.real_folder_dict[path])))

            only_test_file, only_real_file = cls.__difference(set(list(cls.test_folder_dict[path])), set(
                list(cls.real_folder_dict[path])))

            cls.__insert_file_differneces(
                path, list(only_test_file), 'T', cls.TEST_ROOT_FOLDER_NAME)
            cls.__insert_file_differneces(
                path, list(only_real_file), 'R', cls.REAL_ROOT_FOLDER_NAME)

            cls.__file_check(path, file_intersect)
