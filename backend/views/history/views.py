import json

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.dtos import BaseResponse
from backend.sentiment_analysis.classifier import classify
from backend.sentiment_analysis.analysis import TRUE_NEGATIVE, TRUE_POSITIVE, FALSE_NEGATIVE, FALSE_POSITIVE


@csrf_exempt
@api_view(['POST'])
def analyse(request):
    data = json.loads(request.body)
    stressor: str = data["stressor"]
    statement: str = data["statement"]

    if stressor is None:
        return BaseResponse(
            status=False,
            message="Please select stressor"
        )
    if statement is None:
        return BaseResponse(
            status=False,
            message="Please enter the statement to analyse"
        )
    result = classify(stressor, statement)
    return Response(data=BaseResponse(
        status=True,
        message=__get_response(result, stressor)
    ).__dict__, status=status.HTTP_200_OK)


def __get_response(result: str, stressor: str) -> str:
    if result == TRUE_POSITIVE:
        return f"This statement exhibit a sign of {stressor}, a {TRUE_POSITIVE}"

    if result == TRUE_NEGATIVE:
        return f"This statement contains the stressor used exhibit a sign of {stressor} but dose not" \
               f" reflect a ture expression of the stressor, a {TRUE_NEGATIVE}"

    if result == FALSE_POSITIVE:
        return f"This statement show some signs of negativity, but dose not contain the identified stressors " \
               f"relating to {stressor}, a {FALSE_POSITIVE}"

    if result == FALSE_NEGATIVE:
        return f"This statement dose not reelect any negativity, a {FALSE_NEGATIVE}"
