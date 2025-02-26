from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class AIModelLink(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)
    click_count = models.IntegerField(default=0)  # 新增点击次数字段

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['click_count', 'order']  # 按点击次数排序

@receiver(pre_save, sender=AIModelLink)
def set_order(sender, instance, **kwargs):
    if instance.id is None:  # 检测是否是创建新记录
        max_order = AIModelLink.objects.aggregate(models.Max('order'))['order__max']
        instance.order = (max_order or 0) + 1