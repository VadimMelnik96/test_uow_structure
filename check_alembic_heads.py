import subprocess
import sys


def main() -> None:
    """Главная функция"""
    result = subprocess.run(
        ["poetry", "run", "alembic", "heads"], capture_output=True, text=True, check=False
    )

    output = result.stdout.strip().splitlines()

    if len(output) != 1:
        print(f"Error: only one row was expected, but {len(output)} rows were found.")  # noqa: T201
        sys.exit(1)

    print("Success! Find only one row!")  # noqa: T201
    sys.exit(0)


if __name__ == "__main__":
    main()
