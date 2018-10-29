from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from arclight.models import NLUModel, Intent
from bson.objectid import ObjectId
from arclight.utils import NLUModelManager, NLUManagerBoundarie
import time

nlu_model_boundarie = NLUManagerBoundarie()

class TrainModelView(APIView):
    def post(self, request):
        try:
            start_time = time.time()
            _id = ObjectId( request.data['model_id'] )
            nlu_model = NLUModel.objects.get(_id = _id)
            nlu_model_manager = NLUModelManager(nlu_model)
            nlu_model_manager.train()
            elapsed_time = time.time() - start_time
        except Exception as e:
            print("{}: {}".format(type(e), e))
            return JsonResponse({"status":"fail", "message":e.__str__()})
        # success
        return JsonResponse({
            "status":"success",
            "message":"The model was trained successfuly",
            "time":elapsed_time
        })


class ParseMessageView(APIView):
    def post(self, request):
        try:
            _id = ObjectId( request.data['model_id'] )
            message = request.data['message']
            nlu_model_manager = nlu_model_boundarie.getNluManager(_id.__str__())
            result = nlu_model_manager.parse(message)
        except Exception as e:
            print("{}: {}".format(type(e), e))
            return JsonResponse({"status":"fail", "message":e.__str__()})

        return JsonResponse({
            "result": result
        })
