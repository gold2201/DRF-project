import os

from django.http import FileResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from loveshopSite.settings import BASE_DIR


class LogsView(APIView):
    @extend_schema(
        summary='Show logs',
        description='Show logs. If logs are filtered only by date, the log will be downloaded to your computer. If additional filtering by logging levels is set, a list will be sent.',
    )
    def get(self, request):
        filter_by_date = request.query_params.get('filter_by', None)
        filter_by_level = request.query_params.get('filter_by_level', None)
        all_files = os.listdir(BASE_DIR / 'logs')
        if filter_by_date:
            log_file = [file for file in all_files if file.endswith(f'.{filter_by_date}')]
            if not log_file:
                return Response({'error': 'There are no logs for this date.'}, status=status.HTTP_404_NOT_FOUND)
            log_file=log_file[0]
        else:
            log_file = 'app.log'

        path = BASE_DIR / 'logs' / log_file

        if filter_by_level:
            with open(path, 'r') as file:
                response = [line for line in file if f'] {filter_by_level} ' in line]
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = FileResponse(open(path, 'rb'))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = f'attachment; filename={log_file}'
            return response





