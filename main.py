from lxml import html
import requests


class Parser:
    def __init__(self):
        self.url = 'https://www.dotabuff.com/'
        self.heroes = '/heroes/'
        self.matches = '/matches'
        self.profile = '/players/'
        self.records = '/records'
        self.headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}

    def replace(self, text):
        text = text.replace(']', '')
        text = text.replace('[', '')
        text = text.replace("'", '')
        text = text.replace("  ", '_')
        text = text.replace(")", '')
        text = text.replace("(", '')
        return text

    def get_profile(self, dotabuff_ID):
        response_matches = requests.get(self.url + self.profile + dotabuff_ID + self.matches, headers=self.headers)
        response_profile = requests.get(self.url + self.profile + dotabuff_ID, headers=self.headers)
        tree_matches = html.fromstring(response_matches.content)
        tree_profile = html.fromstring(response_profile.content)
        result = {}
        result['profile_image_url'] = tree_matches.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[4]/div[1]/div[1]/div[1]/div/a/img/@src')
        result['profile_nickname'] = tree_matches.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[4]/div[1]/div[1]/div[2]/h1/text()')
        result['profile_last_match'] = tree_matches.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[4]/div[1]/div[2]/dl[1]/dd/time/text()')
        result['profile_wins'] = tree_matches.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[4]/div[1]/div[2]/dl[2]/dd/span/span[1]/text()')
        result['profile_loses'] = tree_matches.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[4]/div[1]/div[2]/dl[2]/dd/span/span[3]/text()')
        result['profile_winrate'] = tree_matches.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[4]/div[1]/div[2]/dl[3]/dd/text()')
        result['profile_total_matches'] = tree_matches.xpath('/html/body/div[2]/div[2]/div[3]/div[5]/section/div/form/div[3]/section/article/div[2]/div[2]/div[1]/text()')
        result['profile_average_match_duration'] = tree_matches.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/section/div/form/div[3]/section/article/div[2]/div[2]/div[2]/text()')
        result['profile_average_kda'] = tree_matches.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/section/div/form/div[3]/section/article/div[2]/div[2]/div[4]/span/text()')
        result['profile_average_kills'] = tree_matches.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/section/div/form/div[3]/section/article/div[2]/div[2]/div[5]/span/text()')
        result['profile_average_deaths'] = tree_matches.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/section/div/form/div[3]/section/article/div[2]/div[2]/div[6]/span/text()')
        result['profile_average_assists'] = tree_matches.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/section/div/form/div[3]/section/article/div[2]/div[2]/div[7]/span/text()')
        result['profile_average_gpm'] = tree_matches.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/section/div/form/div[3]/section/article/div[2]/div[2]/div[8]/span/text()')
        result['profile_average_xpm'] = tree_matches.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/section/div/form/div[3]/section/article/div[2]/div[2]/div[9]/span/text()')
        result['profile_normal_matches'] = tree_profile.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/div[1]/div[2]/section[2]/article/table/tbody[2]/tr[1]/td[2]/text()')
        result['profile_rating_matches'] = tree_profile.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/div[1]/div[2]/section[2]/article/table/tbody[2]/tr[2]/td[2]/text()')
        result['profile_normal_winrate'] = tree_profile.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/div[1]/div[2]/section[2]/article/table/tbody[2]/tr[1]/td[3]/text()')
        result['profile_rating_winrate'] = tree_profile.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/div[1]/div[2]/section[2]/article/table/tbody[2]/tr[2]/td[3]/text()')
        result['profile_dire_games'] = tree_profile.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/div[1]/div[2]/section[2]/article/table/tbody[4]/tr[1]/td[2]/text()')
        result['profile_radiant_games'] = tree_profile.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/div[1]/div[2]/section[2]/article/table/tbody[4]/tr[2]/td[2]/text()')
        result['profile_dire_winrate'] = tree_profile.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/div[1]/div[2]/section[2]/article/table/tbody[4]/tr[1]/td[3]/text()')
        result['profile_radiant_winrate'] = tree_profile.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/div[1]/div[2]/section[2]/article/table/tbody[4]/tr[2]/td[3]/text()')
        result['profile_main_region'] = tree_profile.xpath(
            '/html/body/div[2]/div[2]/div[3]/div[5]/div[1]/div[2]/section[2]/article/table/tbody[5]/tr[1]/td[1]/text()')
        cleaned_result = {key: value[0] for key, value in result.items()}
        return cleaned_result

    def get_records(self, dotabuff_ID):
        response_records = requests.get(self.url + self.profile + dotabuff_ID + self.records, headers=self.headers)
        tree_records = html.fromstring(response_records.content)
        result = {}
        for i in range(14):
            i = i + 1
            record = self.replace(str(tree_records.xpath(f'/html/body/div[2]/div[2]/div[3]/div[5]/section/article/div/div[{i}]/div[2]/a/div[2]/text()')))
            record_match = self.replace(str(tree_records.xpath(f'/html/body/div[2]/div[2]/div[3]/div[5]/section/article/div/div[{i}]/div[2]/a/div[3]/text()'))).split('_')[0]
            a = self.replace(str(tree_records.xpath(f'/html/body/div[2]/div[2]/div[3]/div[5]/section/article/div/div[{i}]/div[2]/a/div[1]/text()')))
            result[a] = f'{record}_{record_match}'
        return result



