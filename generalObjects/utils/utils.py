from pandas import DataFrame
from pydentic import validator,BaseModel

class GoogleTrendsResultDictModel(BaseModel):
    top: object
    rising: object

    @validator('top', 'rising', pre=True, each_item=False)
    def validate_dataframe(cls, value) -> DataFrame:
        if not isinstance(value, DataFrame):
            raise ValueError(f"Value is not a DataFrame. Received type: {type(value)}")
        return value
