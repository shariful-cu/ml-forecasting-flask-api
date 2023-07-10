from marshmallow import Schema, fields, ValidationError


class SklearnModelRequestSchema(Schema):
    """ Validate schema of the input payload json data """
    max_wind = fields.Float(required=True)
    min_temp = fields.Float(required=True)
    max_temp = fields.Float(required=True)
    weather = fields.String(required=True)
    prev_week = fields.Float(required=True)
    day_of_week = fields.Float(required=True)


def validate_inputs(input_data):
    """Check prediction inputs against schema."""
    error_msg = None
    schema = SklearnModelRequestSchema()
    try:
        schema.load(input_data)
    except ValidationError:
        error_msg = 'INVALID data/field in payload schema'

    # check constraints of min and max temperatures
    if input_data['min_temp'] < -20.0 or input_data['min_temp'] > 115.0:
        error_msg = 'min_temp should be in the range of -20 to 115 degrees Fahrenheit'
    elif input_data['max_temp'] < -20.0 or input_data['max_temp'] > 115.0:
        error_msg = 'max_temp should be in the range of -20 to 115 degrees Fahrenheit'

    return error_msg
