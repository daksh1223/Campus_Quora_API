# Campus Quora API

***Authorization*** -  

To access the API get **access token** from **microsoft identity platform** .

Send a POST request at    **/login/**   
```json
with Header = {
    "Authorization" : "Bearer " + "access Token" }
}
```

You will recieve response : -  
```json
{  
    "username" : "Your microsoft email id",  
    "access token" : "Access token to be used for authentication here on",  
    "refresh token" : "Refresh token to refresh the access token"
}
```