import subprocess


def run_command(command):
    """
    Executes a shell command and returns the output.
    Returns a tuple (success, output_or_error).
    """
    try:
        # shell=True is used to allow complex commands; ensure inputs are sanitized if possible.
        # For this local app, we assume user trust.
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()
    except Exception as e:
        return False, str(e)
