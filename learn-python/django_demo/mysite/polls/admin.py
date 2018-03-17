from django.contrib import admin
from polls.models import Question, Choice
# Register your models here.
# 快捷方式
# admin.site.register(Question)
# 自定义方式


class ChoiceInline(admin.TabularInline):
    """
    admin.StackedInline  普通模式
    admin.TabularInline 表格模式 节省页面空间
    """
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # 更改编辑页面字段的顺序
    # fields = ["pub_date", "question_text"]
    # 设置字段集       不能和 fields 同时定义
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('日期信息', {'fields': ['pub_date'], 'classes': ['collapse']})
    ]
    inlines = [ChoiceInline]
    # 列表页显示的内容, 可以添加model定义的变量和函数等等
    list_display = ("question_text", "pub_date", "was_published_recently")

    # 列表过滤
    list_filter = ['pub_date']

    # 搜索字段
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
