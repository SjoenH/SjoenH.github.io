---
layout: post
title: How to write a new post
date: 2016-05-29T20:10:17+02:00
author: Henry
categories:
- blog
img: how-to-write-a-new-post.png

---
The posts need to go in the correct folder, and they need to be written in markdown. <!--more-->
For a overview of markdown check out Daring Fireball's [Syntax Overview](https://daringfireball.net/projects/markdown/syntax).

The start of the document needs to have some metadata, and it should be at the top of the your _.markdown_ file.
Here is the metadata for this particular post:
{% highlight ruby %}
---
layout: post
title: How to write a new post
date: 2016-05-29T20:10:17+02:00
author: Henry
categories:
- blog
img: post02.jpg
thumb: thumb02.jpg
---
{% endhighlight %}
After this you may start writing your post.

Please define where you want your post to split -Preferably after a paragraph or so, by including a _more_-tag as shown under:
{% highlight ruby %}
<!--more-->
{% endhighlight %}

For more information read the [Jekyll documentation](https://jekyllrb.com/docs/posts/)
