import requests
from re import sub
from sys import argv
from utils import rp_parse_ingredient
from bs4 import BeautifulSoup

def main(retailer, identification):
    if retailer == 'target': # :heart_eyes:
        # http get request from target's product API
        product = requests.get(f'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&tcin={int(identification)}&pricing_store_id=1832&channel=WEB', headers={'User-Agent': 'Custom'})

        if product.status_code != 200: # check to make sure we got a valid response
            raise Exception(f"Product get request failed with response {product}") # replace this with a bs4 scraper

        price = product.json()['data']['product']['price']['reg_retail'] # pull price and product info from the json response
        bullets = product.json()['data']['product']['item']['product_description']['bullet_descriptions']
        
        weight_bullet = None
        for bullet in bullets: # find the bullet that has 'weight' in it
            if 'weight' in bullet.lower():
                weight_bullet = bullet.lower()
                break

        weight = weight_bullet[(weight_bullet.index('</b>') + 4):].strip() # pull the product weight from the bullet

        amount, unit, nope = rp_parse_ingredient(weight) # parse amount & unit for the product
        
        return list([amount, unit, 'name', price]) # return a list that can be parsed into json

    if retailer == 'walmart': # :face_vomiting:

        # we need to update the cookie every once in a while...why?
        headers = { "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36", "cookie": 'brwsr=eca6f773-3cf6-11ed-a817-5725a0b433bb; _ga=GA1.2.1490530452.1674964703; ACID=ce4e4b52-e114-4c9a-89bb-4ad9b9d49c8f; hasACID=true; vtc=ZrGmJ4vj52_izd9E7P-4lU; _pxhd=2a34d9c339c08ec8d2577eb6074a91aafa1e0d795b5cf704def2c0eed061b1c8:4dd4c37a-b981-11ed-baf0-436b43427053; dimensionData=577; _pxvid=4dd4c37a-b981-11ed-baf0-436b43427053; assortmentStoreId=4531; hasLocData=1; adblocked=false; ajs_anonymous_id=621c554c-b255-4869-ad93-000442b3f44c; chsn_cnsnt=www.walmart.com:C0001,C0002,C0003,C0004,C0005; tglr_sess_count=1; pmpdid=5d135357-6531-43f9-8420-a69f96479306; TBV=7; AID=wmlspartner=0:reflectorid=0000000000000000000000:lastupd=1680455698209; locGuestData=eyJpbnRlbnQiOiJTSElQUElORyIsImlzRXhwbGljaXQiOmZhbHNlLCJzdG9yZUludGVudCI6IlBJQ0tVUCIsIm1lcmdlRmxhZyI6ZmFsc2UsImlzRGVmYXVsdGVkIjpmYWxzZSwicGlja3VwIjp7Im5vZGVJZCI6IjQ1MzEiLCJ0aW1lc3RhbXAiOjE2Nzc4MjAwNTI2NzR9LCJzaGlwcGluZ0FkZHJlc3MiOnsidGltZXN0YW1wIjoxNjc3ODIwMDUyNjc0LCJ0eXBlIjoicGFydGlhbC1sb2NhdGlvbiIsImdpZnRBZGRyZXNzIjpmYWxzZSwicG9zdGFsQ29kZSI6IjYwNDQ2IiwiY2l0eSI6IlJvbWVvdmlsbGUiLCJzdGF0ZSI6IklMIiwiZGVsaXZlcnlTdG9yZUxpc3QiOlt7Im5vZGVJZCI6IjQ1MzEiLCJ0eXBlIjoiREVMSVZFUlkiLCJzdG9yZVNlbGVjdGlvblR5cGUiOm51bGx9XX0sInBvc3RhbENvZGUiOnsidGltZXN0YW1wIjoxNjc3ODIwMDUyNjc0LCJiYXNlIjoiNjA0NDYifSwidmFsaWRhdGVLZXkiOiJwcm9kOnYyOmNlNGU0YjUyLWUxMTQtNGM5YS04OWJiLTRhZDliOWQ0OWM4ZiJ9; pxcts=09878531-d54c-11ed-a40e-4678544c6958; auth=MTAyOTYyMDE4I9KTz4tCJwS3xxT0Orimvy+NDdOHdxWWf5W1TgyO67cSW6N5z0nrdE65+aT2svJKpnLJ3940bF4WAgeD8ZJKYtnp2Xbt3ppE4QhKNGz8OOIErZq2XC5iMtGmMw+0ZGBi767wuZloTfhm7Wk2KcjygpySosImygUk1x1iKsdnk49uMYpma9XLCM2zGjl8N6qLHIoMM2Oex8wiWNvxSmMEGS9CrVUcZoKrAVWU67OwvqMUMk70P8glgOEpLOprhDfMDCcb9mgycy9jtT1uIyOBHReebqv5XZrAPxIjX039LJnvn1UIcPl6K64sKvSl1WCw4K6Bxs8B82VEbP0ZKOq+VU3eeWEQDX0dgCg2Iq4RISF01b8Kjr2op5cuHcLYCqmsAS4ucvoei2LFl67zI5k06UjyrOXbKKhH072NS/W0j/U=; bstc=cvIyFJLbyHVdI7esrVC4XE; mobileweb=0; xptc=assortmentStoreId+4531; xpth=x-o-mverified+false~x-o-mart+B2C; xpa=14us3|1bHX2|456qm|4RtMC|5T7w_|6zw3d|A5Ih6|BB1yD|D8jju|DckjW|DjfL-|Duc09|HNply|K5ar6|LyOFM|M8rYu|Rtb_h|U947X|VG72V|WB4Te|YkBLY|YnYws|ZLvCF|btMCR|c8tN_|ce_CN|dP467|eITvb|f8iOA|fLj07|jJAPh|lPtmn|l_2Z-|ohl01|q8ZkB|tRgKW|vx67L; exp-ck=1bHX215T7w_3A5Ih63D8jju1DckjW1Duc091K5ar61M8rYu1Rtb_h1U947X1YkBLY2YnYws4ZLvCF1ce_CN1dP4671eITvb1f8iOA2jJAPh2lPtmn1l_2Z-1ohl011q8ZkB1vx67L1; ak_bmsc=BFE05E5C88D002145A4832D024531B60~000000000000000000000000000000~YAAQ1t3AFxyIK3OHAQAA2p7wehOp/w1jbpzK6v9iAW1yMyNecxmdHggTrUc7FkP1BttEoB44dmurVbeNU85BWJypLXLb6eRjnLquMZrlZx0lJuFLDVwrNlYNlOs7TcPpc/4aZZPpJL+DwkLzCSK6jZaqc7jOJDECdQ+eCA+lI2uATg7dZVx4+5uG0utw/Jm+spqeCQ/nCabp16znKtBdYuk0o4BeqFm0bQZ/scxGJIQBpbSilQwgNhTZGh+yf+Hfpfg9U3jSekfH8s6MKZBEwOs3EZWyNxjtzC0SLG9hLIDG2Z5/XB3l/0UEz/a9uFbMkYwGdyvPm1u3luDO2fVzIDVALuEo7VV7mzpkWT5YMQqyEJ+KH6fIczYGN0IbjlMvReNP6hU11gfb1Lh+2og7e9U/TgBRaZ49ddhOZuE2qUvkk8EUgx2wsW8yk3jxd/NtROkbOHIUHEfjNjrObJ0rqSTPIm+L7z4jHdiaHGG/; _astc=0a2efc852495bdc9e2c26ad0bc48c526; xpm=1+1681394801+ZrGmJ4vj52_izd9E7P-4lU~+0; locDataV3=eyJpc0RlZmF1bHRlZCI6ZmFsc2UsImlzRXhwbGljaXQiOmZhbHNlLCJpbnRlbnQiOiJTSElQUElORyIsInBpY2t1cCI6W3siYnVJZCI6IjAiLCJub2RlSWQiOiI0NTMxIiwiZGlzcGxheU5hbWUiOiJSb21lb3ZpbGxlIFN1cGVyY2VudGVyIiwibm9kZVR5cGUiOiJTVE9SRSIsImFkZHJlc3MiOnsicG9zdGFsQ29kZSI6IjYwNDQ2IiwiYWRkcmVzc0xpbmUxIjoiNDIwIFdlYmVyIFJvYWQiLCJjaXR5IjoiUm9tZW92aWxsZSIsInN0YXRlIjoiSUwiLCJjb3VudHJ5IjoiVVMiLCJwb3N0YWxDb2RlOSI6IjYwNDQ2LTY1MzEifSwiZ2VvUG9pbnQiOnsibGF0aXR1ZGUiOjQxLjYwNzI4NiwibG9uZ2l0dWRlIjotODguMTI2OTIyfSwiaXNHbGFzc0VuYWJsZWQiOnRydWUsInNjaGVkdWxlZEVuYWJsZWQiOnRydWUsInVuU2NoZWR1bGVkRW5hYmxlZCI6dHJ1ZSwiaHViTm9kZUlkIjoiNDUzMSIsInN0b3JlSHJzIjoiMDY6MDAtMjM6MDAiLCJzdXBwb3J0ZWRBY2Nlc3NUeXBlcyI6WyJQSUNLVVBfQ1VSQlNJREUiLCJQSUNLVVBfSU5TVE9SRSJdfV0sInNoaXBwaW5nQWRkcmVzcyI6eyJsYXRpdHVkZSI6NDEuNjM2NCwibG9uZ2l0dWRlIjotODguMTA3MiwicG9zdGFsQ29kZSI6IjYwNDQ2IiwiY2l0eSI6IlJvbWVvdmlsbGUiLCJzdGF0ZSI6IklMIiwiY291bnRyeUNvZGUiOiJVU0EiLCJnaWZ0QWRkcmVzcyI6ZmFsc2V9LCJhc3NvcnRtZW50Ijp7Im5vZGVJZCI6IjQ1MzEiLCJkaXNwbGF5TmFtZSI6IlJvbWVvdmlsbGUgU3VwZXJjZW50ZXIiLCJzdXBwb3J0ZWRBY2Nlc3NUeXBlcyI6WyJQSUNLVVBfQ1VSQlNJREUiLCJQSUNLVVBfSU5TVE9SRSJdLCJpbnRlbnQiOiJQSUNLVVAifSwiZGVsaXZlcnkiOnsiYnVJZCI6IjAiLCJub2RlSWQiOiI0NTMxIiwiZGlzcGxheU5hbWUiOiJSb21lb3ZpbGxlIFN1cGVyY2VudGVyIiwibm9kZVR5cGUiOiJTVE9SRSIsImFkZHJlc3MiOnsicG9zdGFsQ29kZSI6IjYwNDQ2IiwiYWRkcmVzc0xpbmUxIjoiNDIwIFdlYmVyIFJvYWQiLCJjaXR5IjoiUm9tZW92aWxsZSIsInN0YXRlIjoiSUwiLCJjb3VudHJ5IjoiVVMiLCJwb3N0YWxDb2RlOSI6IjYwNDQ2LTY1MzEifSwiZ2VvUG9pbnQiOnsibGF0aXR1ZGUiOjQxLjYwNzI4NiwibG9uZ2l0dWRlIjotODguMTI2OTIyfSwiaXNHbGFzc0VuYWJsZWQiOnRydWUsInNjaGVkdWxlZEVuYWJsZWQiOnRydWUsInVuU2NoZWR1bGVkRW5hYmxlZCI6dHJ1ZSwiYWNjZXNzUG9pbnRzIjpbeyJhY2Nlc3NUeXBlIjoiREVMSVZFUllfQUREUkVTUyJ9XSwiaHViTm9kZUlkIjoiNDUzMSIsImlzRXhwcmVzc0RlbGl2ZXJ5T25seSI6ZmFsc2UsInN1cHBvcnRlZEFjY2Vzc1R5cGVzIjpbIkRFTElWRVJZX0FERFJFU1MiXX0sImluc3RvcmUiOmZhbHNlLCJyZWZyZXNoQXQiOjE2ODE0MTY0MDM2MzEsInZhbGlkYXRlS2V5IjoicHJvZDp2MjpjZTRlNGI1Mi1lMTE0LTRjOWEtODliYi00YWQ5YjlkNDljOGYifQ==; wmlh=9150c07026be72969e0838c31b18418837e13ff6cf212e2297c8c48f70bce561; __cf_bm=.WWvsDizhCp2PJRyeeQSCnK2VntZGDSitLTBZTCKfJQ-1681394819-0-AbWTzI4WdFIgHgbmNnd0lCscsKQfz0BqjOLsrLFjw1HFpbMg/Fh69bvPFiWGdAJDM2txcFcWX9dog+630tuad8S328lJgj7digJn0gstn10u; xptwj=rq:aff030bd79981535207c:27l62GdZK2QQKB8Zebtx5CjmCVa5IJcizt3a/sbO9wQWWR2jLQiwSHu4bYgPH3t3ER1o7DGRqnRWWQtW9po68sX3PHDZiIjlXPKARx715e015WrdncwuaCIELblUHPlHbrDJhHkk3aopuNWeCtCd5crmyCYhgtgr; bm_mi=544CBCCCA2F23DD2342855887A3065DA~YAAQ2t3AF+9dFFyHAQAAFW70ehMwV6ZMratIOVGXDyE7XXwuSxibcWzS0DraZ0jtbqW8XrVxtvD20YtzHJ7kFArfAxkVs8EIgmihOfiAncF2bei/nuZ6kygPS7H59SY04VsUADMlaLqRPoFz8cpjpu3a0D1cts/jcHP5/W+3p2PILoclF3XjpTW4izOD3cQv7/I6LawIKdZrDOXUNheV9UWY3tAByGmWHMb0525HqVdTF8nViXxqPrrWm4DGok9LbBKipfk+cr32keBNM3knqdfJRTs0pVoVjGJnP0qHIeQFfFt+Ut1C/zhGElpIeF9TDqybr41UiZS1Uf229wRJTQ==~1; com.wm.reflector="reflectorid:0000000000000000000000@lastupd:1681395053000@firstcreate:1677820052640"; akavpau_p2=1681395653~id=96af56e50623444067b374b020658c18; xptwg=499898409:233FD02FE7DD280:5A0A7DE:434DC266:8DED6E7F:468F068A:; bm_sv=D25B4C306F702B879FCD60C0CFC13142~YAAQ2t3AFxBeFFyHAQAADXT0ehP2L50uGIbak5g2iweJXWNdclfBfF32UGgdZty7UhIU++u25FcjCO9gfGyhsHsO0rudtSlJt7rrSZWaTbSn97Y8mMs0Y3QmYErhXDp5uDpdPn5eutG5oAJTB2LHF5a6TUDxs9ryNu8oFzXcnhWvf7JOFcb/8lSEtxj5TFBzO7ARZkeKD5y7w1CXULJ7yhCTBMtVYT20Y8pWBiMTB2G74jYaZYv4whK7mqKYQVXKqks=~1; TS012768cf=01e5fbf0e67c4d9fc615b7b0cd498308e5a7dbb834d93770b1e0376dab74422756b2a234c0d6323fb3aa7f14cbb453dac05d9529c3; TS01a90220=01e5fbf0e67c4d9fc615b7b0cd498308e5a7dbb834d93770b1e0376dab74422756b2a234c0d6323fb3aa7f14cbb453dac05d9529c3; TS2a5e0c5c027=08f33e0ce8ab20004f9950673487de61d40cb8afa16ec309304c6552324f13267f7525eccca61ffc083d16ab571130006fa3434cc7c293b66c5e61c69aa8cc09628a5aa651e858ebbf65c6216613c7ea1e4b93ced5e3d55008ea270ae256d9f0; _px3=f3b2ad53b402680a0803d3955f94874e6bce8cab7565120c3463820ad5ec88fd:wVHR/5nbzocy+OLgVsOgRuzfRsJXp1UojalPQ5Xy12/IpSpBlL5WzTjAJpLN9X2Cj17bVKQQuVQVjoA8XBkoTA==:1000:0xlKBfyLGcDba1SU8rddalrbE2BRrc8qd68iL5OIFs+Wa7g3pjIILfDH86iBfu/o3fDhuqrKOJQxIoicAh5flrH/K+48JRBzsQnkyXo8gLVev/FjQfky4gMARjOGmQu0iBeTxN8x4WchFA9dLcOcMSUUDwTFvPcP3H2EqLHJYp0eev9b68352BwnCxRcpI/rGCAnZ6webvLJb9XSIPAoZA==; _pxde=2d2e8830437302cd571e655aca50dd96f36e7658536be3f1e7fddda45cbad580:eyJ0aW1lc3RhbXAiOjE2ODEzOTUxMjE3MjJ9' }

        # http get request from a walmart product page
        response = requests.get(f'https://www.walmart.com/ip/seort/{identification}', headers=headers)

        if response.status_code != 200: # check to make sure we got a valid response
            raise Exception(f"Product get request failed with response {response}")

        parsedHtml = BeautifulSoup(response.text, 'html.parser') # parse the html

        price = parsedHtml.find('span', attrs={'itemprop':'price'}).text # get price
        price = sub('[^0-9|.]', '', price) # remove all non-numeric characters from the price using regex
        name = parsedHtml.find('h1', attrs={'itemprop':'name'}).text # get product title

        amount, unit, nope = rp_parse_ingredient(name) # parse amount & unit for the product from the title

        return list([amount, unit, 'name', price]) # return a list that can be parsed into json
    
    raise Exception(f"{retailer} is not a valid retailer.")

if __name__ == "__main__":
    print(main(argv[1], argv[2]))