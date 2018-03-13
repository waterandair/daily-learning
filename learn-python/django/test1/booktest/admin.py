from django.contrib import admin
from booktest.models import BookInfo, HeroInfo
from django.contrib import admin


# 关联注册
# admin.StackedInline 内嵌方式； admin.TabularInline 表格方式
class HeroInfoInline(admin.TabularInline):
    model = HeroInfo
    extra = 2


class BookInfoAdmin(admin.ModelAdmin):
    # 列表页
    list_display = ['pk', 'btitle', 'bpub_date']
    list_filter = ['btitle']
    search_fields = ['btitle']
    list_per_page = 1

    # 添加/编辑页
    # 属性的先后顺序 和 fieldsets 不能同时指定
    # fields = ['bpub_date', 'btitle']
    # 属性分组
    fieldsets = [
        ('basic', {'fields': ['btitle']}),
        ('more', {'fields': ['bpub_date']})
    ]

    inlines = [HeroInfoInline]


class HeroInfoAdmin(admin.ModelAdmin):

    def gender(self):
        if self.hgender:
            return '男'
        else:
            return '女'
    gender.short_description = '性别'

    def hname(self):
        return self.hname

    hname.short_description = "姓名"

    list_display = ['id', 'hname', gender, 'hcontent']


admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)