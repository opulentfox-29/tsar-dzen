import os
import telegram
import dzen


def check_db():
    if not os.path.exists('db.txt'):
        open('db.txt', 'w', encoding='utf-8').close()


def make_post(post_json):
    with open('db.txt', 'r', encoding='utf-8') as f:
        if post_json['url'] in f.read():
            return
    dzen.create_post(post_json['text'], post_json['imgs'])
    with open('db.txt', 'a', encoding='utf-8') as f:
        f.write(post_json['url'] + '\n')


def main():
    check_db()
    posts_json = telegram.parse('https://t.me/Collegetsaritsyno', 2)
    dzen.auth()
    for post_json in posts_json:
        make_post(post_json)
    dzen.close_driver()


if __name__ == "__main__":
    main()
