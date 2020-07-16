from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from django.conf import settings
from django.views import View

if not settings.DEBUG:
    from captcha.fields import ReCaptchaField

code = """inp{} = forms.CharField(label="{}. Seçenek", required={})"""
inps = dict()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class AddForm(forms.Form):
    if not settings.DEBUG:
        captcha = ReCaptchaField()

    title = forms.CharField(label="Başlık", max_length=200, min_length=10)
    exp = forms.CharField(widget=forms.Textarea, label="Açıklama", required=False)

    for i in range(1, 15+1):
        if i == 1 or i == 2:
            c = code.format(i, i, True)
            exec(c)
            inps.setdefault(c.split()[0], None)

        else:
            c = code.format(i, i, False)
            exec(c)
            inps.setdefault(c.split()[0], None)



@login_required
def add(request):
    form = AddForm(request.POST or None)

    if form.is_valid():
        title = form.cleaned_data.get("title")
        exp = form.cleaned_data.get("exp")

        all_datas = list()
        for i in range(1, 16):
            adi = "inp" + str(i)
            all_datas.append(adi)

        for name in all_datas:
            data = form.cleaned_data.get(name)
            inps[name] = data

        print(form.cleaned_data.get("inp"+str(3)))
        poll = models.Poll()
        poll.title = title
        poll.explanation = exp
        poll.author = request.user
        try:
            poll.save()
        except:
            messages.error(request, "Başlık eşsiz olmalıdır. Bu başlık başka bir ankette kullanılmış.")
            return render(request, "polls/add.html", context=dict(form=form))

        for a, b in inps.items():
            if b:
                ch = models.Choice()
                ch.text = b
                ch.save()
                poll.choices.add(ch)

        poll.save()
        request.user.give_score(5)
        messages.success(request, "Başarıyla bir anket oluşturdun. 5 puan kazandın!")
        return redirect("/")

    return render(request, "polls/add.html", context=dict(form=form))


class CommentForm(forms.Form):
    if not settings.DEBUG:
        captcha = ReCaptchaField()

    comment_content = forms.CharField(widget=forms.Textarea, label="Yorumun", min_length=10, max_length=300)


def detail(request, slug):
    context = dict(voted=None)

    poll = get_object_or_404(models.Poll, slug=slug)
    choices = poll.choices.all()
    comments = poll.comments.all()
    votesn = 0
    for i in choices:
        votesn += i.votes

    context.update(choices=choices, poll=poll, votesn=votesn)
    context.setdefault("comment_form", CommentForm())







    if not request.user.is_authenticated:
        context.update(auth=False)
        ip = get_client_ip(request)
        for c in choices:
            for i in c.visitor_voters.all():
                if str(i) == ip:
                    context.update(voted=True)
        
        if not context["voted"]:
            if request.POST.get("choice"): #ıjf9uhr9rg
                if voted:
                    messages.error(request, "Sistem Hatası: Bu cihaz zaten anketi oylamış.")
                    return redirect("home")

                choice = request.POST.get("choice")

                choice = choices.get(text=choice)

                #
                x = models.VisitorIPAddressModel()
                x.ip = ip
                x.save()
                #

                choice.visitor_voters.add(x)
                choice.votes += 1
                choice.save()

                messages.success(request, "Anketi oyladın")
                context.update(voted=True)
                return render(request, "polls/detail.html", context=context)
        return render(request, "polls/detail.html", context=context)
        
    else:
        context.update(auth=True)













        voted = bool()
        for i in choices:
            if request.user in i.voters.all():
                voted = True

        context.update(voted=voted)
        # Eğer Anket Oylandıysa
        if request.POST.get("choice"):
            if voted:
                messages.error(request, "Sistem Hatası: Kullanıcı zaten anketi oylamış.")
                return redirect("home")

            choice = request.POST.get("choice")

            choice = choices.get(text=choice)

            choice.voters.add(request.user)
            choice.votes += 1
            choice.save()

            messages.success(request, "Anketi oyladın, 1 puan kazandın!")
            request.user.give_score(1)
            context.update(voted=True)

        # Eğer Yorum Yapıldıysa
        elif request.POST.get("comment_content"):
            form = CommentForm(request.POST)
            if form.is_valid():
                comcon = request.POST.get("comment_content")
                comment = models.Comment()
                comment.text = comcon
                comment.author = request.user
                comment.save()
                poll.comments.add(comment)
                messages.success(request, "Başarıyla yorum yaptınız.")
                context.update(comment_form=CommentForm())
            context.update(comment_form=form)


        context.update(comments=comments)

        return render(request, "polls/detail.html", context=context)



class DetailView(View):
    post = None
    context = dict()
    choices = None
    comments = None
    request = None

    def end(self):
        return render(
            self.request,
            "polls/detail.html",
            context=self.context,
        )

    def is_voted_auth(self):
        voted = bool()
        for i in self.choices:
            if self.request.user in i.voters.all():
                voted = True
        
        return voted
    
    def is_voted_not_auth(self):
        voted = bool()
        for i in self.choices:
            for x in i.visitor_voters.all():
                if x.ip == self.ip:
                    voted = True
        
        return voted
    
    def get(self, request, slug):
        self.start(request, slug)

        return self.end()

    def post(self, request, slug):
        self.start(request, slug)

        if request.user.is_authenticated:
            return self.authenticated_post()
        
        else:
            return self.not_authenticated_post()
    
    def authenticated_post(self):
        """
        Yorum kontrol edilecek

        Oylanmış mı kontrol edilecek
        """

        request = self.request


        # Eğer Anket Oylandıysa
        if self.request.POST.get("choice"):
            if self.is_voted_auth():
                messages.error(self.request, "Sistem Hatası: Kullanıcı zaten anketi oylamış.")
                return self.end()

            choice = self.request.POST.get("choice")

            choice = self.choices.get(text=choice)

            choice.voters.add(request.user)
            choice.votes += 1
            choice.save()

            messages.success(self.request, "Anketi oyladın, 1 puan kazandın!")
            self.request.user.give_score(1)
            self.context.update(voted=True)

        # Eğer yorum yapıldıysa
        elif self.request.POST.get("comment_content"):
            form = CommentForm(self.request.POST)
            if form.is_valid():
                comcon = self.request.POST.get("comment_content")
                comment = models.Comment()
                comment.text = comcon
                comment.author = self.request.user
                comment.save()
                self.poll.comments.add(comment)
                messages.success(self.request, "Başarıyla yorum yaptınız.")
                self.context.update(comment_form=CommentForm())
            self.context.update(comment_form=form)
        
        return self.end()

    
    def not_authenticated_post(self):
        """
        Oylanmış mı diye kontrol edilecek
        """

        if self.request.POST.get("choice"): # Anketi oyladıysa
            if self.is_voted_auth():
                messages.error(self.request, "Sistem Hatası: Bu cihaz zaten anketi oylamış.")
                return redirect("home")

            choice = self.request.POST.get("choice")

            choice = self.choices.get(text=choice)

            #
            x = models.VisitorIPAddressModel()
            x.ip = self.ip
            x.save()
            #

            choice.visitor_voters.add(x)
            choice.votes += 1
            choice.save()

            messages.success(self.request, "Anketi oyladın")
            self.context.update(voted=True)
        
        return self.end()

    
    def start(self, request, slug):

        self.poll = get_object_or_404(models.Poll, slug=slug)
        self.comments = self.poll.comments.all()
        self.choices = self.poll.choices.all()


        self.votesn = 0
        for i in self.choices:
            self.votesn += i.votes
            
        for i in self.choices:
            if i.votes != 0:
                i.percent = int((i.votes*100) / self.votesn)
            else:
                i.percent = 0
            

        self.context.update(
            poll=self.poll,
            comments=self.comments,
            choices=self.choices,
            votesn=self.votesn,

        )

        self.request = request

        self.context.setdefault("comment_form", CommentForm())

        if request.user.is_authenticated:
            self.context.update(
                auth=True,
                voted=self.is_voted_auth(),
            )
        else:
            self.ip = get_client_ip(request)

            self.context.update(
                auth=False,
                voted=self.is_voted_not_auth(),
            )
        

def index(request):
    query = request.GET.get("q")
    polls = models.Poll.objects.all()
    alerts = models.Alert.objects.filter(is_active=True)

    if query:
        polls = polls.filter(
            Q(title__icontains=query) |
            Q(explanation__icontains=query)
        ).distinct()

    context = {
        "polls": polls,
        "alerts": alerts,
    }

    return render(request, "index.html", context=context)


