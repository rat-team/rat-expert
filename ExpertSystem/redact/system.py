# coding=utf-8
import json
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from ExpertSystem.models import System
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_post_params
from ExpertSystem.utils.log_manager import log
from scripts.recreate import recreate


def create_db(request):
    recreate()
    return HttpResponse(content="OK")


def add_system(request, **kwargs):

    if "system_id" in kwargs:
        # Если выбрали редактирование конкретной системы
        system_id = kwargs["system_id"]
        try:
            system = System.objects.get(id=system_id, user_id=request.user.id, is_deleted=False)
            sessions.init_es_create_session(request, system.id)
            return render(request, "add_system/add_system.html", {"system": system})
        except System.DoesNotExist:
            return redirect("/", {'error': u'Вы не можете редактировать эту систему'})
        except Exception as e:
            log.exception(e)
            return redirect("/", {'error': u'Что-то пошло не так...'})
    else:
        session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
        if session:
            # Если внутри редактирования вернулись на страницу создания системы
            try:
                system = System.objects.get(id=session["system_id"], user_id=request.user.id, is_deleted=False)
            except System.DoesNotExist:
                return redirect("/", {'error': u'Вы не можете редактировать эту систему'})
            except Exception as e:
                log.exception(e)
                return redirect("/", {'error': u'Что-то пошло не так...'})
            return render(request, "add_system/add_system.html", {"system": system})

        # Иначе все по нулям
        return render(request, "add_system/add_system.html")


@login_required(login_url="/login/")
@require_http_methods(["POST"])
@require_post_params("system_name")
def insert_system(request):

    response = {
        "code": 0,
    }

    system_name = request.POST.get("system_name")
    system_about = request.POST.get("system_about")
    system_pic = request.FILES.get('system_pic')

    if system_pic:
        try:
            trial_image = Image.open(system_pic)
            trial_image.verify()
        except IOError:
            response = {
                'code': 1,
                'msg': u'Загрузите корректную картинку.'
            }
            return HttpResponse(json.dumps(response), content_type="application/json")
        except Exception as e:
            log.exception(e)
            response = {
                'code': 1,
                'msg': u'Загрузите корректную картинку.'
            }
            return HttpResponse(json.dumps(response), content_type="application/json")

    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    if session:
        try:
            system = System.objects.get(id=session["system_id"], is_deleted=False)
        except System.DoesNotExist:
            log.error("System " + session["system_id"] + " doesn\'t exist.")
            response = {
                'code': 1,
                'msg': u'Системы не существует. Попробуйте заново создать систему.'
            }
            return HttpResponse(json.dumps(response), content_type="application/json")

        system.name = system_name
        system.about = system_about
        if system_pic:
            system.photo = system_pic
        try:
            system.save()
        except Exception as e:
            log.exception(e)
            response = {
                'code': 1,
                'msg': u'Что-то пошло не так. Попробуйте позже.'
            }
            return HttpResponse(json.dumps(response), content_type="application/json")

        return HttpResponse(json.dumps(response), content_type="application/json")

    params = {
        "name": system_name,
        "user": request.user,
        "about": system_about,
    }
    if system_pic:
        params.update({"photo": system_pic})
    try:
        system = System.objects.create(**params)
    except Exception as e:
        log.exception(e)
        response = {
            'code': 1,
            'msg': u'Что-то пошло не так. Попробуйте позже.'
        }
        return HttpResponse(json.dumps(response), content_type="application/json")

    sessions.init_es_create_session(request, system.id)
    return HttpResponse(json.dumps(response), content_type="application/json")