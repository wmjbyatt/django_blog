Blog.User = DS.Model.extend({
  username: DS.attr('string'),
  firstName: DS.attr('string'),
  lastName: DS.attr('string'),
  posts: DS.hasMany('post', {asynch: true}),
  
  fullName: function() {
    return this.get('firstName') + " " + this.get('lastName')
  }.property('firstName', 'lastName')
});
