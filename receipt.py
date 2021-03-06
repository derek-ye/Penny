from flask import request
import requests
import json

def ocr_space_file(filename, overlay=False, api_key='9235378b0b88957', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'isTable': True
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload
                          )
    return r.content.decode()


def ocr_space_url(url, overlay=False, api_key='9235378b0b88957', language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()


if __name__ == "__main__":
    test_file = ocr_space_file(filename='Receipt.jpg', language='eng')
    test_obj = json.loads(test_file)
    #import pprint
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(test_file)
    print(test_obj['ParsedResults'][0]['TextOverlay']['Lines'][0]['LineText'])
    #print(test_obj)
    print(test_obj['ParsedResults'][1]['TextOverlay']['Lines'][0]['LineText'])
    print(test_obj['ParsedResults'][2]['TextOverlay']['Lines'][0]['LineText'])
    print(test_obj['ParsedResults'][3]['TextOverlay']['Lines'][0]['LineText'])
    print(test_obj['ParsedResults'][4]['TextOverlay']['Lines'][0]['LineText'])

