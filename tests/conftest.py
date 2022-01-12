import os
import pytest
import shutil

@pytest.fixture
def folder1() -> str:
    return "./folder1"

@pytest.fixture
def folder2() -> str:
    return "./folder2"


@pytest.fixture(autouse=True)
def temp_folders(folder1, folder2):
    for i in (folder1, folder2):
        if os.path.isdir(i):
            shutil.rmtree(i, ignore_errors=True)
        os.mkdir(i)
        with open(f"{i}/test.txt", "w") as file_test:
            file_test.write("some_thing")
    yield
    shutil.rmtree(folder1, ignore_errors=True)
    shutil.rmtree(folder2, ignore_errors=True)
