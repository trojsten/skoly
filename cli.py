import click

from skoly.scripts.finalize_schools import finalize
from skoly.scripts.update_programmes import update_programmes


@click.group
def main():
    pass


main.add_command(finalize)
main.add_command(update_programmes)

if __name__ == '__main__':
    main()
