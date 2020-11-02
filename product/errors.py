import logging

logger = logging.getLogger(__name__)


# TODO : find a way the drf serializer takes a schema
def format_serializer_errors(errors):
    """
    formats the default serializer errors in the format we use:
    {
      "errorList": [
        {
          "key": "rating_fraction", #this is the actual key name
          "errorMessage": "rating_fraction - This field is required.",
          "cause": "rating_fraction - This field is required."
        },
        {
          "key": "quizsession", #this is the actual key name
          "errorMessage": "quizsession - This field is required.",
          "cause": "quizsession - This field is required."
        }
      ]
    }
    Another thing that the method is expecting is a errors instance that looks like:
    {
        "cause":[
            "x"
        ],
        "errorMessage":[
            "y"
        ]
    }
    This case can happen when the code uses:
    raise ValidationError({"cause":"x", "errorMessage":"y"})
    1. This usage implies that a field mapping errors has been provided, however we
    are exploiting it to show our own custom format.
    2. The coercion to an array happens due to rest_framework.exceptions._force_text_recursive
    3. Ideally a custom extension of ValidationError should be written, that handles this entire method's work
    4. The only drawback of using the above dict format is that it ignores all other validations, and
    simply raises the given dictionary directly (check here rest_framework.fields.Field.run_validators)
    comment extracted from rest_framework.fields.Field.run_validators:
    # If the validation error contains a mapping of fields to
    # errors then simply raise it immediately rather than
    # attempting to accumulate a list of errors.
    :param errors:
    :return:
    """
    # PS: non_field_errors key is configurable:
    # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
    if "cause" in errors and "error_message" in errors:
        return {
            "error_list": [{
                "key": "non_field_errors",
                "cause": errors["cause"][0],
                "error_message": errors["error_message"][0]
            }],
            "errors_map": {
                "non_field_errors": errors["cause"]
            }
        }

    error_list = []
    for key in errors:
        # errors[key] of [0] because 1 field can return multiple validation errors
        # only using the first one
        flattened_string = key + " - " + errors[key][0]
        error_item = {
            "key": key,
            "cause": flattened_string,
            "error_message": "Something went wrong for which you need to contact UpGrad support. Thank you for your patience."
        }
        error_list.append(error_item)
    return {"error_list": error_list, "errors_map": errors}


class BaseYodaException(Exception):
    cause = None
    error_message = "Something went wrong for which you need to contact upGrad support. Thank you for your patience."
    status = 500

    def __init__(self, message, code=None, params=None):
        super().__init__(message, code, params)
        if isinstance(message, dict):
            self.cause = message.get("cause")
            self.error_message = message.get("error_message")
            status = message.get("status")
            if status:
                self.status = status
        else:
            self.cause = str(message)


class CustomValidationError(BaseYodaException):
    logger.debug("In CustomValidationError")
    status = 400


class UnauthorizedError(BaseYodaException):
    logger.debug("In UnauthorizedError")
    status = 401


class AuthenticationError(BaseYodaException):
    logger.debug("In AuthenticationError")
    status = 403


class PermissionDeniedError(BaseYodaException):
    logger.debug("In PermissionDeniedError")
    status = 403


class NotFoundError(BaseYodaException):
    logger.debug("In NotFoundError")
    status = 404