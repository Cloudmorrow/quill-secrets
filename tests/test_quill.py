"""Secrets' tests: the real vaults backend and gate, on this machine.

Secrets has no code, and never will: nothing of a Quill's code or an
assistant's reaches a secret through it. These hold what the manifest promises.
"""

import pytest

from cloudmorrow.quill.testing import Harness


@pytest.fixture()
def q():
    with Harness(".") as harness:
        yield harness


def test_a_secret_is_hidden_in_a_list_and_there_when_asked_for(q):
    made = q.seed("secret", key="API_KEY", value="s3cret", vault="default", environment="local")
    listed = q.list("secret")
    assert [s["key"] for s in listed] == ["API_KEY"]
    assert listed[0].get("value") is None
    assert q.get("secret", made.id)["value"] == "s3cret"


def test_secrets_are_ones_own(q):
    q.seed("secret", key="API_KEY", value="s3cret", vault="default", environment="local")
    assert q.as_user("sam").list("secret") == []
