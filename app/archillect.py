from requests_html import HTMLSession
import time
import settings

cache = {}

def lifecycle():
    global cache

    session = HTMLSession()

    r = session.get('http://archillect.com/')

    overlays = r.html.find('.overlay')

    results = []

    first = True

    for overlay in overlays[:settings.RANGE]:

        content = overlay.text

        if content in cache:
            print('found {} in cache as {}'.format(content, cache[content]))
            results.append(cache[content])
            continue

        if not first:
            print('yielding for {} second(s)'.format(settings.YIELD_TIME_SECONDS))
            time.sleep(settings.YIELD_TIME_SECONDS)

        first = False

        content_session = session.get(f'http://archillect.com/{content}')

        image = content_session.html.find('head > meta[name="twitter:image"]', first=True).attrs['content']

        sources = content_session.html.find('#sources > a')

        source = sources[0].attrs['href']

        if len(sources) > 1:
            source = sources[1].attrs['href']

        info = {"id": content, "img": image, "source": source}

        cache[content] = info

        results.append(info)

        print(f'{content} = {image}')

    print(f'{results}')

    with open(settings.INDEX_FILE, 'w') as f:
        f.write('<html><head><meta http-equiv="refresh" content="30"></head><body><table border="0" style="text-align: center;">')
        for result in results:
            f.write('<tr><td><a href="{}" target="_blank"><img src="{}" alt="{}" style="width: 100%;"></a></td></tr>\n'.format(result['source'], result['img'], result['id']))
        f.write('</table></body></html>')

    print('sleeping for {} second(s)'.format(settings.SLEEP_SECONDS))
    time.sleep(settings.SLEEP_SECONDS)

    with open(settings.INDEX_FILE, 'r') as f:
        html = f.read()

    print(f'{html}')


if __name__ == "__main__":
    while True:
        lifecycle()
