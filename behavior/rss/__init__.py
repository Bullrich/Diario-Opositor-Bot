# coding=utf-8
import yaml

verbose = None


def get_urls():
    return generate_urls(get_yml_file("config/urls.yml"))


def get_filtered_words():
    filtered_words = get_yml_file("config/filtered_words.yml")
    return encode_list(filtered_words['filtered_words'])


def generate_urls(url_data):
    rss = url_data['rss']
    newspapers = {}
    for newspaper in rss:
        urls_list = url_data[newspaper]['urls']
        newspapers[url_data[newspaper]["name"]] = encode_list(urls_list)
    if verbose:
        print newspapers
    return newspapers


def get_yml_file(yml_file_name):
    yml_file = open(yml_file_name)
    yml_data = yaml.safe_load(yml_file)
    yml_file.close()
    if verbose:
        print yml_file_name
        print yml_data
    return yml_data


def encode_list(list):
    return [x.encode('utf-8') for x in list]
