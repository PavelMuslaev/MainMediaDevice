import pytest


@pytest.fixture(scope="session", autouse=True)
def print_start_end_session():
    print("\n#--- НАЧАЛО ТЕСТОВОЙ ССЕСИИ ---")
    yield
    print("\n#--- КОНЕЦ ТЕСТОВОЙ ССЕСИИ ---")


@pytest.fixture(scope="function", autouse=True)
def track_test_duration_func():
    import time

    start_time = time.time()
    yield
    result = time.time() - start_time
    print(f"\nТест выполнился: {result:.4f} сек.")


@pytest.fixture(scope="session", autouse=True)
def track_test_duration_session():
    import time

    start_time = time.time()
    yield
    result = time.time() - start_time
    print(f"\nОбщее время выполнения: {result:.4f} сек.")