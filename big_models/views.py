from django.shortcuts import render
from django.db.models import Sum

def links_list(request):
    links = AIModelLink.objects.all().order_by('-click_count', 'order')
    num_links = len(links)
    num_placeholders = 4 - (num_links % 4)  # 修复只剩 3 个时占满一行的需求
    if num_placeholders == 4:  # 如果刚好整除，不需要填充
        num_placeholders = 0
    placeholders = list(range(num_placeholders))
    total_clicks = AIModelLink.objects.aggregate(Sum('click_count'))['click_count__sum'] or 0  # 确保处理可能的 None 值
    return render(request, 'links/list.html', {'links': links, 'total_clicks': total_clicks,'placeholders': placeholders})

# 保存点击次数
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AIModelLink

@csrf_exempt
def increment_click_count(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        link_id = data.get('id')
        try:
            link = AIModelLink.objects.get(id=link_id)
            link.click_count += 1
            link.save()
            print(f"Updated click count for link {link_id}")  # 调试输出
            return JsonResponse({'status': 'success'})
        except AIModelLink.DoesNotExist:
            print(f"Link {link_id} not found")  # 调试输出
            return JsonResponse({'status': 'error', 'message': 'Link not found'})
    print("Invalid request")  # 调试输出
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})