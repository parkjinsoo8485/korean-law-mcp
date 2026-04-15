import json
import os

import requests


def fetch_korean_law(search_query=None, api_key=None):
    """
    援??踰뺣졊?뺣낫?쇳꽣(law.go.kr) ?ㅽ뵂 API瑜??댁슜?섏뿬 踰뺣졊 ?뺣낫瑜?媛?몄삤???⑥닔?낅땲??
    
    :param search_query: 寃?됲븷 踰뺣졊 ?대쫫 (?? "嫄댁텞踰?)
    :param api_key: OpenAPI ?몄쬆??(蹂몄씤???ㅻ줈 蹂寃??꾩슂)
    """
    api_key = api_key or os.getenv("LAW_OC")
    if not api_key:
        raise ValueError("LAW_OC environment variable is required.")

    base_url = "https://www.law.go.kr/DRF/lawSearch.do"
    
    # 湲곕낯 ?뚮씪誘명꽣 ?ㅼ젙
    params = {
        "OC": api_key,       # API Key
        "target": "law",     # ??? 踰뺣졊
        "type": "JSON",      # ?묐떟 ?뺤떇 (XML ?먮뒗 JSON)
    }
    
    if search_query:
        params["query"] = search_query

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # ?ㅻ쪟 諛쒖깮 ???덉쇅 泥섎━
        
        # JSON ?곗씠???뚯떛
        data = response.json()
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"API ?붿껌 以??ㅻ쪟媛 諛쒖깮?덉뒿?덈떎: {e}")
        return None
    except json.JSONDecodeError:
        print("寃곌낵瑜?JSON ?뺤떇?쇰줈 ?뚯떛?????놁뒿?덈떎. API ?ㅻ굹 ?붿껌 ?뚮씪誘명꽣瑜??뺤씤?댁＜?몄슂.")
        # 媛꾪샊 ?ㅻ쪟 硫붿떆吏媛 html?대굹 xml濡?諛섑솚?????덉쓬
        print("?묐떟 ?댁슜:", response.text[:200])
        return None

if __name__ == "__main__":
    # "誘쇰쾿"??寃?됲븯???덉젣
    law_name = "誘쇰쾿"
    print(f"'{law_name}' 寃??寃곌낵瑜?媛?몄삤??以?..\n")
    
    result = fetch_korean_law(search_query=law_name)
    
    if result and "LawSearch" in result and "law" in result["LawSearch"]:
        laws = result["LawSearch"]["law"]
        print(f"珥?{len(laws)}媛쒖쓽 踰뺣졊??寃?됰릺?덉뒿?덈떎.\n")
        
        for idx, law in enumerate(laws[:5], 1):  # 理쒕? 5媛쒕쭔 異쒕젰
            print(f"[{idx}] 踰뺣졊紐? {law.get('踰뺣졊紐낇븳湲')}")
            print(f"    踰뺣졊?뚭?: {law.get('?뚭?遺泥섎챸')}")
            print(f"    怨듯룷?쇱옄: {law.get('怨듯룷?쇱옄')}")
            print(f"    ?쒗뻾?쇱옄: {law.get('?쒗뻾?쇱옄')}")
            print("-" * 40)
    else:
        print("寃??寃곌낵媛 ?놁뒿?덈떎.")
