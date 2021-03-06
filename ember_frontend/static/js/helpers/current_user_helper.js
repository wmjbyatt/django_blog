Blog.CurrentUserHelper = {
  beforeModel: function() {
  
    if (!this.controllerFor('application').get('currentUser')) {
      var auth_deferred = $.get('/api/session');
      
      auth_deferred.then(function(response) {
        var self = this;
      
        user = this.store.find('user', response.user_id).then( function(user) {
          Blog.CurrentUser = user;
        });
        
      }.bind(this));
      
      return auth_deferred;
    }
  },
  
  currentUser: function() {
    return Blog.CurrentUser;
  }.property()
};
