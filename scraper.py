import requests
import lxml.html as html
import os
import datetime

XPATH_LINK_TO_ARTICLE = '//text-fill[not(@class)]/a/@href'
XPATH_TITLE = '//div/span[contains(@class,"kicker")]/following-sibling::text-fill/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_AUTHOR = '//div[@class="author-article"]/div/button/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'

HOME_URL = 'https://www.larepublica.co/'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            print(f'Status code: {response.status_code}')
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                print("Retreiving info...")
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','').replace('“',"").replace('”',"")
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
                author = parsed.xpath(XPATH_AUTHOR)[0]
                author = author.replace('\'',"").replace('[',"").replace(']',"")
            except IndexError:
                print("Under index error -> " + IndexError)
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                print("Writing an article...")
                f.write(title)
                f.write('\n\n')
                f.write(f'Autor: {author}')
                f.write('\n\n')
                f.write('-- Resumen --\n')
                f.write(summary)
                f.write('\n\n')
                f.write('-- Noticia completa --\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            print("Under ELSE")
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_articles = parsed.xpath(XPATH_LINK_TO_ARTICLE)

            #Either way could work, one prints the list 1 by 1 and this one the entire list.
            #print(links_to_articles) 
            #for i in range(len(links_to_articles)):
                #print(str(i + 1) + ".- " + links_to_articles[i])

            today = datetime.date.today().strftime('%d-%m-%y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_articles:
                parse_notice(link, today)    

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def main():
    parse_home()


if __name__ == "__main__":
    main()