def can_view_user_posts(viewer, owner):

# Owner can always view
 if viewer == owner:
    return True

# public account
 if not owner.is_private:
   return True
 
#privacy account - must follow
 return owner.follower.filter(follower=viewer).exists()
