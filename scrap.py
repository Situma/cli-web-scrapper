import requests
from bs4 import BeautifulSoup as bsoup
import click


@click.command()
@click.option('--save', '-s',
              prompt='Do you want to save the scrapped url (y/n)',
              default='n',
              type=click.Choice(['y', 'n'],
                                case_sensitive=True))
@click.option('--url', '-u', prompt=True,
              help='Url e.g. http://google.com')
@click.option('--tag', '-t',
              help='HTML tags e.g. a, div, p',
              prompt=True)
def main(save, url, tag):
    response = requests.get(url)
    file_name = get_domain_file_name(url)
    show_tags(file_name, tag, response, save == 'y')

    if save == 'y':
        save_response_file(file_name, response.text)


def save_response_file(file_name, response_text):
    file_name = f'{file_name}.html'
    file = open(file_name, 'w')
    file.write(response_text)
    file.close()


def show_tags(file_name, tag, response, save):
    soup = bsoup(response.text, 'html.parser')

    if save:
        file_name = f'{file_name}:{tag}-tag.txt'
        file = open(file_name, 'w')

        for tag in soup.find_all(tag):
            print(tag)
            file.write(str(tag) + '\n')
        file.close()
    else:
        for tag in soup.find_all(tag):
            print(tag)


def get_domain_file_name(url):
    from urllib.parse import urlparse
    parsed_uri = urlparse(url)
    return '{uri.netloc}'.format(uri=parsed_uri)


if __name__ == '__main__':
    main()
