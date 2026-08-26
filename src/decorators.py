from config import ERRORS

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            error_msg = str(e)
            if error_msg == ERRORS["invalid_command"]:
                return ERRORS["invalid_command"]
            if any(key in error_msg for key in [
                "Invalid date format",
                "Phone number must contain",
                "Invalid email format",
                "Address cannot be empty",
                "Name cannot be empty",
                "Title cannot be empty",
                "Content cannot be empty",
                "Tag cannot be empty",
                "Phone ",
                "not found",
                "Days argument"
            ]):
                return error_msg
            return ERRORS["missing_args"]
        except KeyError:
            return ERRORS["contact_not_found"]
        except IndexError:
            return ERRORS["missing_args"]

    return inner