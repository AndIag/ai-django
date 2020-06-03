from django.contrib import admin
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
