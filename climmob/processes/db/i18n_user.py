from sqlalchemy.exc import IntegrityError
from climmob.models import (
    mapFromSchema,
    I18n,
    I18nUser,
    I18nQuestion,
    I18nQstoption,
    Question,
    mapToSchema,
)
from sqlalchemy import func

__all__ = [
    "getListOfLanguagesByUser",
    "getListOfUnusedLanguagesByUser",
    "addI18nUser",
    "deleteI18nUser",
]


def getListOfLanguagesByUser(request, userName, questionId=None):
    if questionId:
        default = (
            request.dbsession.query(Question.question_lang)
            .filter(Question.question_id == questionId)
            .first()[0]
        )
    else:
        default = ""

    mappedData = mapFromSchema(
        request.dbsession.query(
            I18nUser,
            I18n,
            func.IF(default == I18nUser.lang_code, 1, 0).label("default"),
            (
                request.dbsession.query(func.count(Question.question_id))
                .filter(Question.user_name == userName)
                .filter(Question.question_lang == I18nUser.lang_code)
                .label("Question")
                + request.dbsession.query(func.count(I18nQuestion.lang_code))
                .filter(Question.user_name == userName)
                .filter(Question.question_id == I18nQuestion.question_id)
                .filter(I18nQuestion.lang_code == I18nUser.lang_code)
                .label("I18nQuestion")
                + request.dbsession.query(func.count(I18nQstoption.lang_code))
                .filter(Question.user_name == userName)
                .filter(Question.question_id == I18nQstoption.question_id)
                .filter(I18nQstoption.lang_code == I18nUser.lang_code)
                .label("I18nQstoption")
            ).label("used"),
        )
        .filter(I18nUser.lang_code == I18n.lang_code)
        .filter(I18nUser.user_name == userName)
        .order_by(I18n.lang_name)
        .all()
    )

    return mappedData


def getListOfUnusedLanguagesByUser(request, userName):

    subquery = request.dbsession.query(I18nUser.lang_code).filter(
        I18nUser.user_name == userName
    )

    result = mapFromSchema(
        request.dbsession.query(I18n)
        .filter(I18n.lang_code.not_in(subquery))
        .order_by(I18n.lang_name)
        .all()
    )

    return result


def addI18nUser(data, request):
    mappedData = mapToSchema(I18nUser, data)
    newI18nUser = I18nUser(**mappedData)
    try:
        request.dbsession.add(newI18nUser)
        return True, ""
    except Exception as e:
        return False, str(e)


def deleteI18nUser(data, request):
    try:
        request.dbsession.query(I18nUser).filter(
            I18nUser.user_name == data["user_name"]
        ).filter(I18nUser.lang_code == data["lang_code"]).delete()
        return True, ""
    except IntegrityError as e:
        return False, e
    except Exception as e:
        # print(str(e))
        return False, e