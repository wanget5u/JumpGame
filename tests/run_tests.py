import pytest

exit_code = pytest.main([
    "-v",
    "--tb=short"
])

if exit_code == 0:
    print("✅ Wszystkie testy przeszły!")
else:
    print("❌ Niektóre testy nie przeszły.")
