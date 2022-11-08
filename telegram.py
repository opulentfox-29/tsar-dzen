import requests
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

def get_text(item):
    text_bs4 = item.find('div', class_='tgme_widget_message_text')

    if text_bs4:
        text_str = str(text_bs4)
        emojis = text_bs4.find_all('i', class_='emoji')
        for emoji_bs4 in emojis:
            emoji = emoji_bs4.text
            text_str = text_str.replace(str(emoji_bs4), emoji)

        text_str = text_str.replace('<br/>', '\n')
        post_text = BeautifulSoup(text_str, 'html.parser').text
    else:
        post_text = ""
    post_text = post_text.replace('\n\n', '\n')
    return post_text


def parse_page(url):
    r = requests.get(url, headers=headers)
    
    open('1.html', 'w', encoding='utf-8').write(r.text)
    
    soup = BeautifulSoup(r.text, 'html.parser')
    posts = soup.find_all('div', class_='tgme_widget_message_wrap')

    posts_json = []
    for post in posts:
        post_text = get_text(post)
        url_post = post.find('a', class_='tgme_widget_message_date').get('href')

        img_urls = []
        imgs = post.find_all('a', class_='tgme_widget_message_photo_wrap')
        for img in imgs:
            img_url = img.get('style').split("url('")[1].split("')")[0]
            img_urls.append(img_url)

        posts_json.append({
            'url': url_post,
            'text': post_text,
            'imgs': img_urls
        })

    return posts_json


def parse(url, req_num):
    url = url.replace('t.me/', 't.me/s/')
    posts_json = []
    for i in range(req_num):
        posts_page = parse_page(url)
        start_id = posts_page[0]['url'].split('/')[-1]
        url = url.split('?before=')[0] + f'?before={start_id}'
        posts_json = posts_page + posts_json
        
    return posts_json
    

