Title: Automatic Pelican publishing on GitHub Pages via TravisCI
Date: 2015-06-27
Modified: 2015-06-28
Category: Tech
Tags: devops, Travis CI, GitHub Pages, Pelican, git, continuous integration

As I wrote in the [last blog post]({filename}/fresh-start.md), the *static site generator* that I use to publish this post is [Pelican](http://getpelican.com/). Rather than generating the HTML on my machine and then pushing it to the ```gh-pages``` branch of [github.com/thomastweets/blog.thomasemmerling.de](https://github.com/thomastweets/blog.thomasemmerling.de) I automatized this process using [Travis CI](https://travis-ci.org/). Travis CI is a [continuous integration](https://en.wikipedia.org/wiki/Continuous_integration) that is free to use for open source projects. It can not only run automated tests of your project but also trigger deployment tasks when the build is successful.

Using information from [two](http://blog.mathieu-leplatre.info/publish-your-pelican-blog-on-github-pages-via-travis-ci.html) [blogs](https://zonca.github.io/2013/09/automatically-build-pelican-and-publish-to-github-pages.html) I was able to let Travis CI react on any push to GitHub and automatically generate HTML from the Pelican sources and push them back to the ```gh-pages``` branch. Here is how to do that:

- If you have not done that yet: Create a repository on GitHub called (*e.g.*) ```blog.thomasemmerling.de```.
- Add it as a remote to your local git repository from command line (if you use ssh-keys for authentication - you should do so! [how to generate](https://help.github.com/articles/generating-ssh-keys/) and [use](https://help.github.com/articles/changing-a-remote-s-url/) them):

```bash
# Go to your local Pelican sources
cd ~/blog
# Add the remote GitHub repository
git remote add origin git@github.com:thomastweets/blog.thomasemmerling.de.git
# set the default upstream and push to it
git push --set-upstream origin master
```

- As Travis CI needs to be able to push to your GitHub repository you need to authenticate it. As you do not want to store any passwords, ssh, or API keys in your repo or the Travis CI configuration the easiest way is to use the ```travis``` command line tool that is available as a gem to encrypt an Authentication Token for GitHub so that Travis CI can decrypt it when needed. First we need to install it:
```bash
# on OSX using the default Ruby installation
sudo gem install travis
```
- Now we create a personal access token on GitHub to use with Travis CI. Follow [these instructions](https://help.github.com/articles/creating-an-access-token-for-command-line-use/) to do so. I named mine ```TravisCI blog.thomasemmerling.de``` and kept the standard scope settings. Copy the token when you created it as you will not be able to see it again after you close the page.
- Encrypt the token with the ```travis``` command line tool:

```bash
# where 'your_token' is the token from the last step
travis encrypt GH_TOKEN=your_token
```

- Create a file ```.travis.yml``` (mind the dot at the beginning!) in the root of your git repository and paste the following (replace the encrypted part after ```- secure: ``` with what ```travis encrypt``` got back to you):

```yml
language: python
branches:
  only:
  - master
install:
- pip install pelican
- pip install ghp-import
- pip install markdown
script:
- make publish
- make github
env:
  global:
  - secure: "A4MpKClryaExBapCaXO3bgATD1KK/SmrdmPz7vk+6aUcJbOnQ/r2A1xjtCUv09PWW+QlA8SRBV626H7tfIONlXwLIn9tt6ZA419uoUWMs8Z2DsLvpHZtmP4TVi4Vi192TQDGqGwCh48aakhHlzWm0DTQKtn2MIJuUGOVOeT8DVhvT0jLOxYLAiRRuJI4OR6hVzHWH0Wa8U2BLC+iNsWn+RKro/HzzilY9p62nAahWe0toqltazQHq8AFMbc9BFuucMbfU/fpPYq1tesacQZG1gUFhs2TG1v7addJY63E0jaQ6jWSLgNdMibEvwmjrkKIeqF0E7J1/xZfoNg2KQpVFARqDkl4NOaf6T4inCaBAlvyxVQ6JszdkasM2AX3zzrg/Ph4ooRQ9sxdshq6g69tWbuDWkUGJMEfcKGfH9cbATeR87TXZZo0J5WajzNae1+zv86E2tVYmQM7wJwdve48wi6q+QpGWShMrT5VVOyLZ5txSYDPKgjCU7LrKqWmwVqEeZC8b49rSam6vsC1QAKsMQ+oiseZFuVAh+ZMpW9Tes9kSSQ1wX/zSepM3jbv+1dIpsjrJNZgQasR/yLAM7QjLQz8TwYG2LNPtOG/gWwdA/txLqGFAWnEgqFXeykbLgFwuFucdRe9I3yFi5VLTbwXw6FonWrjWOvSzKzNydP+fTw="
```

- In the ```Makefile``` in the root directory add (or modify) the ```github``` subcommand (this makes the ```make github``` command in the ```.travis.yml``` file work):

```bash
github: publish
	ghp-import -n $(OUTPUTDIR)
	@git push -fq https://${GH_TOKEN}@github.com/$(TRAVIS_REPO_SLUG).git gh-pages > /dev/null
```

- Add the ```.travis.yml``` file and the ```Makefile``` to your git repository, commit, and push to GitHub.

Now, if all went well, after a few minutes you should see a successful build in Travis CI and the new version of your homepage/blog and the ```.github.io``` address (or in my case the custom domain).
