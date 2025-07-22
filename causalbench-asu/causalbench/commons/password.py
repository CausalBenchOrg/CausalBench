import sys
import getpass


def is_jupyter():
    try:
        from IPython import get_ipython
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True
    except:
        return False


def is_colab():
    try:
        import google.colab
        return True
    except ImportError:
        return False


def prompt_password(prompt='Password: '):
    if sys.stdin.isatty() or is_jupyter() or is_colab():
        return getpass.getpass(prompt)

    else:
        # Emulated or non-interactive environment
        return input(prompt)
