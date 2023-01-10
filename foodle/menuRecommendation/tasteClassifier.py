from hanspell import spell_checker
from googletrans import Translator
import urllib.request
import json
import ssl

papago_client_id = "8HomdWr_OTEECvrQnM6j"
papago_client_secret = "QOZkuLzsBt"

fl = ["매운맛", "신맛", "단맛", "쓴맛", "짠맛"]

def sentence_analyze(sentence):
    flavor_weight = [0, 0, 0, 0, 0] # [spicy_weight, sour_weight, sweet_weight, bitter_weight, salty_weight]
    replace_dict = {"약간" : "덜", "조금" : "덜", "엄청" : "매우"}

    replacement = replace_dict.keys()
    for replace in replacement:
        if replace in sentence:
            sentence = sentence.replace(replace, replace_dict[replace])

    checked_sentence = spell_checker.check("나에게 " + sentence + " 음식 추천해줘").checked
    #checked_sentence = "나에게 " + sentence + " 음식 추천해줘"
    #print("sentence : " + checked_sentence)

    # <파파고 API>
    encText = urllib.parse.quote(checked_sentence)
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"

    request = urllib.request.Request(url)
    request.add_header("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
    request.add_header("X-Naver-Client-Id",papago_client_id)
    request.add_header("X-Naver-Client-Secret",papago_client_secret)
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(request, data=data.encode("utf-8"), context=context)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        json_object = json.loads(response_body.decode('utf-8'))
        translated_text = json_object.get("message").get("result").get("translatedText")
        #print(translated_text)
    else:
        print("Error Code:" + rescode)

    # <google trans API>
    # translator = Translator()
    # result = translator.translate(checked_sentence)
    # translated_text = result.text
    # print("translated_sentence : " + translated_text)

    flavors = ["spicy", "sour", "sweet", "bitter", "salty"]
    adverb_dict = {"not" : -1, "very" : 2, "slightly" : 0.5, "bit" : 0.5, "really" : 2, "little" : 0.5, "without" : -1, "less" : 0.5}
    adverbs = adverb_dict.keys()
    sentence_token = translated_text.split()

    for (i,flavor) in enumerate(flavors):
        try:
            flavor_index = sentence_token.index(flavor)
        except ValueError:
            flavor_index = -1

        if flavor_index != -1:
            flavor_weight[i] = 1
            if flavor_index != 0:
                prev_word = sentence_token[flavor_index-1]
                if prev_word in adverbs:
                    flavor_weight[i] *= adverb_dict[prev_word]

    return flavor_weight



#sentence = input("먹고싶은 음식을 묘사하는 문장을 입력해주세요 : ")
#result = sentence_analyze(sentence)

# for i in range(5):
#     print(str(fl[i]) + " 가중치 : " + str(result[i]))