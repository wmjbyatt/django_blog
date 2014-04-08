Blog.Router.map(function() {
  this.resource('posts', function() {
    this.route('new');
  });
  this.resource('post', { path: '/post/:post_id' }, function() {
    this.route('edit');
  });
  this.resource('user', { path: '/user/:user_id' });
  this.resource('session');
});

Blog.ApplicationRoute = Ember.Route.extend({
  setupController: function(controller, model) {
    var self = this;
    Ember.$.getJSON('/api/session/').then( function(response) {
      self.controllerFor('session').setCurrentUser(response.user_id);
    });
  }
});

Blog.IndexRoute = Ember.Route.extend({
  redirect: function() {
    this.transitionTo('posts');
  }
});


Blog.UserRoute = Ember.Route.extend({
  afterModel: function(model) {
    // Nested route lookups weren't loading the associations before the template rendered,
    // so we use direct filtered querying to load the associations.
    var store = this.get('store'),
        userId = model.get('id');
    
    var promises = [
      store.find('post', {user_id: userId})
    ]
    
    return Ember.RSVP.all(promises);
  }
});


Blog.PostsRoute = Ember.Route.extend(Blog.CurrentUserHelper,{
  model: function() {
    return this.store.find('post');
  }
});

Blog.PostsNewRoute = Ember.Route.extend({
  model: function() {
    return this.store.createRecord('post');
  },
  
  renderTemplate: function() {
    this.render('posts.new', {
      into: 'application',
      controller: 'postNew'
    });
  }
});

Blog.PostEditRoute = Ember.Route.extend({
  model: function(params) {
    return this.modelFor('post')
  },

  afterModel: function(post) {
    // Kicking the user back if they don't own this resource
    if (post.get('user') != Blog.CurrentUser) {
      this.transitionTo('post', post);
    }
  },

  renderTemplate: function() {
    this.render('posts.new', {
      into: 'application',
      controller: 'postEdit'
    });
  }
});
