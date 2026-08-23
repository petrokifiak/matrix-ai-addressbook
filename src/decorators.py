from config import ERRORS

def input_error(func):
    """
    Декоратор для обробки помилок користувацького вводу (IndexError, ValueError, KeyError).
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            error_msg = str(e)
            if error_msg == ERRORS["invalid_command"]:
                return ERRORS["invalid_command"]
            if error_msg:
                return error_msg
            return ERRORS["missing_args"]
        except KeyError:
            return ERRORS["contact_not_found"]
        except IndexError:
            return ERRORS["missing_args"]
    return inner
