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
        base_url = "https://security-monitor-git-chore-add-cors-support-lmopes-projects.vercel.app"

        data = {
            "descriptions": {
                "app_name": "Security Monitor",
                "app_description": "Monitors users attempt to access sensitive data",
                "app_url": base_url,
                "app_logo": (
                    "https://media.istockphoto.com/id/953520974/vector/"
                    "tick-mark-approved-icon-shield-vector-on-white-background.jpg?"
                    "s=2048x2048&w=is&k=20&c=PzcwFJsLFCrETZ2MU_Xw4wChwiS5O09bqFdTYkkRH5k="
                ),
                "background_color": "#fff"
            },
            "integration_category": "Monitoring & Logging",
            "integration_type": "interval",
            "is_active": True,
            "key_features": [
                (
                    "Real-time monitoring of user access attempts on secured endpoints,"
                    "including both anonymous and authenticated users."
                ),
                (
                    "Customizable settings to filter and track access details such as timestamp,"
                    "user activity thresholds, and anonymized user tracking."
                ),
            ],
            "permissions": {
                "monitoring_user": {
                    "always_online": True,
                    "display_name": "Access Monitor"
            }
            },
            "settings": [
                {
                    "label": "Monitor Anonymous user",
                    "type": "checkbox",
                    "required": True,
                    "default": "Yes"
                },
                {
                    "label": "Include timestamp for last user request",
                    "type": "checkbox",
                    "required": True,
                    "default": "Yes"
                },
                {
                    "label": "Access Attempt Threshold",
                    "type": "number",
                    "required": False,
                    "default": "5"
                },
                {
                    "label": "interval",
                    "type": "text",
                    "required": True,
                    "default": "* * * * *"
                }
            ],
            "tick_url": f"{base_url}/tick/",
            "target_url": "https://ping.telex.im/v1/return/"
        }

        return Response({"data": data}, status=status.HTTP_200_OK)

class Tick(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        run_background_task(request.data)
        return Response({"status": "accepted"}, status=status.HTTP_202_ACCEPTED)
