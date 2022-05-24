import requests, string
from bs4 import BeautifulSoup

class Row:
	def __init__(self, origin, translate):
		self.origin = origin
		self.translate = translate

def get_soup(url):
	URL = f'https://www.amalgama-lab.com/{url}'
	response = requests.get(URL)
	soup = BeautifulSoup(response.text, 'lxml')
	return soup


def get_artists_by_letter(ltr):
	soup = get_soup(f'songs/{ltr}')
	porc1 = soup.find('div', class_='texts col')
	porc2 = porc1.find('ul', class_='g')
	porc3 = porc2.find_all('li')
	urls=[]
	for li in porc3:
		urls.append(li.find('a', href=True)['href'])
	return(urls)


def get_songs_by_urls(url):
	soup = get_soup(url)
	porc1 = soup.find('div', id='songs_nav').find('ul').find('ul').find_all('li')
	urls=[]
	for li in porc1:
		urls.append(li.find('a', href=True)['href'])
	return urls


def get_text_by_urls(url):
	soup = get_soup(url)

	names = soup.find('div', id='breadcrumbs_nav')
	artist_raw = names.find_all('a')[-1].text
	song_raw = names.text.split('\n')[-2]
	artist = "".join(l for l in artist_raw if (l.isalnum() and l != '_'))
	song = "".join(l for l in song_raw if (l.isalnum() and l != '_'))
	name = artist + ' - ' + song

	porc1 = soup.find_all('div', class_='string_container')
	rows=[]
	for r in porc1:
		orig = r.find('div', class_='original')
		trnslt = r.find('div', class_='translate')
		rows.append(Row(orig.text.replace('\n', ''), trnslt.text.replace('\n', '')))
	return name, rows


def write_txt_file(name, rows):
	f = open(f'{name}.txt', 'w', encoding="utf-8")
	for row in rows:
		f.write(f'{row.origin}\n{row.translate}\n' + '\n')
	f.close()



if __name__ == "__main__":
	rng_list = [i for i in string.ascii_lowercase[:26]]
	for i in range(10): rng_list.append(i)

	for ltr in rng_list:
		for a in get_artists_by_letter(ltr):
			for song in get_songs_by_urls(a):
				song_text = get_text_by_urls(f'{a}/{song}')
				write_txt_file(f'songs/{song_text[0]}', song_text[1])