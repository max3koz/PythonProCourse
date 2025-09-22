import pytest
from assertpy.assertpy import assert_that

from .age_verifier import AgeVerifier


@pytest.mark.parametrize("age, expected", [
	pytest.param(0, False, id="TC_02_01: age 0, wrong value"),
	pytest.param(10, False, id="TC_02_02: age 10, wrong value"),
	pytest.param(17, False, id="TC_02_03: age 17, wrong value"),
	pytest.param(18, True, id="TC_02_04: age 18, good value"),
	pytest.param(25, True, id="TC_02_05: age 25, good value"),
	pytest.param(120, True, id="TC_01: age 120, unexpected in life value"),
])
def test_is_adult_various_ages(age, expected):
	assert_that(AgeVerifier.is_adult(age) == expected,
	            "Error: something wrong").is_true()


@pytest.mark.skip(reason="The are less 0 — uncorrect value, "
                         "the testcase was skipped!")
def test_is_adult_negative_age():
	assert_that(AgeVerifier.is_adult(-5),
	            "Error: something wrong").is_false()


age = 121


@pytest.mark.skipif(age > 120, reason="Wrong the age value")
def test_is_adult_extreme_age():
	assert_that(AgeVerifier.is_adult(age),
	            "Error: something wrong").is_false()
