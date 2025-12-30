from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from .models import BotUser, Question, TestAttempt, AttemptDetail, BotState
import openpyxl

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField()

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'full_name', 'username', 'created_at')
    search_fields = ('full_name', 'username')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'correct_answer', 'is_active')
    list_filter = ('is_active', 'correct_answer')
    search_fields = ('text',)
    change_list_template = "admin/question_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-excel/', self.import_excel),
        ]
        return my_urls + urls

    def import_excel(self, request):
        if request.method == "POST":
            form = ExcelImportForm(request.POST, request.FILES)
            if form.is_valid():
                excel_file = request.FILES["excel_file"]
                try:
                    wb = openpyxl.load_workbook(excel_file)
                    sheet = wb.active
                    count = 0
                    for row in sheet.iter_rows(min_row=2, values_only=True):
                        if not row[0]: continue
                        Question.objects.create(
                            text=row[0],
                            option_a=row[1],
                            option_b=row[2],
                            option_c=row[3],
                            option_d=row[4],
                            correct_answer=str(row[5]).lower(),
                            image=None # Handle image if needed later
                        )
                        count += 1
                    self.message_user(request, f"Successfully imported {count} questions")
                    return redirect("..")
                except Exception as e:
                    self.message_user(request, f"Error: {e}", level=messages.ERROR)
        
        form = ExcelImportForm()
        payload = {"form": form}
        return render(
            request, "admin/excel_form.html", payload
        )

@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'total_questions', 'created_at')
    list_filter = ('created_at',)

@admin.register(AttemptDetail)
class AttemptDetailAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'user_answer', 'is_correct')

@admin.register(BotState)
class BotStateAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'chat_id', 'state', 'updated_at')
