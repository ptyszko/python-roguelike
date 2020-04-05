def generate_level(width, height) -> list:
    assert width > 2 and height > 2
    bound = '#' * width
    middle = '#' + '.' * (width-2) + '#'
    return [bound] + [middle]*(height-2) + [bound]

if __name__ == "__main__":
    print(generate_level(15,10))