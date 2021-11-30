from django.forms import ModelForm
from .models import Comment

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['date', 'comment']

    def form_valid(self, form):
      # Assign the logged in user (self.request.user)
      form.instance.user = self.request.user  # form.instance is the cat
      # Let the CreateView do its job as usual
      return super().form_valid(form)
