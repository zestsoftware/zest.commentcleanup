import logging
from Acquisition import aq_inner
from plone.protect import PostOnly
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

logger = logging.getLogger('zest.content')


class CommentManagement(BrowserView):

    def total_comments(self):
        """Total number of comments from this point on, including
        children.
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        search_path = '/'.join(context.getPhysicalPath())
        filter = dict(
            portal_type='Discussion Item',
            path=search_path,
            )
        brains = catalog.searchResults(**filter)
        return len(brains)

    def comments(self):
        """Comments on this context.

        Note that we only want comments directly in this context, not
        in any children in case folders can have comments.
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        search_path = '/'.join(context.getPhysicalPath())
        depth = len(context.getPhysicalPath()) - 1
        path = dict(
            query=search_path,
            depth=depth,
            )
        filter = dict(
            portal_type='Discussion Item',
            path=path,
            sort_on='created',
            )
        brains = catalog.searchResults(**filter)
        return brains

    def info(self):
        """Info on this context.
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        search_path = '/'.join(context.getPhysicalPath())
        brains = catalog.searchResults(portal_type='Discussion Item',
                                       path=search_path)
        count = len(brains)
        discussion_allowed = self.is_discussion_allowed(context)
        return dict(
            count=count,
            discussion_allowed=discussion_allowed,
            )

    def get_object_by_path(self, path):
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()
        return portal.restrictedTraverse(path)

    def is_discussion_allowed(self, obj):
        portal_discussion = getToolByName(
            self.context, 'portal_discussion', None)
        if portal_discussion is None:
            return False
        return portal_discussion.isDiscussionAllowedFor(obj)

    def paths(self):
        context = aq_inner(self.context)
        portal_url_tool = getToolByName(context, 'portal_url')
        portal_url = portal_url_tool()
        catalog = getToolByName(context, 'portal_catalog')
        search_path = '/'.join(context.getPhysicalPath())
        brains = catalog.searchResults(portal_type='Discussion Item',
                                       path=search_path)
        paths = {}
        for brain in brains:
            # Get path of real content item:
            path = '/'.join(brain.getPath().split('/')[:-2])
            if path in paths:
                paths[path] += 1
            else:
                paths[path] = 1

        sorted_paths = sorted(
            [(count, path) for (path, count) in paths.items()], reverse=True)

        # Make it handier for the template:
        results = []
        for count, path in sorted_paths:
            obj = self.get_object_by_path(path)
            info = dict(
                count=count,
                path=path,
                url=portal_url + path,
                title=obj.Title(),
                discussion_allowed=self.is_discussion_allowed(obj),
                )
            results.append(info)
        return results


class DeleteComment(BrowserView):

    def __call__(self):
        """Delete a comment/reply/reaction.

        Partly taken from
        Products/CMFPlone/skins/plone_scripts/deleteDiscussion.py
        """
        PostOnly(self.request)
        comment_id = self.request.get('comment_id')
        if not comment_id:
            raise ValueError("comment_id expected")
        context = aq_inner(self.context)
        portal_discussion = getToolByName(context, 'portal_discussion')
        talkback = portal_discussion.getDiscussionFor(context)

        # remove the discussion item
        talkback.deleteReply(comment_id)
        logger.info("Deleted reply %s from %s", comment_id,
                    context.absolute_url())

        # redirect to the manage comments view
        self.request.RESPONSE.redirect(
            context.absolute_url() + '/@@cleanup-comments')
        return u'Comment deleted'


class DeleteAllFollowingComments(CommentManagement):

    def __call__(self):
        """Delete this and all following comments.

        This is '''not''' about removing a comment and all its nested
        comments.  No, it is about removing a comment and removing all
        comments that have been added later.  The idea is that you use
        this to get rid of lots of spam comments in one go.
        """
        PostOnly(self.request)
        comment_id = self.request.get('comment_id')
        if not comment_id:
            raise ValueError("comment_id expected")
        context = aq_inner(self.context)
        portal_discussion = getToolByName(context, 'portal_discussion')
        talkback = portal_discussion.getDiscussionFor(context)

        found = False
        # Note that getting the comment brains could result in a
        # KeyError when the parent of a comment has been deleted just
        # now by us.  Easiest way around that is to get all comments
        # first.
        comments = self.comments()[:]
        for comment in comments:
            if comment.getId == comment_id:
                found = True
            if not found:
                continue
            # Remove the discussion item.  A no longer existing item
            # is silently ignored.
            talkback.deleteReply(comment.getId)
            logger.info("Deleted reply %s from %s", comment.getId,
                        context.absolute_url())

        # redirect to the manage comments view
        self.request.RESPONSE.redirect(
            context.absolute_url() + '/@@cleanup-comments')
        return u'Lots of comments deleted!'


class ToggleDiscussion(CommentManagement):

    def __call__(self):
        """Allow or disallow discussion on this context.
        """
        PostOnly(self.request)
        context = aq_inner(self.context)
        if context.isDiscussable():
            context.allowDiscussion(False)
        else:
            context.allowDiscussion(True)
        # redirect to the manage comments view
        self.request.RESPONSE.redirect(
            context.absolute_url() + '/@@cleanup-comments')
        return u'Toggled allowDiscussion.'
