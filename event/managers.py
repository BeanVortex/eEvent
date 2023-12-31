from django.db.models import Manager

class EventManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter()
    def getAllByOrganizer(self, organizer):
        return super().get_queryset().filter(organizer_user=organizer)
    def getById(self, id):
        return super().get_queryset().get(id=id)
    def getByOrganizerAndId(self, organizer, id):
        return super().get_queryset().get(organizer_user=organizer, id=id)
    def allTitleContains(self, title):
        return super().get_queryset().get(title__contains=title)
    

class DiscountManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter()
    def getById(self, id):
        return super().get_queryset().get(id=id)
    def getAllByOrganizer(self, organizer):
        return super().get_queryset().filter(organizer_user=organizer)
    def getByOrganizerAndId(self, organizer, id):
        return super().get_queryset().get(organizer_user=organizer, id=id)
    def getByCode(self, code):
        return super().get_queryset().get(code=code)