from django.test import TestCase

# Create your tests here.
research_content = "test"
test = lambda c: c if len(c) > 0 else ""
print(test(research_content))