"""Test data shared by all tests: one place to change it."""

# Fake address from example.com, a domain reserved for examples: nothing is ever created
FAKE_EMAIL = "test@example.com"

# Fake password: only typed into forms, never submitted
FAKE_PASSWORD = "NotARealPassword-123"

# Fake weak password: too short and no number, so the sign-up form must reject it
FAKE_WEAK_PASSWORD = "short"
