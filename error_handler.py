def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return str(error)
        except TypeError:
            return "Phone number is invalid. The phone number must consist of exactly 10 digits. "
        except IndexError:
            return "The command is bad. Enter a command again."
        except:
            return "Something is worng. Enter a command again."

    return inner