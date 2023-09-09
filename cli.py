import click

from skoly.scripts.finalize_schools import finalize
from skoly.scripts.update_programmes import update_programmes
from skoly.scripts.update_schools import update_schools
from skoly.scripts.update_types import update_types


@click.group
def main():
    pass


main.add_command(finalize)
main.add_command(update_programmes)
main.add_command(update_schools)
main.add_command(update_types)

if __name__ == "__main__":
    main()
