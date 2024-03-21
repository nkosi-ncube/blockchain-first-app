from django.shortcuts import render
from django.http import JsonResponse
from .models import Block
from django.views.decorators.csrf import csrf_exempt
import hashlib
import json


def home(request):
    """
    my home page views
    """
    return render(request,"blockchain.html")

def mine_block(request):
    if request.method == "POST":
        data = json.loads(request.body)
        previous_block = Block.objects.latest("index")
        new_block_index = previous_block.index+1
        new_block_data = data.get('data')
        new_block_previous_hash = previous_block.hash

        new_block =Block.objects.create(
            index = new_block_index,
            data = new_block_data,
            previous_hash = new_block_previous_hash
        )

        response = {
            'message':'A new block is MINED',
            'index':new_block.index,
            'timestamp':str(new_block.timestamp),
            'data':new_block_data,
            'previous_hash':new_block.previous_hash,
            'hash':new_block.hash
        }

        return JsonResponse(response)
    
@csrf_exempt
def display_chain(request):
    if request.method =="GET":
        chain = Block.objects.all().order_by('index')
        chain_data=[]
        for block in chain:
            chain_data.append({
                'index':block.index,
                'timestamp':str(block.timestamp),
                'data':block.data,
                'previous_hash':block.previous_hash,
                'hash':block.hash
            })
        return JsonResponse({'chain':chain_data})
    
def validate_chain(request):
    if request.method =="GET":
        chain = Block.objects.all().order_by('index')
        previous_block = None
        valid = True
        for block in chain:
            if previous_block:
                if block.previous_hash != previous_block.hash:
                    valid =False
                    break
                if block.hash != block.calculate_hash():
                    valid =False
                    break
                previous_block = block
            if valid:
                response = {'message':'The BlockChain is valid'}
            else:
                response={'message':'The Blockchain is not valid'}

            return JsonResponse(response)