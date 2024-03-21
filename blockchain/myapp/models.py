from django.db import models
import hashlib
import json
import datetime

class Block(models.Model):
    index = models.IntegerField()
    timestamp = models.DateTimeField(default=datetime.datetime.now())
    data = models.TextField()
    previous_hash =models.CharField(max_length=250)
    hash=models.CharField(max_length=250)


    def calculate_hash(self):
        block_string=json.dumps({
            "index":self.index,
            "timestamp":str(self.timestamp),
            "data":self.data,
            "previous_hash":self.previous_hash
        },sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def save(self,*args,**kwargs):
        if not self.hash:
            self.hash = self.calculate_hash()
        super(Block,self).save(*args,**kwargs)

    def __str__(self) -> str:
        return f"Block {self.index}"
