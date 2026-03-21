import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture that provides a FastAPI TestClient for testing endpoints."""
    return TestClient(app)


# Test data constants for validation tests
VALID_EMAILS = [
    "student@example.com",
    "user.name@domain.org",
    "test+tag@gmail.com",
    "simple@test.net"
]

INVALID_EMAILS = [
    "invalid-email",  # no @
    "@domain.com",    # no local part
    "user@",          # no domain
    "user@.com",      # invalid domain
    "user..double@domain.com",  # double dot
    "",               # empty
    " ",              # whitespace only
    "very.long.email.address.that.might.be.too.long@domain.com"  # potentially long
]

ACTIVITY_NAMES_WITH_SPECIAL_CHARS = [
    "Activity with spaces",
    "Activity-with-dashes",
    "Activity_with_underscores",
    "Activity123",  # numbers
    "Activity@symbol",  # @ symbol
    "Activity#hash",  # # symbol
    "Activity%percent",  # % symbol
    "Activity&and",  # & symbol
    "Activity+plus",  # + symbol
    "Activity=equals",  # = symbol
    "Activity?question",  # ? symbol
    "Activity:colon",  # : symbol
    "Activity;semicolon",  # ; symbol
    "Activity,comma",  # , symbol
    "Activity.dot",  # . symbol
    "Activity<less>",  # < >
    "Activity>greater>",  # < >
    "Activity|pipe|",  # | symbol
    "Activity\\backslash",  # \ symbol
    "Activity/forwardslash",  # / symbol
    "Activity\"quote\"",  # " symbol
    "Activity'quote'",  # ' symbol
    "Activity(parens)",  # ( )
    "Activity[brackets]",  # [ ]
    "Activity{braces}",  # { }
    "Activity^caret",  # ^ symbol
    "Activity$ dollar",  # $ symbol
    "Activity!exclamation",  # ! symbol
    "Activity~tilde",  # ~ symbol
    "Activity`backtick`",  # ` symbol
]

EMPTY_ACTIVITY_NAMES = [
    "",
    " ",
    "\t",
    "\n"
]


@pytest.fixture(params=VALID_EMAILS)
def valid_email(request):
    """Parameterized fixture providing valid email addresses."""
    return request.param


@pytest.fixture(params=INVALID_EMAILS)
def invalid_email(request):
    """Parameterized fixture providing invalid email addresses."""
    return request.param


@pytest.fixture(params=ACTIVITY_NAMES_WITH_SPECIAL_CHARS)
def activity_name_with_special_chars(request):
    """Parameterized fixture providing activity names with special characters."""
    return request.param


@pytest.fixture(params=EMPTY_ACTIVITY_NAMES)
def empty_activity_name(request):
    """Parameterized fixture providing empty or whitespace-only activity names."""
    return request.param