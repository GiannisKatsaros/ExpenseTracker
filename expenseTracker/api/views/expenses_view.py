from rest_framework.views import APIView

# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from api.services import MailService, HtmlCrawlService
from api.serializer import ExpenseSerializer
import environ
import os

# from rest_framework import status


class ExpensesView(APIView):
    def __init__(self):
        env = environ.Env(DEBUG=(bool, False))
        django_env = env("DJANGO_ENV", default="development")
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        environ.Env.read_env(os.path.join(base_dir, f".env.{django_env}"))
        self.env = env

    def get(self, request, *args, **kwargs):
        action = kwargs.get("action", None)
        if action == "import_expenses":
            return self.import_expenses(request)
        return Response({"detail": "Invalid action"}, status=400)

    def import_expenses(self, request):
        mail_service = MailService()
        messages = mail_service.get_emails_from_sender(self.env("EMAIL_PIRAEUS"))
        imports = []
        for msg in messages:
            try:
                message = mail_service.get_email_message(msg)
                crawl = HtmlCrawlService.crawl_piraeus(message)
                imports.append(crawl)
                mail_service.mark_as_deleted(msg)
            except Exception as e:
                print(f"Error processing message {msg}: {e}")
        if imports:
            serializer = ExpenseSerializer(data=imports, many=True)
            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        serializer.save()
                        mail_service.delete_marked_emails()
                        return Response(serializer.data)
                except Exception as e:
                    print(f"Error saving expenses: {e}")
                    return Response(
                        {"detail": "Error saving expenses."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"detail": "No emails to import."}, status=status.HTTP_204_NO_CONTENT
        )
