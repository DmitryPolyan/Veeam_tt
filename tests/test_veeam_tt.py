import os
import filecmp
from veeam_tt.main import (
    handling_folder_contents,
    del_unnecessary_content,
    update_repl_content,
    append_new_content_int_repl
)


def test_handling_folder_contents(folder1, folder2):
    os.mkdir(f"{folder1}/Test1")
    os.mkdir(f"{folder2}/Test2")
    assert filecmp.cmp(f"{folder1}/test.txt", f"{folder2}/test.txt") is True, "Файлы разные"
    with open(f"{folder2}/test.txt", "w") as file_test:
        file_test.write("text")
    assert filecmp.cmp(f"{folder1}/test.txt", f"{folder2}/test.txt") is False, "Файлы одинаковые"
    assert os.listdir(folder1) != os.listdir(folder2), "Список файлов в папках одинаковый"
    handling_folder_contents(folder1, folder2)
    assert filecmp.cmp(f"{folder1}/test.txt", f"{folder2}/test.txt") is True, "Файлы разные"
    assert os.listdir(folder1) == os.listdir(folder2), "Список файлов в папках разный"


def test_del_unnecessary_content(folder1, folder2):
    os.mkdir(f"{folder2}/Test1")
    os.mkdir(f"{folder2}/Test2")
    os.mkdir(f"{folder1}/Test1")
    assert os.listdir(folder1) != os.listdir(folder2), "Список файлов в папках одинаковый"
    del_unnecessary_content(list(set(os.listdir(folder2)) - set(os.listdir(folder1))), folder2)
    assert os.listdir(folder1) == os.listdir(folder2), "Список файлов в папках разный"


def test_update_repl_content(folder1, folder2):
    assert filecmp.cmp(f"{folder1}/test.txt", f"{folder2}/test.txt") is True, "Файлы разные"
    with open(f"{folder1}/test.txt", "w") as file_test:
        file_test.write("text")
    assert filecmp.cmp(f"{folder1}/test.txt", f"{folder2}/test.txt") is False, "Файлы одинаковые"
    update_repl_content(folder1, folder2, "test.txt")
    assert filecmp.cmp(f"{folder1}/test.txt", f"{folder2}/test.txt") is True, "Файлы разные"
    with open(f"{folder2}/test.txt", "r") as file_test:
        text = file_test.read()
    assert text == "text", "Тексты в файлах не совпадают"


def test_append_new_content_int_repl(folder1, folder2):
    os.mkdir(f"{folder1}/Test1")
    with open(f"{folder1}/Test1/test.txt", "w") as file_test:
        file_test.write("text")
    os.mkdir(f"{folder1}/Test2")
    assert os.listdir(folder1) != os.listdir(folder2), "Список файлов в папках одинаковый"
    for i in os.listdir(folder1):
        append_new_content_int_repl(folder1, i, folder2)
    assert os.listdir(folder1) == os.listdir(folder2), "Список файлов в папках разный"
    assert filecmp.cmp(f"{folder1}/Test1/test.txt", f"{folder2}/Test1/test.txt") is True, "Файлы разные"

