import click
import random
import math
from . import main_commands

bag_upper = [chr(i) for i in range(65, 65+26)]
bag_lower = [chr(i) for i in range(97, 97+26)]
bag_number = "0123456789"
bag_character = "!@#$%^&*-+_:;,.?"

prop_A = 3
prop_a = 4
prop_number = 2
prop_character = 1

@main_commands.command()
@click.option("--rule", default="Aa1!", help="组合规则 [A][a][1][!]")
@click.option("--length", default=8, help="密码长度")
@click.option("--quantity", default=1, help="数量")
def passwd(rule, length, quantity):
    """
    生成密码
    """
    for _ in range(quantity):
        print(generate(rule, length))

def generate(rule, length):
    # proportion based on
    prop_rule = 0
    # distribution in rules
    dis = [0, 0, 0, 0]
    # generate a bundle of 'prop_rule' numbers per round
    rounds = 1
    # array of generated characters. Mod prop_rule equals 0
    array = []

    if 'A' in rule:
        dis[0] = prop_A
        prop_rule += prop_A
    if 'a' in rule:
        dis[1] = prop_a
        prop_rule += prop_a
    if '1' in rule:
        dis[2] = prop_number
        prop_rule += prop_number
    if '!' in rule:
        dis[3] = prop_character
        prop_rule += prop_character
    
    rounds = math.ceil(length / prop_rule)
    
    for _ in range(rounds):
        d = dis[:]
        while sum(d) > 0:
            for i in range(len(d)):
                if d[i] <= 0:
                    continue
                if i == 0:
                    array.append(random.choice(bag_upper))
                elif i == 1:
                    array.append(random.choice(bag_lower))
                elif i == 2:
                    array.append(random.choice(bag_number))
                else:
                    array.append(random.choice(bag_character))
                d[i] -= 1

    array = array[:length]
    random.shuffle(array)
    return ''.join(array)
