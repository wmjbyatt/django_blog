Blog.Post = DS.Model.extend({
  publishedDate: DS.attr('string'),
  visibility: DS.attr('string'),
  title: DS.attr('string'),
  user: DS.belongsTo('user'),
  body: DS.attr('string'),
  
  displayPublishedDate: function() {
    return moment(this.get('publishedDate')).format("YYYY/MM/DD h:mm A");
  }.property('publishedDate')  
});
