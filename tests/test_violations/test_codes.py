from collections import Counter

import pytest

from wemake_python_styleguide.compat.constants import PY311


def test_all_unique_violation_codes(all_violations):
    """Ensures that all violations have unique violation codes."""
    codes = [int(violation.code) for violation in all_violations]
    assert len(set(codes)) == len(all_violations)


@pytest.mark.skipif(not PY311, reason='@final has runtime effect since 3.11')
def test_all_violations_are_final(all_violations):  # pragma: >=3.11 cover
    """Ensures that all violations are final."""
    for violation_type in all_violations:
        assert getattr(violation_type, '__final__', False), violation_type


def test_all_unique_violation_messages(all_violations):
    """Ensures that all violations have unique violation messages."""
    messages = Counter(
        [violation.error_template for violation in all_violations],
    )
    for message, count in messages.items():
        assert count == 1, message


def test_all_violations_correct_numbers(all_module_violations):
    """Ensures that all violations has correct violation code numbers."""
    assert len(all_module_violations) == 7

    for index, module in enumerate(all_module_violations.keys()):
        code_number = index * 100
        for violation_class in all_module_violations[module]:
            assert (
                code_number <= violation_class.code <= code_number + 100 - 1
            ), violation_class.__qualname__


def test_violations_start_zero(all_module_violations):
    """Ensures that all violations start at zero."""
    for index, module in enumerate(all_module_violations.keys()):
        starting_code = min(
            violation_class.code
            for violation_class in all_module_violations[module]
        )
        assert starting_code == index * 100


def test_no_holes(all_violation_codes):
    """Ensures that there are no off-by-one errors."""
    for module_codes in all_violation_codes.values():
        previous_code = None
        for code in sorted(module_codes.keys()):
            if previous_code is not None:
                diff = code - previous_code
                assert diff == 1 or diff > 2, module_codes[code].__qualname__
            previous_code = code


def test_violation_code_is_int(all_violations):
    """Ensures that all violations have an integer code."""
    for violation in all_violations:
        assert isinstance(violation.code, int)
