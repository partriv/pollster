from django.conf.urls.defaults import *
from pollster.conf import settings_local

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #(r'^pollster/', include('pollster.conf.urls')),
    # home page
    (r'^$', 'pollster.views.home.slug_handler'),
    

    # register/login sutff
    (r'^register/$', 'pollster.views.register.index'),
    (r'^register/checkname$', 'pollster.views.register.checkname'),
    (r'^register/thanks/$', 'pollster.views.register.thanks'),
    (r'^login/$', 'pollster.views.login.index'),
    (r'^login-block/$', 'pollster.views.login.login_block'),
    (r'^logout/$', 'pollster.views.profile.logout'),
    (r'^facebook-login/$', 'pollster.views.login.facebook_login'),
    (r'^facebook-connect/$', 'pollster.views.login.facebook_connect'),
    
    # profile
    (r'^profile/(?P<username>[^/]+)/$', 'pollster.views.profile.voted_on'),
    (r'^profile/(?P<username>[^/]+)/(?P<page_num>\d+)/$', 'pollster.views.profile.voted_on'),
    (r'^profile/(?P<username>[^/]+)/activity/$', 'pollster.views.profile.activity_home_index'),
    (r'^profile/(?P<username>[^/]+)/more-activity/$', 'pollster.views.profile.activity_index'),
    (r'^profile/(?P<username>[^/]+)/created/$', 'pollster.views.profile.created'),
    (r'^profile/(?P<username>[^/]+)/created/(?P<page_num>\d+)/$', 'pollster.views.profile.created'),
    (r'^profile/(?P<username>[^/]+)/commented/$', 'pollster.views.profile.commented'),
    (r'^profile/(?P<username>[^/]+)/commented/(?P<page_num>\d+)/$', 'pollster.views.profile.commented'),    
    (r'^profile/(?P<username>[^/]+)/not-finished/$', 'pollster.views.profile.not_finished'),
    (r'^profile/(?P<username>[^/]+)/not-finished/(?P<page_num>\d+)/$', 'pollster.views.profile.not_finished'),
    (r'^profile/(?P<username>[^/]+)/watching/$', 'pollster.views.profile.watching'),
    (r'^profile/(?P<username>[^/]+)/watching/(?P<page_num>\d+)/$', 'pollster.views.profile.watching'),
    (r'^profile/(?P<username>[^/]+)/edit/$', 'pollster.views.profile.edit'),
    (r'^profile/(?P<username>[^/]+)/pic/$', 'pollster.views.profile.pic'),
    (r'^profile/(?P<username>[^/]+)/voted-on/$', 'pollster.views.profile.voted_on'),
    (r'^profile/(?P<username>[^/]+)/voted-on/(?P<page_num>\d+)/$', 'pollster.views.profile.voted_on'),
    # mail stuff
    (r'^profile/(?P<username>[^/]+)/mail/$', 'pollster.views.profile.mail'),
    (r'^profile/(?P<username>[^/]+)/mail/view/$', 'pollster.views.profile.mail_view'),
    (r'^profile/(?P<username>[^/]+)/mail/view/(?P<page_num>\d+)/$', 'pollster.views.profile.mail_view'),
    (r'^profile/(?P<username>[^/]+)/mail/sent/$', 'pollster.views.profile.mail_sent'),
    (r'^profile/(?P<username>[^/]+)/mail/sent/(?P<page_num>\d+)/$', 'pollster.views.profile.mail_sent'),
    (r'^mark-mail-as-read/$', 'pollster.views.profile.mark_mail_read'),
    
    # settings    
    (r'^profile/(?P<username>[^/]+)/settings/$', 'pollster.views.user.usersettings.index'),
    (r'^profile/(?P<username>[^/]+)/change-password/$', 'pollster.views.profile.change_password'),
    (r'^profile/settings/update-setting/$', 'pollster.views.user.usersettings.update_settings'),
    (r'^profile/$', 'pollster.views.profile.index'),
    (r'^profile/search/(?P<field>[^/]+)/(?P<many_to_many>[^/]+)/$', 'pollster.views.pollajax.search_profile_tags'),
    (r'^friend/$', 'pollster.views.profile.friend'),
    (r'^forgot-password/$', 'pollster.views.profile.forgot_password'),
    (r'^forgot-username/$', 'pollster.views.profile.forgot_username'),
    
    #  poll creation
    (r'^create-poll/$', 'pollster.views.pollcreate.index'),
    (r'^create-poll/answers/(?P<poll_url>[^/]+)/$', 'pollster.views.pollcreate.answers'),
    #(r'^create-poll/tags/(?P<poll_url>[^/]+)/$', 'pollster.views.pollcreate.tags'),
    (r'^create-poll/finish/(?P<poll_url>[^/]+)/$', 'pollster.views.pollcreate.finish'),
    #(r'^create-poll/description/(?P<poll_url>[^/]+)/$', 'pollster.views.pollcreate.description'),
    (r'^create-poll/search/$', 'pollster.views.pollajax.search'),
    (r'^create-poll/load-inactive/$', 'pollster.views.pollajax.get_inactive'),
    (r'^create-poll/add-answer/$', 'pollster.views.pollajax.add_answer'),
    (r'^create-poll/delete-answer/$', 'pollster.views.pollajax.delete_answer'),
    (r'^create-poll/add-tag/$', 'pollster.views.pollajax.add_tag'),
    (r'^create-poll/delete-poll-tag/$', 'pollster.views.pollajax.delete_poll_tag'),
    (r'^create-poll/search-tags/$', 'pollster.views.pollajax.search_tags'),
    (r'^create-poll/allow-user-answer/(?P<poll_id>\d+)/(?P<choice>\d+)/$', 'pollster.views.pollajax.set_allow_user_answer'),
    (r'^create-poll/poll-active/(?P<poll_id>\d+)/(?P<choice>\d+)/$', 'pollster.views.pollajax.poll_active'),
    (r'^create-poll/set-main-file/(?P<poll_id>\d+)/(?P<poll_file_id>\d+)/$', 'pollster.views.pollajax.set_main_file'),
    (r'^create-poll/delete-file/(?P<poll_id>\d+)/(?P<poll_file_id>\d+)/$', 'pollster.views.pollajax.delete_file'),
    (r'^create-poll/reload-files/(?P<poll_id>\d+)/$', 'pollster.views.pollajax.reload_files'),
    (r'^create-poll/show-video/(?P<poll_id>\d+)/$', 'pollster.views.pollajax.show_video'),
    (r'^create-poll/edit-title/$', 'pollster.views.pollajax.edit_title'),
    
    # poll viewing
    (r'^view-poll/demographic_form/$',                          'pollster.views.pollajax.demographic_form'),
    (r'^view-poll/demographic_value_form/$',                    'pollster.views.pollajax.demographic_value_form'),
    (r'^view-poll/watch-poll/$',                                'pollster.views.pollview.watch_poll'),
    (r'^view-poll/answer_poll/$',                               'pollster.views.pollview.answer_poll'),
    (r'^view-poll/flag-inappropriate/$',                        'pollster.views.pollview.flag_inappropriate'),
    (r'^view-poll/answer-suggest/$',                            'pollster.views.pollview.answer_suggest'),
    (r'^view-poll/new-answer/$',                                'pollster.views.pollview.new_answer'),
    (r'^view-poll/get-spillover-answers/$',                     'pollster.views.pollview.get_spillover_answers'),
    (r'^view-poll/get-voters/$',                                'pollster.views.pollview.get_voters'),
    (r'^view-poll/(?P<poll_url>[^/]+)/$',                       'pollster.views.pollview.index'),
    (r'^preview-poll/(?P<poll_url>[^/]+)/$',                    'pollster.views.pollview.preview'),
    (r'^view-poll/(?P<poll_url>[^/]+)/(?P<demographics>.+)/$',  'pollster.views.pollview.index'),
    (r'^view-poll/$',                                           'pollster.views.pollview.index'),    
    (r'^delete-comment/(?P<object_id>\d+)/$',                   'pollster.views.pollajax.delete_comment'),
    (r'^email-on-comment/(?P<object_id>\d+)/$',                 'pollster.views.pollajax.email_on_comment'),
    
    
    # search
    (r'^search/$', 'pollster.views.search.index'),
    (r'^search/terms/(?P<search_terms>[^/]+)/$',                        'pollster.views.search.doSearch'),
    (r'^search/(?P<search_terms>[^/]+)/$',                              'pollster.views.search.index'),
    (r'^search/(?P<search_terms>[^/]+)/(?P<page_num>\d+)/$',            'pollster.views.search.index'),
    (r'^search/(?P<search_terms>[^/]+)/sort/votes/$',                   'pollster.views.search.index_sort_votes'),
    (r'^search/(?P<search_terms>[^/]+)/sort/votes/(?P<page_num>\d+)/$', 'pollster.views.search.index_sort_votes'),
    (r'^search/(?P<search_terms>[^/]+)/sort/comments/$',                'pollster.views.search.index_sort_comments'),
    (r'^search/(?P<search_terms>[^/]+)/sort/comments/(?P<page_num>\d+)/$', 'pollster.views.search.index_sort_comments'),
    (r'^search/(?P<search_terms>[^/]+)/sort/date/$',                    'pollster.views.search.index_sort_date'),
    (r'^search/(?P<search_terms>[^/]+)/sort/date/(?P<page_num>\d+)/$',  'pollster.views.search.index_sort_date'),
    (r'^tag/$',                                                         'pollster.views.search.tag'),
    (r'^tag/(?P<tag_name>[^/]+)/$',                                     'pollster.views.search.tag'),
    (r'^tag/(?P<tag_name>[^/]+)/(?P<page_num>\d+)/$',                   'pollster.views.search.tag'),
    (r'^tag/(?P<tag_name>[^/]+)/sort/votes/$',                          'pollster.views.search.tag_sort_votes'),
    (r'^tag/(?P<tag_name>[^/]+)/sort/votes/(?P<page_num>\d+)/$',        'pollster.views.search.tag_sort_votes'),
    (r'^tag/(?P<tag_name>[^/]+)/sort/comments/$',                       'pollster.views.search.tag_sort_comments'),
    (r'^tag/(?P<tag_name>[^/]+)/sort/comments/(?P<page_num>\d+)/$',     'pollster.views.search.tag_sort_comments'),
    (r'^tag/(?P<tag_name>[^/]+)/sort/date/$',                           'pollster.views.search.tag_sort_date'),
    (r'^tag/(?P<tag_name>[^/]+)/sort/date/(?P<page_num>\d+)/$',         'pollster.views.search.tag_sort_date'),
            
    # misc
    
    (r'^contact/$', 'pollster.views.static.contact'),
    (r'^about/$',   'pollster.views.static.about'),
    (r'^error/$',   'pollster.views.error.index'),
    (r'^sitemap/$',    'pollster.views.sitemap.sitemap'),
    
    (r'^xd_receiver.htm$',  'pollster.views.static.xd_receiver'),
    (r'^robots.txt$',       'pollster.views.static.robots'),
    (r'^sitemap.xml$',      'pollster.views.sitemap.index'),
    (r'^delorie.htm$',      'pollster.views.static.delorie'),
    (r'^favicon.ico$',      'pollster.views.static.favicon'),
    
    # comments schtuff
    (r'^threadedcomments/', include('threadedcomments.urls')),
    (r'^poll-comments/update-count/', "pollster.views.pollajax.update_comment_count"),
    (r'^poll-comments/update-comments/', "pollster.views.pollajax.update_comment"),
    
    # admin
    (r'^admin/mailusers/', "pollster.views.admin.admin.mailusers"),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
    
    # INDEX SLUG HANDLER
    (r'^(?P<page_num>\d+)/$', 'pollster.views.home.slug_handler'),
    (r'^(?P<slug>[^/]+)/$', 'pollster.views.home.slug_handler'),
    (r'^(?P<slug>[^/]+)/(?P<page_num>\d+)/$', 'pollster.views.home.slug_handler'),
    (r'^(?P<slug>[^/]+)/(?P<time_length>[^/]+)/$', 'pollster.views.home.slug_time'),
    (r'^(?P<slug>[^/]+)/(?P<time_length>[^/]+)/(?P<page_num>\d+)/$', 'pollster.views.home.slug_time'),
)

# static server
if settings_local.STATIC_SERVER:
    urlpatterns += patterns('', (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings_local.MEDIA_ROOT}))
if settings_local.DEBUG:
    urlpatterns += patterns('', (r'^test/$',    'pollster.views.test.index'))
    