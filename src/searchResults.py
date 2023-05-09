import requests
from sys import argv

def main(retailer, query):
    if retailer == 'target':
        # http get request from target's search API
        search = requests.get(f'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&channel=WEB&count=24&keyword={query}&offset=0&page=1&pricing_store_id=1832&visitor_id=0188021CAB690201B0C889396D7E181B', headers={'User-Agent': 'Custom'})

        if search.status_code != 200: # check to make sure we got a valid response
            raise Exception(f"Search get request failed with response {search} from retailer {retailer}")

        # get response as json, then get the items from it
        products = search.json()['data']['search']['products']

        results = []

        for prod in products:
            try: # attempt to parse each individual product
                title = prod['item']['product_description']['title'].replace("'", "")
                price = prod['price']['formatted_current_price']
                tcin = prod['tcin']
                results.append(f'{title}: {price}; TCIN (UID): {tcin}')
            except: # if there's an error, ignore it
                pass
            
        return results

    if retailer == 'walmart':
        # set request params and headers because walmart will deny the request otherwise
        PARAMS = {'variables': '{"id":"","dealsId":"","query":"' + query + '","page":1,"prg":"desktop","catId":"","facet":"","sort":"best_match","rawFacet":"","seoPath":"","ps":40,"ptss":"","trsp":"","beShelfId":"","recall_set":"","module_search":"","min_price":"","max_price":"","storeSlotBooked":"","additionalQueryParams":{"hidden_facet":null,"translation":null,"isMoreOptionsTileEnabled":true},"searchArgs":{"query":"' + query + '","cat_id":"","prg":"desktop","facet":""},"fitmentFieldParams":{"powerSportEnabled":true},"fitmentSearchParams":{"id":"","dealsId":"","query":"' + query + '","page":1,"prg":"desktop","catId":"","facet":"","sort":"best_match","rawFacet":"","seoPath":"","ps":40,"ptss":"","trsp":"","beShelfId":"","recall_set":"","module_search":"","min_price":"","max_price":"","storeSlotBooked":"","additionalQueryParams":{"hidden_facet":null,"translation":null,"isMoreOptionsTileEnabled":true},"searchArgs":{"query":"' + query + '","cat_id":"","prg":"desktop","facet":""},"cat_id":"","_be_shelf_id":""},"enableFashionTopNav":false,"enableRelatedSearches":false,"enablePortableFacets":true,"enableFacetCount":true,"fetchMarquee":true,"fetchSkyline":true,"fetchGallery":false,"fetchSbaTop":true,"tenant":"WM_GLASS","enableFlattenedFitment":true,"pageType":"SearchPage"}'}
        HEADERS = { # this is ugly, but there's really nothing I can do about it because walmart hates me
            'authority': 'www.walmart.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'cookie': 'brwsr=eca6f773-3cf6-11ed-a817-5725a0b433bb; _ga=GA1.2.1490530452.1674964703; ACID=ce4e4b52-e114-4c9a-89bb-4ad9b9d49c8f; hasACID=true; vtc=ZrGmJ4vj52_izd9E7P-4lU; _pxhd=2a34d9c339c08ec8d2577eb6074a91aafa1e0d795b5cf704def2c0eed061b1c8:4dd4c37a-b981-11ed-baf0-436b43427053; dimensionData=577; _pxvid=4dd4c37a-b981-11ed-baf0-436b43427053; TBV=7; AID=wmlspartner%3D0%3Areflectorid%3D0000000000000000000000%3Alastupd%3D1677820141150; locGuestData=eyJpbnRlbnQiOiJTSElQUElORyIsImlzRXhwbGljaXQiOmZhbHNlLCJzdG9yZUludGVudCI6IlBJQ0tVUCIsIm1lcmdlRmxhZyI6ZmFsc2UsImlzRGVmYXVsdGVkIjpmYWxzZSwicGlja3VwIjp7Im5vZGVJZCI6IjQ1MzEiLCJ0aW1lc3RhbXAiOjE2Nzc4MjAwNTI2NzR9LCJzaGlwcGluZ0FkZHJlc3MiOnsidGltZXN0YW1wIjoxNjc3ODIwMDUyNjc0LCJ0eXBlIjoicGFydGlhbC1sb2NhdGlvbiIsImdpZnRBZGRyZXNzIjpmYWxzZSwicG9zdGFsQ29kZSI6IjYwNDQ2IiwiY2l0eSI6IlJvbWVvdmlsbGUiLCJzdGF0ZSI6IklMIiwiZGVsaXZlcnlTdG9yZUxpc3QiOlt7Im5vZGVJZCI6IjQ1MzEiLCJ0eXBlIjoiREVMSVZFUlkiLCJzdG9yZVNlbGVjdGlvblR5cGUiOm51bGx9XX0sInBvc3RhbENvZGUiOnsidGltZXN0YW1wIjoxNjc3ODIwMDUyNjc0LCJiYXNlIjoiNjA0NDYifSwibXAiOltdLCJ2YWxpZGF0ZUtleSI6InByb2Q6djI6Y2U0ZTRiNTItZTExNC00YzlhLTg5YmItNGFkOWI5ZDQ5YzhmIn0%3D; assortmentStoreId=4531; hasLocData=1; TB_SFOU-100=; adblocked=false; pxcts=686774c5-ca51-11ed-805d-507772467942; _gid=GA1.2.208204782.1679759028; ajs_anonymous_id=621c554c-b255-4869-ad93-000442b3f44c; chsn_cnsnt=www.walmart.com%3AC0001%2CC0002%2CC0003%2CC0004%2CC0005; tglr_sess_count=1; pmpdid=5d135357-6531-43f9-8420-a69f96479306; TS011d008b=011797f54128593278588e6cbe3ba5a9de046a913b8727530af3ab795f25d7a6c57adaff2a860630fc38db58e77909d4f77428cf67; TS019ef69b=01538efd7c99b8f6232b7bf4bc30a504343859de32185e6b41584e06b53eb0cbce71a973c3f63b028b36b1b79a93034d5910d7e9a9; auth=MTAyOTYyMDE4I9KTz4tCJwS3xxT0Orimvy%2BNDdOHdxWWf5W1TgyO67cSW6N5z0nrdE65%2BaT2svJKpnLJ3940bF4WAgeD8ZJKYtnp2Xbt3ppE4QhKNGz8OOIErZq2XC5iMtGmMw%2B0ZGBi767wuZloTfhm7Wk2Kcjygv699%2F6tFVwuL3qJB39WKV%2Fp2Q%2FErnN1MRh9tjVkpzihTqgBvcJrJyfyzA5dR4Bca44tU2RelMqpaOuu5MfGZtwUMk70P8glgOEpLOprhDfMDCcb9mgycy9jtT1uIyOBHcsxxAyUZnnLZUYYr%2FhSIKizHx%2F5x1lx3sYC%2FDFdn1f1kseT%2B3xuQ4hGVd1WZg7rMXh7MDMcCL9HcTki2DYLalp%2F4tsZXnxrCxqyO9NfxRQyPml502Mv1Uk5LQHQuNGaCEjyrOXbKKhH072NS%2FW0j%2FU%3D; bstc=a244EKmeh5J_4JsI-zcu04; mobileweb=0; xptc=assortmentStoreId%2B4531; xpth=x-o-mart%2BB2C~x-o-mverified%2Bfalse; xpa=0W4fs|14us3|A5Ih6|D8jju|DckjW|EGOfa|FSXGR|FvI0t|GkWzY|IM26Z|INoIG|K3TS3|Oj9au|VG72V|VfQ5W|YnYws|ZLvCF|_3mcc|aizjH|c8tN_|ce_CN|eITvb|f8iOA|fLj07|hCzsU|hlZ5z|jJAPh|omGZ5|rwcby|s_wwc|vx67L|w-QQR|wW-8A|y3LRi; exp-ck=0W4fs1A5Ih62D8jju1DckjW1EGOfa1FSXGR1FvI0t1GkWzY1IM26Z4K3TS32Oj9au1VfQ5W4YnYws4ZLvCF1_3mcc1aizjH1ce_CN1eITvb1f8iOA1hCzsU1jJAPh2s_wwc1vx67L1w-QQR3y3LRi1; xptwj=rq:0e976ecc5ff791c6fe68:GwF3q+6yOQ8VbxbjXEHUPj67HXrq2BkxSNOAr/QdRVhJfw0a9bavo8YN413BYvJqmrHcR8HlD7FrVsNySM+nKDL53T+m5IOtPwW/pzuCIRru0gOqnxZIkukNjl7XIAxIu+hHpDid24QSdY+bXenkyfqn5MozG/PPkIoV; akavpau_p2=1679812566~id=f4abace763251d4b59d16f83ee0a5b8d; _astc=728da170aa7932c549d0f94690d7e42c; ak_bmsc=1131FA797C2EA9174D30129073319494~000000000000000000000000000000~YAAQPAsRYMh8SweHAQAAQ32YHBP1DcSR2wLy6W32/3aqNYhgG0I06/7KKYg1mJjpjZryefaHNsTIGF1GdvWND4Inl3EAoZbBrSn4V45LLY6c/YuaxrPDxz1HN07l9IPQrQRbZ/mN1YjqX0q/hSFzwaVzQPLu95R77kjgcdSglR9IQIQ9qD83FHPZCz3vMt/Ewj3urt4/W5HmF7vltlJQYESe+KdeXkF3uLD1vxeAEj6KWSFiVHD5tuzLk7VkP1C4jSqNhgBei5luHJQ9GEnprICuzeItCu7Ww/khdz7PjEhdm9iI2b9gCwnLD0NDSnhio8eKTCPUUSVuQ+/1S9OV+RPJm7lzuZ2sryiwLRB+wAuurTh7bnbFZlAAMpAAuGC3m1QDJzE721FLM7BWyylc+A8WEezf1AqbgkKGwjRtarp+wIr0u699jfxx+dhinKUP8mz+xZx0HHqNZbJoO/HLoXdwanV2J0IS0UrC1m3jOWM=; _pxff_cfp=1; xpm=1%2B1679811966%2BZrGmJ4vj52_izd9E7P-4lU~%2B0; wmlh=530950f903db6e7cbc9b550d624ac4a887dff42a0e6b52d556c5f2ea5ee276b3; locDataV3=eyJpc0RlZmF1bHRlZCI6ZmFsc2UsImlzRXhwbGljaXQiOmZhbHNlLCJpbnRlbnQiOiJTSElQUElORyIsInBpY2t1cCI6W3siYnVJZCI6IjAiLCJub2RlSWQiOiI0NTMxIiwiZGlzcGxheU5hbWUiOiJSb21lb3ZpbGxlIFN1cGVyY2VudGVyIiwibm9kZVR5cGUiOiJTVE9SRSIsImFkZHJlc3MiOnsicG9zdGFsQ29kZSI6IjYwNDQ2IiwiYWRkcmVzc0xpbmUxIjoiNDIwIFdlYmVyIFJvYWQiLCJjaXR5IjoiUm9tZW92aWxsZSIsInN0YXRlIjoiSUwiLCJjb3VudHJ5IjoiVVMiLCJwb3N0YWxDb2RlOSI6IjYwNDQ2LTY1MzEifSwiZ2VvUG9pbnQiOnsibGF0aXR1ZGUiOjQxLjYwNzI4NiwibG9uZ2l0dWRlIjotODguMTI2OTIyfSwiaXNHbGFzc0VuYWJsZWQiOnRydWUsInNjaGVkdWxlZEVuYWJsZWQiOnRydWUsInVuU2NoZWR1bGVkRW5hYmxlZCI6dHJ1ZSwiaHViTm9kZUlkIjoiNDUzMSIsInN0b3JlSHJzIjoiMDY6MDAtMjM6MDAiLCJzdXBwb3J0ZWRBY2Nlc3NUeXBlcyI6WyJQSUNLVVBfQ1VSQlNJREUiLCJQSUNLVVBfSU5TVE9SRSJdfV0sInNoaXBwaW5nQWRkcmVzcyI6eyJsYXRpdHVkZSI6NDEuNjM2NCwibG9uZ2l0dWRlIjotODguMTA3MiwicG9zdGFsQ29kZSI6IjYwNDQ2IiwiY2l0eSI6IlJvbWVvdmlsbGUiLCJzdGF0ZSI6IklMIiwiY291bnRyeUNvZGUiOiJVU0EiLCJnaWZ0QWRkcmVzcyI6ZmFsc2V9LCJhc3NvcnRtZW50Ijp7Im5vZGVJZCI6IjQ1MzEiLCJkaXNwbGF5TmFtZSI6IlJvbWVvdmlsbGUgU3VwZXJjZW50ZXIiLCJzdXBwb3J0ZWRBY2Nlc3NUeXBlcyI6W10sImludGVudCI6IlBJQ0tVUCJ9LCJpbnN0b3JlIjpmYWxzZSwiZGVsaXZlcnkiOnsiYnVJZCI6IjAiLCJub2RlSWQiOiI0NTMxIiwiZGlzcGxheU5hbWUiOiJSb21lb3ZpbGxlIFN1cGVyY2VudGVyIiwibm9kZVR5cGUiOiJTVE9SRSIsImFkZHJlc3MiOnsicG9zdGFsQ29kZSI6IjYwNDQ2IiwiYWRkcmVzc0xpbmUxIjoiNDIwIFdlYmVyIFJvYWQiLCJjaXR5IjoiUm9tZW92aWxsZSIsInN0YXRlIjoiSUwiLCJjb3VudHJ5IjoiVVMiLCJwb3N0YWxDb2RlOSI6IjYwNDQ2LTY1MzEifSwiZ2VvUG9pbnQiOnsibGF0aXR1ZGUiOjQxLjYwNzI4NiwibG9uZ2l0dWRlIjotODguMTI2OTIyfSwiaXNHbGFzc0VuYWJsZWQiOnRydWUsInNjaGVkdWxlZEVuYWJsZWQiOnRydWUsInVuU2NoZWR1bGVkRW5hYmxlZCI6dHJ1ZSwiYWNjZXNzUG9pbnRzIjpbeyJhY2Nlc3NUeXBlIjoiREVMSVZFUllfQUREUkVTUyJ9XSwiaHViTm9kZUlkIjoiNDUzMSIsImlzRXhwcmVzc0RlbGl2ZXJ5T25seSI6ZmFsc2UsInN1cHBvcnRlZEFjY2Vzc1R5cGVzIjpbIkRFTElWRVJZX0FERFJFU1MiXX0sInJlZnJlc2hBdCI6MTY3OTgxMjI2ODY4NSwidmFsaWRhdGVLZXkiOiJwcm9kOnYyOmNlNGU0YjUyLWUxMTQtNGM5YS04OWJiLTRhZDliOWQ0OWM4ZiJ9; com.wm.reflector="reflectorid:0000000000000000000000@lastupd:1679811969000@firstcreate:1677820052640"; _px3=749c52b27d8c83d1fde2241025833ca704d9b7781325517a881956cabc2ddb5e:jwqozwCIRo38I1N4Au2ntUbNfbAmYsXn4b9BvqQAM/lfOZrHRtdr6lS78LOgue58im3GCMXa5hEzAdkA4dx6Og==:1000:FPxB3wgIzaHVrFkETCrlgZoIyVDJHkALaGL5cDBJ+DUyueh4mBhDIYRIIZUXRZoJchX+NDXUVlMfCCnCNjOhmNUQyK7/s2gH8YIAadtVsC++di6iB1+VKR/l9YLQUFXB0iWDiNl2pwLenYCJi6SmCyFeY2RrTsutWy3KTFJrSwglHwQYW0C4MQktaCU+oAsP21JQzlxCcNuI4G2a+fir/Q==; xptwg=3306321786:E08E453C47C8E0:23E25B8:D9FDD764:49BED54E:6880777A:; TS012768cf=01cb1199b1c75c0c930b9c2422a72b04f998818504e2887e13527d0586d617165e6f56f9912138d161467498737258343a5609e371; TS01a90220=01cb1199b1c75c0c930b9c2422a72b04f998818504e2887e13527d0586d617165e6f56f9912138d161467498737258343a5609e371; TS2a5e0c5c027=0851107c88ab20003955f2767faac7f93235f71b859e9ac68d801a92193775a70c908577a3ddad700884213d8f1130003286a55cf17b65ea6ff19f19641b6c53ec06607adcf06fe50238708b769dbc3354f681317ee7de0a221f365eb72c775d; bm_sv=26C7604B30012A40B9F93C333FCE29B0~YAAQPAsRYAF9SweHAQAA8saYHBPhqGXYCPSMTBf/6hOHu2u+kdUMjScUHH0xFw1JH2199sHwP1U2Ebw8Y38FdQ7Ke4VuOYZKW6Tqb3IacIRXecInlk8EisvAnPoOr4rKg1CDyhOg89D3vh8MpwA1FqwclRsc0f9FW2384nQdF+9Uy1jlTN2R/ZS4z4o1daAIYGyYabMyNYH85bvg7JAbWazt4g0asGZoAshhiyAL5t6MgE4ld7T1utfzkpu/yuwk3A==~1; _pxde=7491bb4a18e0fbd9c2cd5c8eb82c6dd576e1230736589cce0bf26f684194e238:eyJ0aW1lc3RhbXAiOjE2Nzk4MTE5OTIyMjh9',
            'device_profile_ref_id': 'KD99iK6I8gnzRPU--XSgFthZAX943XxwhNt3',
            'referer': f'https://www.walmart.com/search?q={query}',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-platform': '"Windows"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'wm_page_url': f'https://www.walmart.com/search?q={query}',
            'x-apollo-operation-name': 'Search',
            'x-enable-server-timing': '1',
            'x-latency-trace': '1',
            'x-o-bu': 'WALMART-US',
            'x-o-ccm': 'server',
            'x-o-correlation-id': 'Eyk4mviYkIQVi5JSkG4TIc9TYsbU8UMejtdE',
            'x-o-gql-query': 'query Search',
            'x-o-mart': 'B2C',
            'x-o-platform': 'rweb',
            'x-o-platform-version': 'main-1.58.0-a086a4-0324T0316',
            'x-o-segment': 'oaoh'
        }

        # http get request from walmart's crappy search API
        search = requests.get('https://www.walmart.com/orchestra/snb/graphql/Search/9a02e6e7b5db0aba794042ee2b0cb04e9166c05958e97f8967dd86e2b6efdbf6/search', params=PARAMS, headers=HEADERS)        

        if search.status_code != 200: # check to make sure we got a valid response
            raise Exception(f"Search get request failed with response {search} from retailer {retailer}")
        
        # get response as json, then get the items from it
        products = search.json()['data']['search']['searchResult']['itemStacks'][0]['itemsV2']
        
        results = []

        for prod in products:
            try: # attempt to parse each individual product
                title = prod['name'].replace("'", "")
                price = prod['priceInfo']['currentPrice']['priceString']
                sku = prod['usItemId']
                results.append(f'{title}: {price}; SKU (UID): {sku}')
            except: # if there's an error, ignore it
                pass
        
        return results

    raise Exception(f"{retailer} is not a valid retailer.")

if __name__ == "__main__":
    print(main(argv[1], argv[2]))