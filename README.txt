Introduction
============

You have enabled commenting in your Plone Site.  Now you wake up and
see that during the night some spammer has added 1337 comments in your
site.  What do you do now?  Sure, you first shoot him and then you
integrate some captcha solution, but you still have those 1337
comments.  You do not want to click 1337 times on a delete button.
Have no fear: ``zest.commentcleanup`` will rescue you!  Or at least
it will help you get rid of those spam comments faster.


How does it work?
-----------------

Just add ``zest.commentcleanup`` to the eggs parameter of the
instance section of your buildout.cfg.  On Plone 3.2 or earlier add it
to the zcml parameter as well.

The package simply works by registering some browser views.  Start
your instance, go to the root of your site and add
``/@@cleanup-comments-overview`` to the url.  This will give you an
overview of which items in your site have comments.  It is sorted so
the item with the most comments is at the top.

Note that the overview works on other contexts as well, for example on
a folder.

In the overview click on the ``manage`` link of an item with comments.
This takes you to the ``cleanup-comments-details`` page of that item.
This lists all comments, ordered by creation date.  From there you can
delete single items.

But the biggest thing you can do there is: select a comment and delete
this **and all following comments**.  The idea is that the first three
comments may be valid comments, then there are a gazillion spam
comments, and very likely no actual human has added a valid comment
somewhere in that spam flood anymore. So you keep the first few
comments and delete the rest without having to buy a new mouse because
you have clicked too much.

From the overview page you can also go to the
``@@cleanup-comments-list`` page.  Here you see the latest comments,
which you can remove one at a time.  This is handier when you have
done the big cleanup already and only need to check the new comments
of the last few days.

All the used views are only available if you have the ``Manage
portal`` permission.


Requirements
------------

This has been tested on Plone 3.3.5 with the standard comments.  It
might or might not work with packages like
``quintagroup.plonecomments`` or ``plone.app.discussion``.  It
probably works on Plone 2.5 and 4 as well, but I have not checked.
Hey, it might even work in a default CMF site.
