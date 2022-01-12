import os
import filecmp
from veeam_tt.main import handling_folder_contents, del_unnecessary_content


def test_handling_folder_contents(temp_folders, folder1, folder2):
    os.mkdir(f"{folder1}/Test1")
    os.mkdir(f"{folder2}/Test2")
    assert filecmp.cmp(f"{folder1}/test.txt", f"{folder2}/test.txt") is True
    with open(f"{folder1}/test.txt", "w") as file_test:
        file_test.write("text")
    assert filecmp.cmp(f"{folder1}/test.txt", f"{folder2}/test.txt") is False
    assert os.listdir(folder1) != os.listdir(folder2)
    handling_folder_contents(folder1, folder2)
    assert filecmp.cmp(f"{folder1}/test.txt", f"{folder2}/test.txt") is True
    assert os.listdir(folder1) == os.listdir(folder2)


def test_del_unnecessary_content(temp_folders, folder1, folder2):
    os.mkdir(f"{folder2}/Test1")
    os.mkdir(f"{folder2}/Test2")
    os.mkdir(f"{folder1}/Test1")
    assert os.listdir(folder1) != os.listdir(folder2)
    del_unnecessary_content(list(set(os.listdir(folder2)) - set(os.listdir(folder1))), folder2)
    assert os.listdir(folder1) == os.listdir(folder2)
