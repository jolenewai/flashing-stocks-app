from django.urls import path
import site_admin.views

urlpatterns = [
    path('', site_admin.views.admin_homepage, name="admin_homepage"),
    path('category/add', site_admin.views.add_category, name="add_category"),
    path(
        'category/edit/<category_id>',
        site_admin.views.edit_category,
        name="edit_category"
        ),
    path(
        'category/delete/<category_id>',
        site_admin.views.delete_category,
        name="delete_category"
    ),
    path('tags/add', site_admin.views.add_tags, name="add_tags"),
    path('tags/edit/<tag_id>', site_admin.views.edit_tag, name="edit_tag"),
    path('tags/delete/<tag_id>', site_admin.views.delete_tag, name="delete_tag")
]