from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from django.utils import timezone

from .serializers import ApplicationSerializer, PracticeRecordSerializer
from .models import *

import json
from pathlib import Path
from django.conf import settings
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def ApplicationUploadView(request):
    if request.method == "GET":
        template_name = "application_upload.html"
        roles_path = Path(settings.BASE_DIR) / "interview" / "job_roles.json"
        with open(roles_path, "r", encoding="utf-8") as f:
            job_roles = json.load(f)
        return render(request, template_name, {"job_roles": job_roles, })
    
    elif request.method == "POST":
        template_name = "home.html"
        job_role = request.POST["job_role"]
        uploaded_file = request.FILES["resume"]
        file_content = uploaded_file.read().decode("utf-8")
        app = Application.objects.create(user=request.user, desired_role=job_role,)
        prompt = (
            f"I'm preparing for a {job_role} position. "
            f"Here is my resume:\n\n{file_content}\n\n"
            f"Please generate exactly {50} relevant interview questions, "
            "and return them **only** as a valid JSON object where each key is "
            "the question number (as a string) and each value is the question text. "
            "For example:\n"
            '{\n'
            '  "1": "First question?",\n'
            '  "2": "Second question?",\n'
            '  …\n'
            '}\n'
            "Do not include any markdown fences or extra commentary."
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert technical interview coach."},
                {"role": "user", "content": prompt}
            ]
        )

        raw = response.choices[0].message.content.strip()

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            lines = raw.strip("{} \n").split("\n")
            data = {}
            for line in lines:
                if ":" not in line: continue
                key, val = line.split(":", 1)
                key = key.strip().strip('"')
                val = val.strip().rstrip(',').strip().strip('"')
                data[key] = val
                data = {int(k): v for k, v in data.items()}

        for key, value in data.items():
            PracticeRecord.objects.create(
                application=app, 
                question_text=value,
                batch_number=key,
            )
        
        
        return JsonResponse({"application_id": app.id})


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def ApplicationReadView(request, application_id=None):
    apps = request.user.application_set.all()
    if not apps.exists():
        return redirect("application_upload")
    if application_id is None:
        first_id = apps.first().id
        return redirect("application_read", application_id=first_id)
    app = get_object_or_404(Application, id=application_id, user=request.user)
    if request.method == "GET":
        template_name="application_read.html"
        serializer = ApplicationSerializer(app)
        return render(request, template_name, {"apps": apps, "selected_app": serializer.data, })
    if request.method == "POST" and request.POST.get("delete") == "true":
        app.delete()
        return redirect("home")


@api_view(['POST', 'DELETE'])
def AnswerUpdateDeleteView(request):
    record = get_object_or_404(PracticeRecord, id=request.data.get('question_id'), application__user=request.user)
    text = request.data.get('answer_text')
    record.answer_text = text
    record.answered_at = timezone.now()
    record.save()
    serializer = PracticeRecordSerializer(record)
    
    return Response(serializer.data)

@api_view(['POST'])
def AnswerSubmitView(request):
    record = get_object_or_404(PracticeRecord, id=request.data.get('question_id'), application__user=request.user)
    text = request.data.get('answer_text')
    record.answer_text = text
    prompt = (
        "You are a stern, no-nonsense technical interviewer at a top firm. "
        "I will give you a question and a candidate’s answer. "
        "  90–100: Exceptional — complete, detailed, with examples.\n"
        "  70–89 : Good — covers main points, but could use examples or detail.\n"
        "  50–69 : Fair — basic understanding but lacks clarity or structure.\n"
        "  30–49 : Poor — significant omissions or misunderstandings.\n"
        "  0–29 : Unacceptable — incorrect or off-topic.\n\n"
        "Please evaluate the answer and return ONLY a JSON object with two fields:\n\n"
        "  • score: an integer between 0 and 100 (higher is better)\n"
        "  • feedback: a concise, constructive comment of **no more than 150 characters**\n\n"
        "Question:\n"
        f"{record.question_text}\n\n"
        "Answer:\n"
        f"{text}\n\n"
        "Respond with valid JSON, for example:\n"
        '{"score": 78, "feedback": "Good explanation of sync vs async. Next time, include an example of event loops to strengthen your answer."}'
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert technical interview coach."},
            {"role": "user", "content": prompt}
        ]
    )
    resp_text = response.choices[0].message.content.strip()
    try:
        data = json.loads(resp_text)
        score    = int(data.get("score", 0))
        feedback = data.get("feedback", "").strip()
    except Exception:
        return
    record.answered_at = timezone.now()
    record.score = score
    record.feedback = feedback
    record.is_scored = True
    record.save()
    serializer = PracticeRecordSerializer(record)
    
    return Response(serializer.data)


