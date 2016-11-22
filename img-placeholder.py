import sublime
import sublime_plugin
import re

completions = []

def plugin_loaded():
    init_settings()

def init_settings():
    get_settings()
    sublime.load_settings('img-placeholder.sublime-settings').add_on_change('get_settings', get_settings)

def get_settings():
    settings = sublime.load_settings('img-placeholder.sublime-settings')
    domains = settings.get('domains')
    protocol = settings.get('protocol', 'http:')
    width = str(settings.get('width', 600))
    height = str(settings.get('height', 300))
    background_color = settings.get('backgroundColor', 'ccc')
    text_color = settings.get('textColor', '333')
    file_ext = settings.get('format', 'png')
    text = settings.get('text', '')

    del completions[:]
    for domain in domains:
        url = protocol + '//' + domain + '/'
        completions.append(
            (
            domain,
            url + '${1:' + width + 'x' + height + '}'
            )
        )
        completions.append(
            (
            domain + ' (full version)',
            url + '${1:' + width + 'x' + height + '/' + background_color + '/' + text_color + '.' + file_ext + '?text=' + text + '}'
            )
        )

def pos(view, pos):
    point = view.sel()[0].begin()
    return view.substr(sublime.Region(point - pos, point))

def before(view, location):
    lineLocation = view.line(location)
    return view.substr(sublime.Region(lineLocation.a, location))

def get_before_text(view):
    point = view.sel()[0].begin()
    lineLocation = view.line(point)
    return view.substr(sublime.Region(lineLocation.a, point))

def is_trigger(text, syntax):
    text = text.lower()

    if syntax.lower().find(u'html'):
        search = re.search(r"(?:(?:^|\s))(?:src|poster|srcset)=[\"\']?$", text)
        if (search):
            return True

    for s in (u'html', u'css', u'less', u'sass', u'scss', u'stylus'):
        if syntax.lower().find(s):
            search = re.search(r"(?:(?:^|\s))url\([\"\']?$", text)
            if (search):
                return True

    return False

class imgHolder(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        syntax = view.settings().get('syntax')
        before_text = before(view, locations[0]);

        if is_trigger(before_text, syntax):
            return (completions, sublime.INHIBIT_EXPLICIT_COMPLETIONS)
        return
