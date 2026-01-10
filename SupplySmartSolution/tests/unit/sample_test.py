import pytest
from models.discount import Discount
from schemas.contracts import DiscountInput
from pydantic import ValidationError
@pytest.fixture
def model():
    return Discount()


@pytest.fixture
def val_input():
    return DiscountInput()

def expected_value_test(model, input):
    pred = model.predict(input)
    assert pred == 20

def predict_test(model, input):
    pred = model.predict(input)
    assert isinstance(pred, float)

def error_test():
    with pytest.raises(ValidationError):
        DiscountInput(data="hello")

def type_test():
    input_obj = DiscountInput(data=50)
    assert model.predict(input_obj) == 20