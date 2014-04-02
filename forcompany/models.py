from django.db import models
from django.core.urlresolvers import reverse

class CompanyInfo(models.Model):
    title = models.TextField()
    position = models.TextField()
    nearby_station = models.TextField()
    description = models.TextField()
    preparation_material = models.TextField()
    facility = models.TextField()

    class1_count = models.TextField()
    class1_price = models.TextField()
    class2_count = models.TextField()
    class2_price = models.TextField()
    class3_count = models.TextField()
    class3_price = models.TextField()
    class4_count = models.TextField()
    class4_price = models.TextField()
    class5_count = models.TextField()
    class5_price = models.TextField()
    class6_count = models.TextField()
    class6_price = models.TextField()

    # teacher_image = models.ImageField(upload_to = 'pic_folder/')
    teacher_image = models.ImageField(upload_to = 'pic_folder/', default = '../static/no.jpg')
    teacher_name = models.TextField()
    teacher_career = models.TextField()

    curriculum1_time = models.TextField()
    curriculum1_preparation_material = models.TextField()
    curriculum1_class_description = models.TextField()
    curriculum1_class_detail_description = models.TextField()
    curriculum2_time = models.TextField()
    curriculum2_preparation_material = models.TextField()
    curriculum2_class_description = models.TextField()
    curriculum2_class_detail_description = models.TextField()
    curriculum3_time = models.TextField()
    curriculum3_preparation_material = models.TextField()
    curriculum3_class_description = models.TextField()
    curriculum3_class_detail_description = models.TextField()
    curriculum4_time = models.TextField()
    curriculum4_preparation_material = models.TextField()
    curriculum4_class_description = models.TextField()
    curriculum4_class_detail_description = models.TextField()
    curriculum5_time = models.TextField()
    curriculum5_preparation_material = models.TextField()
    curriculum5_class_description = models.TextField()
    curriculum5_class_detail_description = models.TextField()
    curriculum6_time = models.TextField()
    curriculum6_preparation_material = models.TextField()
    curriculum6_class_description = models.TextField()
    curriculum6_class_detail_description = models.TextField()
    curriculum7_time = models.TextField()
    curriculum7_preparation_material = models.TextField()
    curriculum7_class_description = models.TextField()
    curriculum7_class_detail_description = models.TextField()
    curriculum8_time = models.TextField()
    curriculum8_preparation_material = models.TextField()
    curriculum8_class_description = models.TextField()
    curriculum8_class_detail_description = models.TextField()

    refund_info = models.TextField()

    class Meta:
        ordering = ('id',)
        # unique_together = ('list', 'text' )

    def __str__(self):
        return self.title