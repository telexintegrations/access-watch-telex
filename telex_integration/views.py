from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .utils import run_background_task

class GetIntegrationJson(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        scheme = request.scheme
        host = request.get_host()
        #base_url = f"{scheme}://{host}"
        #vercel_base_url = "https://security-monitor-git-chore-add-cors-support-lmopes-projects.vercel.app"
        render_base_url = "https://access-watch.onrender.com"

        data = {
            "data": {
                "date": {
                "created_at": "2025-02-18",
                "updated_at": "2025-02-18"
                },
                "descriptions": {
                "app_name": "Access Watch",
                "app_description": "Monitors users attempt to access sensitive data",
                "app_logo": "https://media.istockphoto.com/id/953520974/vector/tick-mark-approved-icon-shield-vector-on-white-background.jpg?s=2048x2048&w=is&k=20&c=PzcwFJsLFCrETZ2MU_Xw4wChwiS5O09bqFdTYkkRH5k=",
                "app_url": render_base_url,
                "background_color": "#fff"
                },
                "is_active": True,
                "integration_category": "Monitoring & Logging",
                "integration_type": "interval",
                "key_features": [
                "Customizable settings to filter and track access details such as timestamp user activity thresholds",
                "and anonymized user tracking."
                ],
                "author": "Muhammed",
                "settings": [
                {
                    "label": "interval",
                    "type": "text",
                    "required": True,
                    "default": "* * * * *"
                },
                {
                    "label": "Access Attempt Threshold",
                    "type": "number",
                    "required": True,
                    "default": "5"
                },
                {
                    "label": "Include timestamp for last user request",
                    "type": "checkbox",
                    "required": True,
                    "default": "Yes"
                },
                {
                    "label": "Monitor Anonymous user",
                    "type": "checkbox",
                    "required": True,
                    "default": "Yes"
                }
                ],
                "target_url": "",
                "tick_url": f"{render_base_url}/tick/"
            }
            }

        return Response(data, status=status.HTTP_200_OK)

class Tick(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        run_background_task(request.data)
        return Response({"status": "accepted"}, status=status.HTTP_202_ACCEPTED)
