from time import perf_counter

import pytest


@pytest.fixture(scope="session", autouse=True)
def print_start_end_session():
    print("\n#--- TEST SESSION START ---")
    yield
    print("\n#--- TEST SESSION END ---")


@pytest.fixture(scope="function", autouse=True)
def track_test_duration_func(request):
    start_time = perf_counter()
    yield
    result = perf_counter() - start_time
    print(f"\nTest duration [{request.node.nodeid}]: {result:.4f} sec.")


@pytest.fixture(scope="session", autouse=True)
def track_test_duration_session():
    start_time = perf_counter()
    yield
    result = perf_counter() - start_time
    print(f"\nTotal test duration: {result:.4f} sec.")
