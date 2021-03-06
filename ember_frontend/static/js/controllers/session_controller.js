Blog.SessionController = Ember.ObjectController.extend({
  username: null,
  password: null,
  errorMessage: null,
  user_id: null,

  reset: function() {
    this.setProperties({
      username: null,
      password: null,
      errorMessage: null,
      model: null
    });
  },

  isAuthenticated: function() {
    return !Ember.isEmpty(this.get('model'));
  }.property('model'),

  setCurrentUser: function(user_id) {
    if (!Ember.isEmpty(user_id)) {
      var currentUser = this.store.find('user', user_id);
      this.set('model', currentUser);
      this.set('user_id', user_id);
    }
  },

  actions: {
    login: function() {
      var self = this, data = this.getProperties('username', 'password');
      
      $.post('/api/session/', data).then(function(response) {
        self.set('errorMessage', response.message);
        self.setCurrentUser(response.user_id);
      });
    },
    logout: function() {
      $.ajax({url: '/api/session/', type: 'delete'});
      this.reset();
      this.transitionToRoute('index');
    }
  }
});
