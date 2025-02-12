from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializers import DocumentUploadSerializer, QuerySerializer
from .utils import process_document, search_documents


class UploadDocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary',
                        'description': 'Document file to upload',
                    }
                }
            }
        },
        responses={200: OpenApiTypes.BINARY},
        description="Upload a document file."
    )
    def post(self, request):
        serializer = DocumentUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data["file"]
            result = process_document(file)
            return Response(result)
        return Response(serializer.errors, status=400)


class SearchDocumentView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="query", 
                type=str, 
                description="El término de búsqueda que se utilizará para encontrar documentos.",
                required=True
            ),
            OpenApiParameter(
                name="limit", 
                type=int, 
                description="Número máximo de resultados a devolver. (Opcional)",
                required=False,
                default=10
            )
        ],
        responses={200: OpenApiTypes.OBJECT},
        description="Busca documentos en Elasticsearch usando el término de búsqueda proporcionado y devuelve los resultados."
    )
    def get(self, request):
        serializer = QuerySerializer(data=request.query_params)
        if serializer.is_valid():
            query = serializer.validated_data["query"]
            results = search_documents(query)
            return Response(results)
        return Response(serializer.errors, status=400)