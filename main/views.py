import os
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_protect

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from PIL import Image, ImageDraw, ImageFont
import tempfile

from .forms import StudentListForm, ScaffoldForm
from .models import Student, Scaffold

COHORT_LOOKUP = {
    'F': 'Feb Standard',
    'A': 'Aug Standard',
    'M': 'May Express',
    'O': 'October Express'
}

CLASS_LOOKUP = {
    'F': {str(i): f'IT.f{i}' for i in range(1, 12)},
    'A': {str(i): f'IT.a{i}' for i in range(1, 12)},
    'M': {str(i): f'IT.m{i}' for i in range(1, 12)},
    'O': {str(i): f'IT.o{i}' for i in range(1, 12)},
}

MODULE_LOOKUP = {
    'WC': 'Web Coding',
    'CE': 'Computer Essentials',
    'IS': 'Information Systems',
    'PR': 'Programming',
    'SI': 'Social Issues'
}


# Create your views here.
def home(request):
    year_choices = Student.objects.order_by().values('year_choices').distinct()

    year_choices_list = [item['year_choices'] for item in year_choices]

    return render(request, 'main/index.html', {'years': year_choices_list})


def get_cohort_options(request):
    year_choice = request.GET.get('year', '')
    cohort_choices = Student.objects.filter(year_choices=year_choice).order_by().values('cohort_choices').distinct()
    cohort_choices = list(cohort_choices)
    cohort_choices = [item['cohort_choices'] for item in cohort_choices]

    cohorts = [
        {
            'id': item,
            'display': COHORT_LOOKUP[item]
        } for item in cohort_choices]

    return JsonResponse(cohorts, safe=False)


def get_class_options(request):
    year_choice = request.GET.get('year', '')
    cohort_choice = request.GET.get('cohort', '')

    # a list of the distinct modules represented in the uploaded scaffolds
    scaffold_module_choices = Scaffold.objects.filter(
        year_choices=year_choice,
        cohort_choices=cohort_choice).order_by().values(
        'module').distinct()

    # all of the uploaded scaffolds for given year and cohort
    scaffolds = Scaffold.objects.filter(
        year_choices=year_choice,
        cohort_choices=cohort_choice,
    )

    # Make a list of module choices
    module_choices = [
        {"text": f"{MODULE_LOOKUP[module_choice['module']]}",
         "children": [{"id": s.pk, "text": os.path.basename(s.pdf.name)} for s in scaffolds.filter(module=module_choice['module'])]} for module_choice in scaffold_module_choices]

    class_choices = Student.objects.filter(year_choices=year_choice, cohort_choices=cohort_choice).order_by().values(
        'class_number').distinct()

    class_choices = [item['class_number'] for item in list(class_choices)]

    classes = [
        {
            'id': item,
            'display': CLASS_LOOKUP[cohort_choice][item]
        } for item in class_choices]

    return JsonResponse({
        'classes': classes,
        'scaffold': module_choices
    }, safe=False)


@csrf_protect
def upload_student_list(request):
    # POST to change
    if request.method == 'POST':
        form = StudentListForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # List of years

            return redirect('index')

    else:
        form = StudentListForm()
        # make list of years

    return render(request, 'main/upload.html', {
        'form': form
    })


@csrf_protect
def upload_scaffold(request):
    # POST to change
    if request.method == 'POST':
        form = ScaffoldForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('index')

    else:
        form = ScaffoldForm()
        # make list of years

    return render(request, 'main/upload.html', {
        'form': form
    })


def get_students(request):
    year_choice = request.GET.get('year', '')
    cohort_choice = request.GET.get('cohort', '')
    class_num = request.GET.get('class_num', '')

    students = Student.objects.filter(
        year_choices=year_choice,
        cohort_choices=cohort_choice,
        class_number=class_num
    )

    students_list = [(std.pk, str(std)) for std in students]

    cls = {"text": f"{CLASS_LOOKUP[cohort_choice][class_num]}",
           "children": []
           }
    for student_id, student_name in students_list:
        cls['children'].append({'id': student_id, 'text': student_name})

    return JsonResponse({"results": [cls]}, safe=False)


def wm_text(student_names, scaffold):

    width, height = 595, 842
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 28, encoding="unic")
    output = PdfFileWriter()

    for student in student_names:
        notes = PdfFileReader(open(scaffold, 'rb'))
        composite = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        t_width, t_height = font.getsize(student)
        # 1bit mask canvas to fit text
        mask = Image.new('1', (t_width, t_height))

        draw = ImageDraw.Draw(mask)

        draw.text((0, 0), student, fill=1, font=font)
        mask = mask.rotate(45, expand=True)

        composite.paste(mask, (0, 0), mask=mask)

        with tempfile.NamedTemporaryFile(mode='rb', delete=True, suffix=".png") as png:

            composite.save(png.name, format='PNG')
            with tempfile.NamedTemporaryFile(mode='rb', delete=True, suffix=".pdf") as pdf:
                imgDoc = canvas.Canvas(pdf.name, pagesize=A4)
                imgDoc.drawImage(png.name, 0, 0, mask='auto')
                imgDoc.save()
                watermark = PdfFileReader(pdf.name).getPage(0)

                for page_no in range(0, notes.numPages):
                    notes_page = notes.getPage(page_no)
                    notes_page.mergePage(watermark)
                    output.addPage(notes_page)

    output.write(open('watermarked.pdf', 'wb'))

    try:
        with open('watermarked.pdf', 'rb') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
            return response

    except FileNotFoundError:
        return HttpResponseNotFound('The requested pdf was not found in our server.')


def make_watermark(request):
    scaffold_id = request.GET.get('scaffold', '')
    students = request.GET.get('students', '')

    scaffold = Scaffold.objects.get(id=scaffold_id)
    student_ids = students.split(" ")[:-1]

    sn = [str(Student.objects.get(id=std_id)) for std_id in student_ids]
    return wm_text(sn, scaffold=scaffold.pdf.path)