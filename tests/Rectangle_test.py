import pytest
from Rectangle import Rectangle

# For functional testing, we can use the following fixtures:
@pytest.fixture
def rect():
  return Rectangle(3, 4)

def test_area(rect:Rectangle):
  assert rect.area() == 12

# alternative to fixture, just instantiate the Rectangle, but this won't be reusable if it gets mutated
rect_not_fixture = Rectangle(3, 4)

def test_perimeter():
  assert rect_not_fixture.perimeter() == 14

# Alternative to functional testing above, we can use the following class-based testing:
class TestRectangle:
    def setup_method(self):
        self.rect = Rectangle(0, 4)
    
    def teardown_method(self):
        pass

    def test_zero_area(self):
        assert self.rect.area() == 0
        print(self.rect.width)

    def test_zero_perimeter(self):
        assert self.rect.perimeter() == 8
