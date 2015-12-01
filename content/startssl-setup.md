Title: Let's already encrypt!
Date: 2015-12-02
Category: Tech
Tags: SSL, HTTPS, VPS, server, security

It seems that the internet finally understood that encryption is a necessity. Recently, the brilliant guys of [Let's Encrypt](https://letsencrypt.org) started their beta program and I got myself an invite for it. They [announced](https://letsencrypt.org/2015/11/12/public-beta-timing.html) that they will open their beta to the public tomorrow and I thought that this is a good moment to show off the small script that I used until now before it vanishes into obsolescence.

Before [Let's Encrypt](https://letsencrypt.org) came along [StartSSL](https://www.startssl.com) was one way to obtain a ssl certificate at no cost. However, the workflow of creating and installing the certificates was not very straight forward which led to [some](https://konklone.com/post/switch-to-https-now-for-free) [blogposts](https://joshemerson.co.uk/blog/secure-your-site) trying to help the novice user. I wanted to streamline the process so that I could have SSL certificates for some domains including all kinds of subdomains in place. As the free StartSSL certificates are not wildcard certificates this called for some scripting.

You can look at the code at [github.com/thomastweets/setupSSL](https://github.com/thomastweets/setupSSL). There is small ReadMe and some settings in the bash script. Things should be pretty self-explanatory - otherwise just send me a message!
From tomorrow on [Let's Encrypt](https://letsencrypt.org) might be the better choice. But no matter which tool you use: encrypt your traffic!
