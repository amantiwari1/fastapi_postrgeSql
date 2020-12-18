
# importing the requests library 
import requests, json 
  
# defining the api-endpoint  
API_ENDPOINT = "http://127.0.0.1:8000/posts/"
  
for i in range(1,50): 
    data = {
  "uuid": "fake...id"+str(i),
  "description": "this is description and with images and it is workiing",
  "username": "useranme"+str(i),
  "imageurl": "https://picsum.photos/1200/800",
  "nlike": i,
  "ncomment": i,
  "commentid": "string"+str(i),
}

    r = requests.post(
        url = API_ENDPOINT, 
        data = json.dumps(data),
        headers = {'content-type': 'application/json'}
    ) 
    
# extracting response text  
pastebin_url = r.text 
print("The pastebin URL is:%s"%pastebin_url)