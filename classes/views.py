# -*- coding: utf-8 -*-
import json
import datetime

from classweek import const
from classweek.const import ITEM_COUNT_IN_PAGE, WEEKDAY_NUMBER_CONVERTER

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from django.core import serializers
from django.db import IntegrityError
from classes.models import Category, SubCategory, Classes, ClassesInquire, Schedule

def _makeJsonResponse( isSuccess, error_message, error_code = 0 , data = None):
    return_value = {}
    if isSuccess:
        return_value['result'] = const.RESPONSE_STR_SUCCESS
    else:
        return_value['result'] = const.RESPONSE_STR_FAIL
    return_value['error_message'] = error_message
    return_value['error_code'] = error_code
    if data is not None:
        return_value['data'] = data

    return return_value

def _HttpJsonResponse( error, data, error_code = 0):
    if error is None:
        return HttpResponse(json.dumps( _makeJsonResponse( True, None, error_code, data ) , ensure_ascii=False ), content_type="application/json; charset=utf-8" )
    else:
        return HttpResponse(json.dumps( _makeJsonResponse( False, error, error_code, data ) , ensure_ascii=False ), content_type="application/json; charset=utf-8" )


@csrf_exempt
def getSubCategoryList_view( request, category_name ):

    category = Category.objects.filter( name = category_name ).select_related( 'get_subcategorys' )
    if category.exists():
        subCategorys = category.first().get_subcategorys.filter( category__name = category_name ).values()

        return _HttpJsonResponse( None, list(subCategorys) )
    else:
        return _HttpJsonResponse( const.ERROR_CATEGORY_NAME_DOES_NOT_EXIST, None , const.CODE_ERROR_CATEGORY_NAME_DOES_NOT_EXIST )

# location, weekday, time( morning, .. ), price ( by month )
@csrf_exempt
def getClassesList_view( request, category_name, subcategory_name, page_num = 1 ):
    page_num = int(page_num)

    subcategory = SubCategory.objects.filter( name = subcategory_name ).select_related( 'get_classes' )
    if subcategory.exists():
        classes = subcategory.first().get_classes.filter( subCategory__name = subcategory_name ).select_related('get_schedules', 'company',  ).all()
        classes_list = []

        for classes_item in classes:
            item = {}
            item.update( {
                'id':classes_item.id,
                'title':classes_item.title,
                'company':classes_item.company.name,
                'nearby_station':classes_item.company.nearby_station,
                'price_of_day':classes_item.priceOfDay,
                'price_of_month':classes_item.priceOfMonth,
                'image_url':classes_item.image_url,
                'discount_rate': round(100 - classes_item.priceOfMonth*100.0/(classes_item.priceOfDay*classes_item.countOfMonth))
                } )
            schedules = classes_item.get_schedules.all()
            for schedule in schedules:
                item_detail = item.copy()
                dayOfWeek_list = schedule.dayOfWeek.split('|')
                startTime_list = schedule.startTime.split('|')

                times = []
                for i in range( len(dayOfWeek_list ) ):
                    times.append( dayOfWeek_list[i] + " : " + startTime_list[i] )

                item_detail.update( {
                    'times': times,
                    'duration': schedule.duration.strftime("%H시간%M분").decode('utf-8'),
                    'schedule_id':schedule.id
                })

                classes_list.append( item_detail )

        return _HttpJsonResponse( None, classes_list[ (page_num-1)*ITEM_COUNT_IN_PAGE : page_num*ITEM_COUNT_IN_PAGE ] )
        # return _HttpJsonResponse( None, json.dumps( classes_list[ (page_num-1)*ITEM_COUNT_IN_PAGE : page_num*ITEM_COUNT_IN_PAGE ] , ensure_ascii=False ) )
    else:
        return _HttpJsonResponse( const.ERROR_SUBCATEGORY_NAME_DOES_NOT_EXIST, None , const.CODE_ERROR_SUBCATEGORY_NAME_DOES_NOT_EXIST )

@csrf_exempt
def getClassesDetail_view( request, classes_id, schedule_id ):
    classes = Classes.objects.select_related('company', 'get_images' ).get( id = classes_id )
    schedule = Schedule.objects.get( id = schedule_id )

    classes_detail = {}

    classes_detail.update( {
        'id': classes.id,
        'title': classes.title,
        'company': classes.company.name,
        'nearby_station': classes.company.nearby_station,
        'address': classes.company.location,
        'person_or_group': classes.personalOrGroup,
        'description': classes.description,
        'preparation': classes.preparation,
        'refund_info': classes.refundInfomation,
        'price_of_day': classes.priceOfDay,
        'price_of_month': classes.priceOfMonth,
        'count_of_month': classes.countOfMonth,
        'discount_rate': round(100 - classes.priceOfMonth*100.0/(classes.priceOfDay*classes.countOfMonth)),
        'image_url': classes.image_url,
    })

    facilitiesInfomation = classes.company.facilitiesInfomation

    classes_detail.update({
        'toilet': facilitiesInfomation.__contains__('toilet'),
        'fitting_room': facilitiesInfomation.__contains__('fitting_room'),
        'shower_stall': facilitiesInfomation.__contains__('shower_stall'),
        'locker': facilitiesInfomation.__contains__('locker'),
        'parking_lot': facilitiesInfomation.__contains__('parking_lot'),
        'practice_room': facilitiesInfomation.__contains__('practice_room'),
        'instrument_rental': facilitiesInfomation.__contains__('instrument_rental')
    })

    images = classes.get_images.all()
    detail_images = []
    for image in images:
        detail_images.append( image.image_url )

    classes_detail.update({\
        'detail_image_url': detail_images
    })

    dayOfWeek_list = schedule.dayOfWeek.split('|')
    startTime_list = schedule.startTime.split('|')

    times = []
    for i in range( len(dayOfWeek_list ) ):
        times.append( dayOfWeek_list[i] + " : " + startTime_list[i] )

    classes_detail.update({
        'times':times,
        'duration':schedule.duration.strftime("%H시간%M분").decode('utf-8'),
        'schedule_id':schedule.id
    })

    today = datetime.datetime.today()
    today_year = today.year
    today_month = today.month
    today_day = today.day
    timedelta_from_today = datetime.timedelta()
    today_weekday = today.weekday()

    current_weekday_position = 0
    for i in range( len(dayOfWeek_list ) ):
        if today_weekday <= WEEKDAY_NUMBER_CONVERTER[dayOfWeek_list[i]]:
            current_weekday_position = i
            break

    one_month_schedule = []
    for i in range(4):

        for j in range( current_weekday_position, len(dayOfWeek_list ) ):
            if (today+timedelta_from_today).weekday() <= WEEKDAY_NUMBER_CONVERTER[dayOfWeek_list[j]]:
                timedelta_from_today = datetime.timedelta(days=timedelta_from_today.days+WEEKDAY_NUMBER_CONVERTER[dayOfWeek_list[j]]-(today+timedelta_from_today).weekday())
            else:
                timedelta_from_today = datetime.timedelta(days=7+timedelta_from_today.days+WEEKDAY_NUMBER_CONVERTER[dayOfWeek_list[j]]-(today+timedelta_from_today).weekday())

            start_date = today+timedelta_from_today
            if j == 0:
                end_date = start_date + datetime.timedelta(days=21+WEEKDAY_NUMBER_CONVERTER[dayOfWeek_list[len(dayOfWeek_list)-1]] - start_date.weekday())
            else:
                end_date = start_date + datetime.timedelta(days=28+WEEKDAY_NUMBER_CONVERTER[dayOfWeek_list[j-1]] - start_date.weekday())

            one_month_schedule.append( {
                'start_date_time':str(start_date.month)+"-"+str(start_date.day)+"("+WEEKDAY_NUMBER_CONVERTER[start_date.weekday()]+") " + str(startTime_list[j]),
                'end_date_time':str(end_date.month)+"-"+str(end_date.day)+"("+WEEKDAY_NUMBER_CONVERTER[end_date.weekday()]+") " + str(startTime_list[j])
            })

        for j in range( 0, current_weekday_position+1 ):
            if (today+timedelta_from_today).weekday() <= WEEKDAY_NUMBER_CONVERTER[dayOfWeek_list[j]]:
                timedelta_from_today = datetime.timedelta(days=timedelta_from_today.days+WEEKDAY_NUMBER_CONVERTER[dayOfWeek_list[j]]-(today+timedelta_from_today).weekday())
            else:
                timedelta_from_today = datetime.timedelta(days=7+timedelta_from_today.days+WEEKDAY_NUMBER_CONVERTER[dayOfWeek_list[j]]-(today+timedelta_from_today).weekday())

            start_date = today+timedelta_from_today
            if j == 0:
                end_date = start_date + datetime.timedelta(days=21+WEEKDAY_NUMBER_CONVERTER[dayOfWeek_list[len(dayOfWeek_list)-1]] - start_date.weekday())
            else:
                end_date = start_date + datetime.timedelta(days=28+WEEKDAY_NUMBER_CONVERTER[dayOfWeek_list[j-1]] - start_date.weekday())

            one_month_schedule.append( {
                'start_date_time':str(start_date.month)+"-"+str(start_date.day)+"("+WEEKDAY_NUMBER_CONVERTER[start_date.weekday()]+") " + str(startTime_list[j]),
                'end_date_time':str(end_date.month)+"-"+str(end_date.day)+"("+WEEKDAY_NUMBER_CONVERTER[end_date.weekday()]+") " + str(startTime_list[j])
            })

    classes_detail.update({
        'one_month_schedule':one_month_schedule
    })

    # print repr(classes)
    return _HttpJsonResponse( None, classes_detail )

@csrf_exempt
def inquire_view( request, classes_id ):
    if not(request.user.is_authenticated()):
        return HttpResponse( json.dumps( _makeJsonResponse( False, const.ERROR_HAVE_TO_LOGIN, const.CODE_ERROR_HAVE_TO_LOGIN ) ), content_type="application/json" )
    else:
        classesInquire = ClassesInquire( classes_id = classes_id, user = request.user, content= request.POST.get('content') )
        # classesInquire.classes_id = classes_id
        try:
            classesInquire.save()
        except IntegrityError:
            return HttpResponse( json.dumps( _makeJsonResponse( False, const.ERROR_CLASSES_INQUIRE_FAIL, const.CODE_ERROR_CLASSES_INQUIRE_FAIL ) ), content_type="application/json" )
        return HttpResponse( json.dumps( _makeJsonResponse( True, None ) ), content_type="application/json" )
