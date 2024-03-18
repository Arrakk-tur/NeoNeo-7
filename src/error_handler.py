red = "\033[91m"
reset = "\033[0m"


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:

            return f"{red}{str(error)}{reset}"
        except TypeError as t_e:

            return f"{red}{str(t_e)}{reset}"
        except IndexError:
            return f"{red}The command is bad. Enter a command again.{reset}\n"
        except:
            return f"{red}Something is wrong. Enter a command again.{reset}\n"

    return inner
