import click
import random
from . import main_commands

bag_upper = [chr(i) for i in range(65, 65+26)]
bag_lower = [chr(i) for i in range(97, 97+26)]
bag_number = "0123456789"
bag_character = "!@#$%^&*-+_:;,.?"

@main_commands.command()
@click.option("--rule", default="Aa1!", help="组合规则 [A][a][1][!]")
@click.option("--length", default=8, help="密码长度")
def passwd(rule, length):
    """
    生成密码
    """
    population = []
    rule = set(rule)
    if 'A' in rule:
        population.extend(bag_upper)
    if 'a' in rule:
        population.extend(bag_lower)
    if '1' in rule:
        population.extend(bag_number)
    if '!' in rule:
        population.extend(bag_character)
    if not population:
        population.extend(bag_upper)
        population.extend(bag_lower)
    pwd = "".join(random.choices(population, k=length))
    print(pwd)
    return pwd