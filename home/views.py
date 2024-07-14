import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.http import require_POST
from pdf2docx import Converter
from docx2pdf import convert
from .models import ConvertedFile
import uuid

def generate_short_code():
    return str(uuid.uuid4())[:5]


@require_POST
def pdftoword(request):
    file = request.FILES.get('pdf_file')
    if file and file.name.endswith('.pdf'): 
        short_code = generate_short_code()
        converted_file = ConvertedFile(pdf_file=file, short_code=short_code)
        converted_file.save()


        filename = os.path.splitext(file.name)[0]
        docx_filename = filename.replace(" ", "_")
        docx_file_path = os.path.join(settings.MEDIA_ROOT, 'docx_files', docx_filename + '.docx')


        try:
            pdf_converter = Converter(converted_file.pdf_file.path, docx_file_path)
            pdf_converter.convert()

            converted_file.docx_file.name = os.path.join('pdf_files', docx_filename + '.docx')  # Add '.docx' extension here
            converted_file.save()

            return JsonResponse({'short_code': short_code})
        except Exception as e:
            return HttpResponse('Conversion failed or file not found', status=500)
    else:
        return HttpResponse('Invalid PDF file provided', status=400)

def wordtopdf(request):
    file = request.FILES.get('docx_file')
    if file and file.name.endswith('.docx'): 
        short_code = generate_short_code()
        converted_file = ConvertedFile(docx_file=file, short_code=short_code)
        converted_file.save()


        filename = os.path.splitext(file.name)[0]
        pdf_filename = filename.replace(" ", "_")
        pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'pdf_files', pdf_filename + '.pdf')


        try:
            docx_converter = convert(converted_file.pdf_file.path, pdf_file_path)
            docx_converter.convert()

            converted_file.pdf_file.name = os.path.join('docx_files', pdf_filename + '.pdf')  # Add '.docx' extension here
            converted_file.save()

            return JsonResponse({'short_code': short_code})
        except Exception as e:
            return HttpResponse('Conversion failed or file not found', status=500)
    else:
        return HttpResponse('Invalid PDF file provided', status=400)

def convert_form(request):
    return render(request, r'C:\\Users\\hp\\OneDrive\Desktop\BHARAT XR\\pdftoword\\pdftoword\\templates\\index.html')


def downloadpage(request, pk):
    converted_file = ConvertedFile.objects.get(short_code=pk)
    d = os.path.splitext(converted_file.docx_file.name)[0]
    prefix_to_remove = "pdf_files\\"
    if d.startswith(prefix_to_remove):
        d = d[len(prefix_to_remove):]
    print(d)
    return render(request, 'dq.html', {'hi': converted_file,'h':d})

