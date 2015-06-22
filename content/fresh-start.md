Title: Fresh Starts
Date: 2015-06-21 10:51
Category: News

OK, this is the first day of the rest of my blog life. Over the last years I had a couple of blogs but none survived all the VPS reinstalls or migrations.
This time, however, I chose to host on [GitHub Pages](https://pages.github.com/), so that the blog is independent of any [devops](https://en.wikipedia.org/wiki/DevOps) experiments I pursue and will hopefully last longer.

I think that the first post should probably be about the technology that is driving it. So let's start!

### GitHub Pages
Venerable GitHub offers not only the probably most widely used service to host git repositories but also to host (raw html) data if they are present in certain repositories of your GitHub account or a branch called ```gh-pages```. If you want to know more about it [this](https://help.github.com/categories/github-pages-basics/) should help you out. You might wonder why you are still looking at the domain [blog.thomasemmerling.de](http://blog.thomasemmerling.de) and not [thomastweets.github.io/blog.thomasemmerling.de/](https://thomastweets.github.io/blog.thomasemmerling.de/): there is an easy way of adding a [CNAME record](https://en.wikipedia.org/wiki/CNAME_record) to your [DNS zone file](https://en.wikipedia.org/wiki/DNS_zone) and then add a file called ```CNAME``` to your git repository containing your custom domain (you can read more about that [here](https://help.github.com/articles/about-custom-domains-for-github-pages-sites/)).

### Pelican
Of course you could just go ahead and start to write HTML that will be your new homepage/blog. Although I like the back-to-the-roots mentality of it this approach has quite some overhead to maintain some visual aesthetics. This is where *static site generators* come in. You can find a quite exhaustive list of static site generators at [staticsitegenerators.net](https://staticsitegenerators.net/). As I really like Python I chose [Pelican](http://getpelican.com/). You can choose from a lot available [themes](https://github.com/getpelican/pelican-themes) or, of course, write your own. I use the nice [svbtle](https://svbtle.com/)-like [svbhack](https://github.com/gfidente/pelican-svbhack) by [Guilio Fidente](http://giuliofidente.com/). I like the fresh and clean looks of it.

I stop here for today. In the next post I am going to write about a nice way to automatize the publishing process using [continuous integration](https://en.wikipedia.org/wiki/Continuous_integration).
