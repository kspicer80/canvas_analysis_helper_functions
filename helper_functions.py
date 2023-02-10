import json
import re
import spacy
nlp = spacy.load('en_core_web_lg')

# A function to normalize the data returned from the Canvas Instructure API—will need to change row['replies'] to, potentially, row['recent_replies']:

def normalize_data(data):
    result = []
    for row in data:
        result.append({
            'id': row['id'],
            'parent_id': row['parent_id'],
            'user_id': row['user_id'],
            'message': row['message']
        })
        if 'replies' in row:
            result += normalize_data(row['replies'])
    return result

# A function to clean up the student posts, which have HTML tags in them ...:

def clean_text(text):
    text = re.sub(r'<.*?>', '', text) # remove HTML tags
    text = text.replace('\n', ' ').replace('&nbsp;', ' ')

    # replace Unicode characters
    text = text.translate(str.maketrans({'\u2019':"'"}))
    return text

# Functions to track author mentions in student posts:

def track_aliases(json_file, input_string):
    data = json.load(json_file)
    alias_count = {}
    name_title_count = {}
    for item in data:
        name = item["name"]
        title = item["title"]
        if name not in name_title_count:
            name_title_count[name] = {}
        if title not in name_title_count[name]:
            name_title_count[name][title] = {}
        for alias in item["aliases"]:
            if alias not in alias_count:
                alias_count[alias] = 0
            if alias not in name_title_count[name][title]:
                name_title_count[name][title][alias] = 0
            if alias in input_string:
                alias_count[alias] += 1
                name_title_count[name][title][alias] += 1
    filtered_data = [item for item in data if any(alias_count[alias] > 0 for alias in item["aliases"])]
    filtered_alias_count = {k: v for k, v in alias_count.items() if v > 0}
    return filtered_alias_count, filtered_data

def track_aliases_1(json_data_filepath, test_string):
    with open(json_data_filepath) as json_file:
        json_data = json.load(json_file)
    result = {}
    for author in json_data:
        alias_count = 0
        title_count = 0
        for alias in author['aliases']:
            alias_count += test_string.count(alias)
        title_count = test_string.count(author['title'])
        if alias_count > 0 or title_count > 0:
            result[f"{author['name']} - {author['title']}"] = {'alias_count': alias_count, 'title_count': title_count}
    return result

def track_aliases_v2(json_data_filepath, input_string):
    with open(json_data_filepath) as json_file:
        data = json.load(json_file)
    result = {}
    for item in data:
        title_count = input_string.count(item['title'])
        aliases_count = sum(input_string.count(alias) for alias in item['aliases'])
        if aliases_count > 0 or title_count > 0:
            result[item['name']] = {'aliases_count': aliases_count, 'title_count': title_count}
            # check if title count is greater than aliases count
            if title_count > aliases_count:
                result[item['name']]['text'] = item['title']
    return

def track_aliases_v3(json_data_filepath, input_string):
    with open(json_data_filepath) as json_file:
        data = json.load(json_file)
    result = {}
    for item in data:
        title_count = input_string.count(item['title'])
        aliases_count = sum(input_string.count(alias) for alias in item['aliases'])
        if aliases_count > 0 or title_count > 0:
            result[item['name'] + ' ' + item['title']] = {'aliases_count': aliases_count, 'title_count': title_count}
    return result

def track_aliases_with_dict(data, test_string):
    with open('author_list_no_numbers_v4.json') as json_file:
        author_data = json.load(json_file)
    result = {}
    for item in data:
        title_count = test_string.count(item['title'])
        alias_count = sum(test_string.count(alias) for alias in item['aliases'])
        if title_count > 0 or alias_count > 0:
            result[item['name']] = {'title': item['title'], 'aliases': alias_count, 'title': title_count}
    return result

def track_aliases_with_unique_id(author_data, text_string):
    with open('author_list_no_numbers_v4.json') as json_file:
        author_data = json.load(json_file)
    result = {}
    for author in author_data:
        title_count = text_string.count(author['title'])
        alias_count = sum([text_string.count(alias) for alias in author['aliases']])
        if title_count + alias_count > 0:
            result[author['id_number']] = {'name': author['name'], 'title': author['title'], 'alias_count': alias_count, 'title_count': title_count}
    return result

def find_most_similar(text, df, text_index):
    max_similarity = -1
    max_index = -1
    max_similarity_value = -1
    doc = nlp(text)

    for i, row in df.iterrows():
        if i != text_index:
            similarity = doc.similarity(nlp(row['cleaned_text']))
            if similarity > max_similarity:
                max_similarity = similarity
                max_index = i
                max_similarity_value = similarity

    return max_index, max_similarity_value



