import requests
import datetime


#SPX
key = "cb978c0a4a9574dafc1e630885296ea231bb7964cea07ebf34e638672f66a347"
courier = "spx"
awb = "SPXID026979199288"
# awb = "SPXID02436902733A"





r = requests.get(f"https://api.binderbyte.com/v1/track?api_key={key}&courier={courier}&awb={awb}")
r_dict = r.json()
print(r_dict)
print(type(r.status_code))
# print(r_dict['data']['summary'])

print(f"Resi Pengiriman : {r_dict['data']['summary']['awb']}")
print(f"Penerima : {r_dict['data']['detail']['receiver']}")
print(f"Status Pengiriman : {r_dict['data']['summary']['status'].title()}")
print(f"Ekspedisi : {r_dict['data']['summary']['courier']}")
# print(f"Diterima Pada : {datetime.datetime.now()}")
deliver_time = datetime.datetime.now()
print(f"Delivered Time : {r_dict['data']['summary']['date']}")
print(f"Diterima Satpam Pada : {deliver_time.strftime('%A, %d-%m-%Y, %H:%M:%S')}")






# import requests

# url = f"https://api.aftership.com/v4/trackings/{awb}"

# headers = {
#     "Content-Type": "application/json",
#     "as-api-key": f"{key}"
# }

# response = requests.request("GET", url, headers=headers)

# print(response.text)

# import requests

# url = "https://api.aftership.com/v4/trackings"

# headers = {
#     "Content-Type": "application/json",
#     "as-api-key": f"{key}"
# }

# response = requests.request("GET", url, headers=headers)

# print(response.text)

# url = "https://api.aftership.com/v4/trackings"

# payload = {"tracking": {
#         "slug": "dhl",
#         "tracking_number": "123456789",
#         "title": "Title Name",
#         "smses": ["+18555072509", "+18555072501"],
#         "emails": ["angkianto@gmail.com"],
#         "order_id": "ID 1234",
#         "order_number": "1234",
#         "order_id_path": "http://www.aftership.com/order_id=1234",
#         "custom_fields": {
#             "product_name": "iPhone Case",
#             "product_price": "USD19.99"
#         },
#         "language": "en",
#         "order_promised_delivery_date": "2019-05-20",
#         "delivery_type": "pickup_at_store",
#         "pickup_location": "Flagship Store",
#         "pickup_note": "Reach out to our staffs when you arrive our stores for shipment pickup"
#     }}
# headers = {
#     "Content-Type": "application/json",
#     "as-api-key": ""
# }

# response = requests.request("POST", url, json=payload, headers=headers)

# print(response.text)