import re


def cleanxml(raw_xml):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_xml)
    return cleantext


def only_single_whitespace(str):
    spl = str.replace("\n", " ").split(" ")
    arr = []
    for part in spl:
        if part != "" and part != " ":
            arr.append(part)
    return " ".join(arr)


def remove_all_whitespace(str):
    return str.replace(" ","")
