from yandex_music import Client, Icon


client = Client().init()


def search(*arg):
    search_result = client.search(*arg)
    print(f'https://{search_result.best.result.cover_uri.replace("%%", "600x600")}')
    print(f'https://{search_result.best.result.artists[0]["cover"].uri.replace("%%", "600x600")}')
    print(f'{search_result.best.result.artists[0].name}')
    print(f'{search_result.best.result.albums[0].title}')
    print(f'{search_result.best.result.albums[0].year}')
    print(f'{search_result.best.result.title}')
    return f'{search_result.best.result.id}:{search_result.best.result.albums[0].id}'



if __name__ == '__main__':
    while True:
        input_query = input('Введите поисковой запрос: ')
        search(input_query)