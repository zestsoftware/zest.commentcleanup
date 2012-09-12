Changelog
=========

1.6 (unreleased)
----------------

- Nothing changed yet.


1.5 (2012-09-12)
----------------

- Moved to github.
  [maurits]


1.4 (2011-01-26)
----------------

- Also catch AttributeError in @@find-catalog-comments, which may
  happen for objects in portal_skins/custom.
  [maurits]


1.3 (2011-01-26)
----------------

- Moved the remove-buttons more the the left, so they do not hop
  around after deleting an item with a long title, or that causes a
  new long title to appear.
  [maurits]

- On the overview page offer to also index comments in objects that
  currently do not allow comments but may have done so in the past.
  [maurits]

- When switching comments off for an object, uncatalog its existing
  comments.
  [maurits]

- When turning comments on for an object, catalog its possibly
  already existing comments, when needed.
  [maurits]

- On the details page, also show number of actual comments, instead of
  only the comments in the catalog.
  [maurits]

- Added @@find-catalog-comments page (linked from the overview page)
  that finds and catalogs all comments for objects that currently
  allow commenting.  This is needed after a clear and rebuild of the
  portal_catalog, as the catalog then loses all info about comments.
  [maurits]


1.2 (2011-01-04)
----------------

- Sort the cleanup-comments-list on creation date.
  [maurits]


1.1 (2011-01-04)
----------------

- Handle redirection in the same way everywhere, so you also get to
  the same batched page using a came_from parameter.
  [maurits]

- Added '@@cleanup-comments-list' page that lists the latest comments.
  [maurits]


1.0 (2010-12-21)
----------------

- Initial release
