# Campus Quora API

***Authorization*** -  

To access the API get **access token** from **microsoft identity platform** .

Send a POST request at    **/login/**   
```
with Header = {
    "Authorization" : Access Token,
}
```

You will recieve response : -  
```
{  
    "username" : "Your microsoft email id",  
    "access token" : "Access token to be used for authentication here on",  
    "refresh token" : "Refresh token to refresh the access token"
}
```
