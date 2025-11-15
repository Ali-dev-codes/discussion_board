from django.db.transaction import commit
from django.shortcuts import render, get_object_or_404, redirect  # أضف redirect هنا
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView

from .models import Board
from django.contrib.auth.models import User
from .models import Topic, Post
from .forms import NewTopicForm,PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


#def home(request):
 #   boards = Board.objects.all()
  #  return render(request,'home.html',{'boards':boards})

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'




def board_topics(request,board_id):
    board = get_object_or_404(Board,pk=board_id)
    queryset = board.topics.order_by('-created_dt').annotate(comments=Count('posts'))
    page = request.GET.get('page',1)
    paginator = Paginator(queryset,20)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger :
        topics = paginator.page(1)

    except EmptyPage:
        topics = paginator.page(paginator.num_pages)



    return render(request,'topics.html',{'board':board,'topics':topics})


@login_required
def new_topic(request,board_id):
    board = get_object_or_404(Board, pk=board_id)

    #user = User.objects.first()
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
          topic = form.save(commit=False)
          topic.board = board
          topic.created_by = request.user
          topic.save()

          post = Post.objects.create(
              message = form.cleaned_data.get('message'),
              created_by = request.user,
              topic = topic
          )

          return redirect('board_topics',board_id=board.pk)

    else:
        form = NewTopicForm()

    return render(request,'new_topic.html',{'board':board,'form':form})

def about(request):
    return HttpResponse("yes")  # هذا صحيح الآن


def topic_posts(request,board_id,topic_id):
    topic = get_object_or_404(Topic,board__pk=board_id,pk=topic_id)

#زيادة مرة واحدة لكل زيارة خاصة لكل مستخدم
    viewed_topics = request.session.get('viewed_topics',{})
    if str(topic.pk) not in viewed_topics:
        topic.views += 1
        topic.save()
        viewed_topics[str(topic.pk)]=True
        request.session['viewed_topics']=viewed_topics


    return render(request,'topic_posts.html',{'topic':topic})


def test_static(request):
    return render(request,'test_static.html')

@login_required
def reply_topic(request,board_id,topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
          post = form.save(commit=False)
          post.topic = topic
          post.created_by = request.user
          post.save()


          return redirect('topic_posts',board_id=board_id,topic_id=topic_id)

    else:
        form =PostForm()

    return render(request,'reply_topic.html',{'topic':topic,'form':form})



#--------------------GCBV
@method_decorator(login_required,name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_dt = timezone.now()
        post.save()
        return redirect('topic_posts',board_id=post.topic.board.pk,topic_id=post.topic.pk)