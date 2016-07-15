from django.http import HttpResponse
from models import Coterie
from home.models import User
from django.contrib.auth import get_user
from django.shortcuts import render, redirect



# from django.contrib.auth import get_user
# from django.http import HttpResponse
# from django.shortcuts import render
# import os
# import zipfile
# #from unrar import rarfile
# #from wand.image import Image
# from file_viewer import models





def handle_create_coterie(request):
    coterie = Coterie()
    coterie.name = request.POST["coterie_name"]
    coterie.description = request.POST["coterie_description"]
    coterie.save()
    coterie.administrators.add(get_user(request))
    return HttpResponse()


def handle_apply_coterie(request):
    coterie = Coterie.objects.get(id=request.POST["coterie_id"])
    applicant = get_user(request)
    if applicant not in coterie.members.all() and applicant not in coterie.administrators.all():
        coterie.applicants.add(applicant)
        coterie.save()
    return redirect("user_dashboard")


def handle_join_coterie(request):  
    coterie = Coterie.objects.get(id=request.POST["coterie_id"])
    if get_user(request) in coterie.administrators.all():
        applicant = User.objects.get(id=request.POST["applicant_id"])
        coterie.applicants.remove(applicant)
        if request.POST["decision"] == "accept":
            coterie.members.add(applicant)
        elif request.POST["decision"] == "refuse":
            pass;
        coterie.save()
        context = {
            "current_user": get_user(request),
            "coterie": coterie,
            "page_type": "administrated_coterie_page",
        }
        return render(request, "user_dashboard/administrated_coterie_page.html", context)
    else: 
        return HttpResponse("<h1>Sorry, you are not an administrator</h1>")


def handle_quit_coterie(request):
    coterie = Coterie.objects.get(id=request.POST["coterie_id"])
    user = get_user(request)
    if user in coterie.members.all():
        coterie.members.remove(user)
        coterie.save()
    return redirect("user_dashboard")


def handle_delete_coterie(request):
    coterie = Coterie.objects.get(id=request.POST["coterie_id"])
    user = get_user(request)
    if user in coterie.administrators.all():
        coterie.delete()
    return redirect("user_dashboard")





# def display_coterie_file_viewer_page(request):

#     if request.method == "POST":
#         if request.POST["operation"] == "like_comment":
#             comment = models.CoterieComment.objects.get(id=int(request.POST["comment_id"]))
#             comment.num_like += 1
#             comment.save()
#             return HttpResponse()

#         elif request.POST["operation"] == "like_annotation":
#             annotation = models.CoterieAnnotation.objects.get(id=int(request.POST["annotation_id"]))
#             annotation.num_like += 1
#             annotation.save()
#             return HttpResponse()

#         elif request.POST["operation"] == "refresh":
#             document = models.CoterieDocument.objects.get(id=int(request.POST["document_id"]))

#             context = {
#                 "document": document,
#                 "comments": document.comment_set.order_by("-post_time"),
#             }

#             return render(request, "file_viewer/comment_viewer_subpage.html", context)

#         elif request.POST["operation"] == "comment":
#             document = models.CoterieDocument.objects.get(id=int(request.POST["document_id"]))
#             comment = models.CoterieComment()
#             comment.content = request.POST["comment_content"]
#             comment.commenter = get_user(request)
#             comment.document_this_comment_belongs = document

#             if request.POST.has_key("reply_to_comment_id"):
#                 comment.reply_to_comment = models.CoterieComment.objects.get(id=int(request.POST["reply_to_comment_id"]))

#             comment.save()

#             context = {
#                 "document": document,
#                 "comments": document.comment_set.order_by("-post_time"),
#             }

#             return render(request, "file_viewer/comment_viewer_subpage.html", context)

#         elif request.POST["operation"] == "annotate":
#             document = models.CoterieDocument.objects.get(id=int(request.POST["document_id"]))
#             annotation = models.CoterieAnnotation()
#             annotation.content = request.POST["annotation_content"]
#             annotation.annotator = get_user(request)
#             annotation.document_this_annotation_belongs = document
#             annotation.page_index = request.POST["page_id"].split("_")[2]
#             annotation.height_percent = request.POST["height_percent"]
#             annotation.width_percent = request.POST["width_percent"]
#             annotation.top_percent = request.POST["top_percent"]
#             annotation.left_percent = request.POST["left_percent"]
#             annotation.frame_color = request.POST["frame_color"]
#             annotation.save()

#             context = {
#                 "document": document,
#                 "annotations": document.annotation_set.order_by("page_index"),
#                 "new_annotation_id": annotation.id,
#             }

#             return render(request, "file_viewer/annotation_viewer_subpage.html", context)

#         elif request.POST["operation"] == "reply_annotation":
#             annotation_reply = models.CoterieAnnotationReply()
#             annotation = models.CoterieAnnotation.objects.get(id=int(request.POST["reply_to_annotation_id"]))
#             document = models.CoterieDocument.objects.get(id=int(request.POST["document_id"]))
#             annotation_reply.content = request.POST["annotation_reply_content"]
#             annotation_reply.replier = get_user(request)
#             annotation_reply.reply_to_annotation = annotation

#             if request.POST.has_key("reply_to_annotation_reply_id"):
#                 annotation_reply.reply_to_annotation_reply = models.CoterieAnnotationReply.objects.get(id=int(request.POST["reply_to_annotation_reply_id"]))
                
#             annotation_reply.save()

#             context = {
#                 "document": document,
#                 "annotations": document.annotation_set.order_by("page_index"),
#             }

#             return render(request, "file_viewer/annotation_viewer_subpage.html", context)

#     else:
#         document = models.CoterieDocument.objects.get(id = int(request.GET["document_id"]))
#         file = document.unique_file

#         file_position = file.file_field.storage.path(file.file_field)
#         file_url = file.file_field.url

#         file_dirname, file_name_and_extension = os.path.split(file_position)
#         file_name, extension = file_name_and_extension.split(".")
#         img_folder_path = os.path.join(file_dirname, file_name)

#         pages = []

#         user = get_user(request)
#         collected = False
#         if document in user.collected_document_set.all():
#             collected = True

#         document.num_visit += 1
#         document.save()
        
#         if extension == "zip":
#             zip_file = zipfile.ZipFile(file_position, "r")
#             zip_alphabatical_list = sorted(zip_file.namelist())

#             if not os.path.isdir(img_folder_path):
#                 os.mkdir(img_folder_path)
#                 i = 0
#                 for page_name in zip_alphabatical_list:
#                     zip_file.extract(page_name, img_folder_path)
#                     os.rename(os.path.join(img_folder_path, page_name),
#                               os.path.join(img_folder_path, str(i) + "." + page_name.split(".")[-1]))
#                     pages.extend([os.path.dirname(file_url)[1:] + "/" + file_name + "/" + str(i) + "." + page_name.split(".")[-1]])
#                     i += 1
#             else:
#                 i = 0
#                 for page_name in zip_alphabatical_list:
#                     pages.extend([os.path.dirname(file_url)[1:] + "/" + file_name + "/" + str(i) + "." + page_name.split(".")[-1]])
#                     i += 1

#         elif extension == "rar":
#             rar_file = rarfile.RarFile(file_position, "r")
#             rar_alphabatical_list = sorted(rar_file.namelist())

#             if not os.path.isdir(img_folder_path):
#                 os.mkdir(img_folder_path)
#                 i = 0
#                 for page_name in rar_alphabatical_list:
#                     rar_file.extract(page_name, img_folder_path)
#                     os.rename(os.path.join(img_folder_path, page_name),
#                               os.path.join(img_folder_path, str(i) + "." + page_name.split(".")[-1]))
#                     pages.extend([os.path.dirname(file_url)[1:] + "/" + file_name + "/" + str(i) + "." + page_name.split(".")[-1]])
#                     i += 1
#             else:
#                 i = 0
#                 for page_name in rar_alphabatical_list:
#                     pages.extend([os.path.dirname(file_url)[1:] + "/" + file_name + "/" + str(i) + "." + page_name.split(".")[-1]])
#                     i += 1

#         elif extension == "pdf":
#             '''
#             if not os.path.isdir(img_folder_path):
#                 os.mkdir(img_folder_path)
#                 document_images = Image(filename=file_position, resolution=240)
#                 for i, page in enumerate(document_images.sequence):
#                     with Image(page) as page_image:
#                         page_image.alpha_channel = False
#                         page_image.save(filename = os.path.join(img_folder_path, str(i) + ".png"))
#                         pages.extend([os.path.dirname(file_url)[1:] + "/" + file_name + "/" + str(i) + ".png"])
#             else:
#                 document_images = Image(filename=file_position, resolution=180)
#                 for i, page in enumerate(document_images.sequence):
#                     pages.extend([os.path.dirname(file_url)[1:] + "/" + file_name + "/" + str(i) + ".png"])
#             '''
#             context = {
#                 "document": document,
#                 "file_url": file_url[1:],
#                 "comments": document.comment_set.order_by("-post_time"),
#                 "annotations": document.annotation_set.order_by("page_index"),
#                 "collected": collected
#             }
#             return render(request, "file_viewer/pdf_file_viewer_page.html", context)

#         context = {
#             "numPages": len(pages),
#             "document": document,
#             "pages": pages,
#             "comments": document.comment_set.order_by("-post_time"),
#             "annotations": document.annotation_set.order_by("page_index"),
#             "collected": collected,
#         }
#         return render(request, "file_viewer/file_viewer_page.html", context)
