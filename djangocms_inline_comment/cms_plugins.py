from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase, PluginMenuItem
from cms.plugin_pool import plugin_pool
from cms.utils.urlutils import admin_reverse
from django.conf.urls import url
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from django.middleware.csrf import get_token
from djangocms_inline_comment.models import InlineComment


class InlineCommentPlugin(CMSPluginBase):
    model = InlineComment
    name = _("Inline comment")
    render_template = "djangocms_inline_comment/inline_comment.html"
    allow_children = True

    def get_extra_local_plugin_menu_items(self, request, plugin):
        return [
            PluginMenuItem(
                _("Hide contents (currently visible)") if plugin.show_contents else _("Show contents (currently hidden)"),
                admin_reverse("djangocms_inline_comment_change_show_contents"),
                data={
                    'plugin_id': plugin.pk,
                    'show_contents': '0' if plugin.show_contents else '1',
                    'csrfmiddlewaretoken': get_token(request),
                },
            )
        ]

    def get_plugin_urls(self):
        return [
            url(r'^change_show_contents/$', self.change_show_contents, name='djangocms_inline_comment_change_show_contents'),
        ]

    def change_show_contents(self, request):
        if not request.user.is_staff:
            return HttpResponseForbidden("not enough privileges")
        if not 'plugin_id' in request.POST or not 'show_contents' in request.POST:
            return HttpResponseBadRequest("plugin_id and show_contents POST parameter missing.")
        plugin = None
        if 'plugin_id' in request.POST:
            pk = request.POST['plugin_id']
            try:
                plugin = self.model.objects.get(pk=pk)
            except CMSPlugin.DoesNotExist:
                return HttpResponseBadRequest("plugin with id %s not found." % pk)
        show_contents = bool(int(request.POST['show_contents']))
        plugin.show_contents = show_contents
        plugin.save(update_fields=['show_contents'])
        return HttpResponse("ok")


plugin_pool.register_plugin(InlineCommentPlugin)
