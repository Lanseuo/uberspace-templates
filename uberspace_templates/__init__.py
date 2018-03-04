import click

from uberspace_templates import templates


@click.group()
def cli():
    pass


@cli.command()
@click.argument("template_name")
@click.argument("name")
def init(template_name, name):
    beautified_name = name.replace(" ", "").replace(".", "").replace(",", "").lower()
    if name != beautified_name:
        beautified_name = input("Name (" + beautified_name + "): ") or beautified_name

    if template_name == "flask":
        templates.flask(beautified_name)
    elif template_name == "website":
        templates.website(beautified_name)
    elif template_name == "vuejs":
        templates.vuejs(beautified_name)
    else:
        click.echo("Did not find " + template_name)
