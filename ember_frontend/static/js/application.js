window.Blog = Ember.Application.create();

Blog.ApplicationAdapter = DS.DjangoRESTAdapter.extend({
  namespace: 'api'
});
