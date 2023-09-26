import requests
import hashlib
from flask import render_template
from db_handler import *
from bs4 import BeautifulSoup
import difflib


#---------------------Helper Functions--------------------------


def update_db(changed_urls, db_dict, curr_hashes):
    changed_data = []
    diffc =""
    for url in changed_urls:
        # print(db_dict[url]) # url : hash,content,dattie,tzinfo
        # print(curr_hashes[(url).lstrip('"["').rstrip('"]"')]) # url : hash,content
        diffc = diff(db_dict[url][1],curr_hashes[url][1])
        changed_data.append( [url, db_dict[url][0], db_dict[url][2], curr_hashes[url][0], diffc])
        update_row( str(url),curr_hashes[url][0], curr_hashes[url][1] )
        # print(f'Updated URL : {url}')
    return changed_data

def insert_urls(hashes):
    message = ""
    for key,val in hashes.items():
        if val in ["Invalid URL Schema","URL BAD - REQ EXCEPTION","BAD URL EXCEPTION e"]:
            try:
                insert_url(str(key), str(val), str(val))
            except Exception as e:
                message += f'Key {key} already exists \n '
        else:
            message+=f'{key} :-key issue {val}\n'
        if val not in ["Invalid URL Schema","URL BAD - REQ EXCEPTION","BAD URL EXCEPTION e"]:
            try:
                insert_url(str(key), str(val[0]), str(val[1]))
            except Exception as e:
                message += f'Key {key} already exists \n '
        else:
            message+=f'{key} :-key issue {val}\n'
    message += "if any, Remaining URLS have been added successfully ! "
    return message


def diff(str1:str, str2:str):
    delta = difflib.HtmlDiff(
                tabsize=8, wrapcolumn=60, linejunk=None, charjunk=difflib.IS_CHARACTER_JUNK
            ).make_table(
                str1.split("."), str2.split("."),  fromdesc='old version', todesc='new version', context=True, numlines=3
                )
    print(delta)
    return str("".join(delta))


def check_for_changes(db_dict :dict, curr_hashes:dict):
    changed_urls = []
    for url in db_dict.keys():
        if (db_dict[url][0] == curr_hashes[url][0]):
            pass
        else:
            changed_urls.append(url)

    return changed_urls


def readfile(fname):
    fdata=""
    with open(f'./uploads/{fname}', "r") as f:
        try:
            fdata = f.read()
        except Exception as e:
            return render_template('errors.html', message="File cant be read UPLOAD proper file")
        finally:
            f.close()
    os.remove(f'./uploads/{fname}')
    return fdata


def track(urls):
    if urls:
        current_hashes = hash_urls(urls)
        return current_hashes
    else:
        return render_template("errors.html", message="URLs empty")


def hash_urls(urls):
    current_hashes = {}
    for page_url in urls:
        current_hashes[page_url] = hash_page_url(page_url)
    return current_hashes


def hash_page_url(page_url):
    print("~"*60)
    print(f'Fetching URL : {page_url}')
    page_url_hash = ""
    try:
        r = requests.get(page_url)
        m = hashlib.md5()
        m.update(r.content)
        page_url_hash = m.hexdigest()
        print("~"*60)
        return [page_url_hash, remove_tags(r.content)]
    except requests.exceptions.InvalidSchema as e:  # This is the correct syntax
        message="Invalid URL Schema"
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        message="BAD URL - REQ EXCEPTION"
    except Exception as e:
        message="BAD URL EXCEPTION e"
    print("~"*60)
    return message

 
def formatted(urls:str):
    urls = urls.split(",")
    for i in range(len(urls)):
        urls[i] = urls[i].strip()
        urls[i] = urls[i].strip("\n")
        urls[i] = urls[i].replace("\n","")
    return urls

def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
    # return data by retrieving the tag content
    return '.'.join(soup.stripped_strings)