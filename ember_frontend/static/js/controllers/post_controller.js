// Abstract editable controller, basically just for DRY
Blog.PostEditableController = Ember.ObjectController.extend({
  abstract_controller: true,
  
  visibility_options: [
    {code: 'PU', label: 'Public'},
    {code: 'PR', label: 'Private'},
    {code: 'DR', label: 'Draft'}
  ],
  
  actions: {
    save: function() {
      return false;
    }
  }
});

// Concrete controllers

Blog.PostsController = Ember.ArrayController.extend({
  sortProperty: 'publishedDate',
  sortAscending: false,
});

Blog.PostController = Ember.ObjectController.extend({
  belongsToCurrentUser: function() {
    return this.get('user') == Blog.CurrentUser
  }.property('user')
});

Blog.PostsNewController = Blog.PostEditableController.extend({
  actions: {
    save: function() {
      var self = this;

      current_user = this.store.find('user', Blog.get('currentUser'));
      var post = this.get('model');
      post.set('publishedDate', moment().format('YYYY-MM-DD HH:mm:ss'));
      post.set('user', Blog.CurrentUser);

      post.save().then(function(saved_post) {
        self.transitionToRoute('post', saved_post);
      });
    }
  }
});

Blog.PostEditController = Blog.PostEditableController.extend({
  actions: {
    save: function() {
      var post = this.get('model');
      
      post.save();
      
      this.transitionToRoute('post', post);
    }
  }
});
