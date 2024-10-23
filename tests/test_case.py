from django.test import TransactionTestCase


class TranslationTestCase(TransactionTestCase):
    """TestCase for Translation."""

    def assertQuerySetEqual(self, *args, **kwargs) -> None:
        if hasattr(super(), "assertQuerySetEqual"):
            super().assertQuerySetEqual(*args, **kwargs)
        else:
            super().assertQuerysetEqual(*args, **kwargs)
