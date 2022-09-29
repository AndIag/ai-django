from abc import abstractmethod

from django.contrib import admin
from django.db.models.functions import ExtractYear
from django.http import HttpResponseRedirect


class StampedModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return super(StampedModelAdmin, self).get_readonly_fields(request, obj) + ('creation_date',)


class AuditedModelAdmin(StampedModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return super(AuditedModelAdmin, self).get_readonly_fields(request, obj) + ('created_by',)


class TraceableModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return super(TraceableModelAdmin, self).get_readonly_fields(request, obj) \
               + ('from_date', 'to_date', 'is_active')

    def response_change(self, request, obj):
        if "_unsubscribe" in request.POST:
            obj.delete()
            return HttpResponseRedirect(".")

        return super(TraceableModelAdmin, self).response_change(request, obj)


class ReadOnlyTabularInline(admin.TabularInline):
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class YearFilter(admin.SimpleListFilter):
    title = 'year'
    parameter_name = 'year'

    @property
    @abstractmethod
    def model(self):
        raise NotImplementedError

    def lookups(self, request, model_admin):
        year_list = self.model.objects \
            .annotate(y=ExtractYear('date')).order_by('y') \
            .values_list('y', flat=True) \
            .distinct()
        return [(str(y), str(y)) for y in year_list]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(date__year=self.value())
        return queryset
