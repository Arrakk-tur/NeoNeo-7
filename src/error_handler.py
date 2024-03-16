def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return str(error)
        except TypeError as t_e:
            return str(t_e)
        except IndexError:
            return "The command is bad. Enter a command again."
        except:
            return "Something is wrong. Enter a command again."

    return inner
