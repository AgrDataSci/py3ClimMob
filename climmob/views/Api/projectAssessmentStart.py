from ..classes import apiView
from pyramid.response import Response
import json

from ...processes import (
    projectExists,
    projectAsessmentStatus,
    getProjectProgress,
    checkAssessments,
    generateAssessmentFiles,
    setAssessmentStatus,
    assessmentExists,
    generateStructureForInterfaceAssessment,
    isAssessmentOpen,
    generateStructureForValidateJsonOdkAssessment,
    numberOfCombinationsForTheProject,
    setAssessmentIndividualStatus,
    AsessmentStatus,
    getPackages,
)

from ..registry import getDataFormPreview
from ...products.forms.form import create_document_form
import os
import uuid
from xml.dom import minidom
from ...processes.odk.api import storeJSONInMySQL


class createProjectAssessment_view(apiView):
    def processView(self):
        if self.request.method == "POST":
            obligatory = [u"project_cod", u"ass_cod"]
            dataworking = json.loads(self.body)

            if sorted(obligatory) == sorted(dataworking.keys()):
                dataworking["user_name"] = self.user.login

                dataInParams = True
                for key in dataworking.keys():
                    if dataworking[key] == "":
                        dataInParams = False

                if dataInParams:
                    exitsproject = projectExists(
                        self.user.login, dataworking["project_cod"], self.request
                    )
                    if exitsproject:
                        progress, pcompleted = getProjectProgress(
                            self.user.login, dataworking["project_cod"], self.request
                        )
                        if progress["regsubmissions"] == 2:
                            if projectAsessmentStatus(
                                self.user.login,
                                dataworking["project_cod"],
                                dataworking["ass_cod"],
                                self.request,
                            ):
                                if progress["assessment"] == True:
                                    checkPass, errors = checkAssessments(
                                        self.user.login,
                                        dataworking["project_cod"],
                                        dataworking["ass_cod"],
                                        self.request,
                                    )
                                    if checkPass:
                                        generateAssessmentFiles(
                                            self.user.login,
                                            dataworking["project_cod"],
                                            dataworking["ass_cod"],
                                            self.request,
                                        )
                                        # setAssessmentStatus(self.user.login, dataworking['project_cod'], 1, self.request)
                                        setAssessmentIndividualStatus(
                                            self.user.login,
                                            dataworking["project_cod"],
                                            dataworking["ass_cod"],
                                            1,
                                            self.request,
                                        )

                                        ncombs, packages = getPackages(
                                            self.user.login,
                                            dataworking["project_cod"],
                                            self.request,
                                        )

                                        data, finalCloseQst = getDataFormPreview(
                                            self,
                                            dataworking["project_cod"],
                                            dataworking["ass_cod"],
                                        )

                                        create_document_form(
                                            self.request,
                                            "en",
                                            self.user.login,
                                            dataworking["project_cod"],
                                            "Assessment",
                                            dataworking["ass_cod"],
                                            data,
                                            packages,
                                        )

                                        response = Response(
                                            status=200,
                                            body=self._("Data collection started."),
                                        )
                                        return response
                                    else:
                                        response = Response(
                                            status=401,
                                            body=json.dumps({"errors": errors}),
                                        )
                                        return response
                                else:
                                    response = Response(
                                        status=401,
                                        body=self._(
                                            "You must have created the assessment forms."
                                        ),
                                    )
                                    return response
                            else:
                                response = Response(
                                    status=401,
                                    body=self._("Data collection has already started."),
                                )
                                return response
                        else:
                            response = Response(
                                status=401,
                                body=self._(
                                    "You cannot add data collection moments. You alreaday started data collection."
                                ),
                            )
                            return response
                    else:
                        response = Response(
                            status=401,
                            body=self._("There is not project with that code."),
                        )
                        return response
                else:
                    response = Response(
                        status=401, body=self._("Not all parameters have data.")
                    )
                    return response
            else:
                response = Response(status=401, body=self._("Error in the JSON."))
                return response
        else:
            response = Response(status=401, body=self._("Only accepts POST method."))
            return response


class cancelAssessmentApi_view(apiView):
    def processView(self):
        if self.request.method == "POST":
            obligatory = [u"project_cod", u"ass_cod"]
            dataworking = json.loads(self.body)

            if sorted(obligatory) == sorted(dataworking.keys()):
                dataworking["user_name"] = self.user.login

                dataInParams = True
                for key in dataworking.keys():
                    if dataworking[key] == "":
                        dataInParams = False

                if dataInParams:
                    exitsproject = projectExists(
                        self.user.login, dataworking["project_cod"], self.request
                    )
                    if exitsproject:
                        if not AsessmentStatus(
                            self.user.login,
                            dataworking["project_cod"],
                            dataworking["ass_cod"],
                            self.request,
                        ):

                            setAssessmentIndividualStatus(
                                self.user.login,
                                dataworking["project_cod"],
                                dataworking["ass_cod"],
                                0,
                                self.request,
                            )
                            # setAssessmentStatus(self.user.login, dataworking['project_cod'], 0, self.request)

                            response = Response(
                                status=200, body=self._("Cancel data collection")
                            )
                            return response

                        else:
                            response = Response(
                                status=401,
                                body=self._(
                                    "Data collection has not started. You cannot cancel it."
                                ),
                            )
                            return response
                    else:
                        response = Response(
                            status=401,
                            body=self._("There is no project with that code."),
                        )
                        return response
                else:
                    response = Response(
                        status=401, body=self._("Not all parameters have data.")
                    )
                    return response
            else:
                response = Response(status=401, body=self._("Error in the JSON."))
                return response
        else:
            response = Response(status=401, body=self._("Only accepts POST method."))
            return response


class closeAssessmentApi_view(apiView):
    def processView(self):
        if self.request.method == "POST":
            obligatory = [u"project_cod", u"ass_cod"]
            dataworking = json.loads(self.body)

            if sorted(obligatory) == sorted(dataworking.keys()):
                dataworking["user_name"] = self.user.login

                dataInParams = True
                for key in dataworking.keys():
                    if dataworking[key] == "":
                        dataInParams = False

                if dataInParams:
                    exitsproject = projectExists(
                        self.user.login, dataworking["project_cod"], self.request
                    )
                    if exitsproject:
                        if not projectAsessmentStatus(
                            self.user.login,
                            dataworking["project_cod"],
                            dataworking["ass_cod"],
                            self.request,
                        ):
                            if assessmentExists(
                                self.user.login,
                                dataworking["project_cod"],
                                dataworking["ass_cod"],
                                self.request,
                            ):

                                setAssessmentIndividualStatus(
                                    self.user.login,
                                    dataworking["project_cod"],
                                    dataworking["ass_cod"],
                                    2,
                                    self.request,
                                )
                                response = Response(
                                    status=200, body=self._("Data collection closed.")
                                )
                                return response

                            else:
                                response = Response(
                                    status=401,
                                    body=self._(
                                        "There is no data collection with that code."
                                    ),
                                )
                                return response
                        else:
                            response = Response(
                                status=401,
                                body=self._(
                                    "Data collection has not started. You cannot cancel it."
                                ),
                            )
                            return response
                    else:
                        response = Response(
                            status=401,
                            body=self._("There is no project with that code."),
                        )
                        return response
                else:
                    response = Response(
                        status=401, body=self._("Not all parameters have data.")
                    )
                    return response
            else:
                response = Response(status=401, body=self._("Error in the JSON."))
                return response
        else:
            response = Response(status=401, body=self._("Only accepts POST method."))
            return response


class readAssessmentStructure_view(apiView):
    def processView(self):
        if self.request.method == "GET":
            obligatory = [u"project_cod", u"ass_cod"]
            try:
                dataworking = json.loads(self.body)
            except:
                response = Response(
                    status=401,
                    body=self._(
                        "Error in the JSON, It does not have the 'body' parameter."
                    ),
                )
                return response

            if sorted(obligatory) == sorted(dataworking.keys()):
                dataworking["user_name"] = self.user.login
                dataworking["section_private"] = None

                dataInParams = True
                for key in dataworking.keys():
                    if dataworking[key] == "":
                        dataInParams = False

                if dataInParams:
                    exitsproject = projectExists(
                        self.user.login, dataworking["project_cod"], self.request
                    )
                    if exitsproject:
                        if not projectAsessmentStatus(
                            self.user.login,
                            dataworking["project_cod"],
                            dataworking["ass_cod"],
                            self.request,
                        ):
                            if assessmentExists(
                                self.user.login,
                                dataworking["project_cod"],
                                dataworking["ass_cod"],
                                self.request,
                            ):
                                response = Response(
                                    status=200,
                                    body=json.dumps(
                                        generateStructureForInterfaceAssessment(
                                            self.user.login,
                                            dataworking["project_cod"],
                                            dataworking["ass_cod"],
                                            self.request,
                                        )
                                    ),
                                )
                                return response
                            else:
                                response = Response(
                                    status=401,
                                    body=self._(
                                        "There is no data collection with that code."
                                    ),
                                )
                                return response
                        else:
                            response = Response(
                                status=401,
                                body=self._("Data collection has not started."),
                            )
                            return response
                    else:
                        response = Response(
                            status=401,
                            body=self._("There is no project with that code."),
                        )
                        return response
                else:
                    response = Response(
                        status=401, body=self._("Not all parameters have data.")
                    )
                    return response
            else:
                response = Response(status=401, body=self._("Error in the JSON."))
                return response
        else:
            response = Response(status=401, body=self._("Only accepts GET method."))
            return response


class pushJsonToAssessment_view(apiView):
    def processView(self):
        if self.request.method == "POST":
            obligatory = [u"project_cod", u"ass_cod", u"json"]
            dataworking = json.loads(self.body)

            if sorted(obligatory) == sorted(dataworking.keys()):
                dataworking["user_name"] = self.user.login

                dataInParams = True
                for key in dataworking.keys():
                    if dataworking[key] == "":
                        dataInParams = False

                if dataInParams:
                    exitsproject = projectExists(
                        self.user.login, dataworking["project_cod"], self.request
                    )
                    if exitsproject:

                        if assessmentExists(
                            self.user.login,
                            dataworking["project_cod"],
                            dataworking["ass_cod"],
                            self.request,
                        ):
                            if not projectAsessmentStatus(
                                self.user.login,
                                dataworking["project_cod"],
                                dataworking["ass_cod"],
                                self.request,
                            ):
                                if isAssessmentOpen(
                                    self.user.login,
                                    dataworking["project_cod"],
                                    dataworking["ass_cod"],
                                    self.request,
                                ):
                                    structure = generateStructureForValidateJsonOdkAssessment(
                                        self.user.login,
                                        dataworking["project_cod"],
                                        dataworking["ass_cod"],
                                        self.request,
                                    )
                                    if structure:
                                        numComb = numberOfCombinationsForTheProject(
                                            self.user.login,
                                            dataworking["project_cod"],
                                            self.request,
                                        )
                                        obligatoryQuestions = [u"clm_start", u"clm_end"]
                                        possibleQuestions = [u"clm_start", u"clm_end"]
                                        searchQST163 = ""
                                        groupsForValidation = {}
                                        for _data in structure:
                                            # the index number 2 is the question.dtype
                                            if _data[2] != 9 and _data[2] != 10:
                                                possibleQuestions.append(
                                                    "grp_"
                                                    + str(_data[0])
                                                    + "/"
                                                    + str(_data[1])
                                                )
                                                if _data[3] == 1:
                                                    obligatoryQuestions.append(
                                                        "grp_"
                                                        + str(_data[0])
                                                        + "/"
                                                        + str(_data[1])
                                                    )
                                            else:
                                                if _data[2] == 9:

                                                    if numComb == 2:
                                                        possibleQuestions.append(
                                                            "grp_"
                                                            + str(_data[0])
                                                            + "/char_"
                                                            + _data[1]
                                                        )
                                                        if _data[3] == 1:
                                                            obligatoryQuestions.append(
                                                                "grp_"
                                                                + str(_data[0])
                                                                + "/char_"
                                                                + _data[1]
                                                            )
                                                    if numComb == 3:
                                                        possibleQuestions.append(
                                                            "grp_"
                                                            + str(_data[0])
                                                            + "/char_"
                                                            + _data[1]
                                                            + "_pos"
                                                        )
                                                        possibleQuestions.append(
                                                            "grp_"
                                                            + str(_data[0])
                                                            + "/char_"
                                                            + _data[1]
                                                            + "_neg"
                                                        )
                                                        if _data[3] == 1:
                                                            obligatoryQuestions.append(
                                                                "grp_"
                                                                + str(_data[0])
                                                                + "/char_"
                                                                + _data[1]
                                                                + "_pos"
                                                            )
                                                            obligatoryQuestions.append(
                                                                "grp_"
                                                                + str(_data[0])
                                                                + "/char_"
                                                                + _data[1]
                                                                + "_neg"
                                                            )

                                                        groupsForValidation[
                                                            _data[1]
                                                        ] = []
                                                        groupsForValidation[
                                                            _data[1]
                                                        ].append(
                                                            "grp_"
                                                            + str(_data[0])
                                                            + "/char_"
                                                            + _data[1]
                                                            + "_pos"
                                                        )
                                                        groupsForValidation[
                                                            _data[1]
                                                        ].append(
                                                            "grp_"
                                                            + str(_data[0])
                                                            + "/char_"
                                                            + _data[1]
                                                            + "_neg"
                                                        )

                                                    if numComb == 4:
                                                        groupsForValidation[
                                                            _data[1]
                                                        ] = []
                                                        for opt in range(0, numComb):
                                                            tittle = (
                                                                "grp_"
                                                                + str(_data[0])
                                                                + "/char_"
                                                                + _data[1]
                                                                + "_stmt_"
                                                                + str(opt + 1)
                                                            )
                                                            groupsForValidation[
                                                                _data[1]
                                                            ].append(tittle)
                                                            possibleQuestions.append(
                                                                tittle
                                                            )
                                                            if _data[3] == 1:
                                                                obligatoryQuestions.append(
                                                                    tittle
                                                                )

                                                if _data[2] == 10:
                                                    for opt in range(0, numComb):
                                                        tittle = (
                                                            "grp_"
                                                            + str(_data[0])
                                                            + "/perf_"
                                                            + _data[1]
                                                            + "_"
                                                            + str(opt + 1)
                                                        )
                                                        possibleQuestions.append(tittle)
                                                        if _data[3] == 1:
                                                            obligatoryQuestions.append(
                                                                tittle
                                                            )

                                            if str(_data[1]) == "QST163":
                                                searchQST163 = (
                                                    "grp_"
                                                    + str(_data[0])
                                                    + "/"
                                                    + str(_data[1])
                                                )

                                        try:
                                            _json = json.loads(dataworking["json"])

                                            permitedKeys = True
                                            for key in _json.keys():
                                                if key not in possibleQuestions:
                                                    permitedKeys = False

                                            if permitedKeys:
                                                obligatoryKeys = True
                                                for key in obligatoryQuestions:
                                                    if key not in _json.keys():
                                                        obligatoryKeys = False

                                                if obligatoryKeys:

                                                    dataInParams = True
                                                    for key in obligatoryQuestions:
                                                        if _json[key].strip(" ") == "":
                                                            dataInParams = False

                                                    if dataInParams:
                                                        if _json[
                                                            searchQST163
                                                        ].isdigit():
                                                            # Validation for repeat response
                                                            for (
                                                                _group
                                                            ) in groupsForValidation:
                                                                letter = []
                                                                for (
                                                                    _var
                                                                ) in groupsForValidation[
                                                                    _group
                                                                ]:

                                                                    if (
                                                                        not _json[_var]
                                                                        in letter
                                                                    ):
                                                                        letter.append(
                                                                            _json[_var]
                                                                        )
                                                                    else:
                                                                        response = Response(
                                                                            status=401,
                                                                            body=self._(
                                                                                "You have repeated data in the next column: "
                                                                                + _var
                                                                                + ". Remember that the options can not be repeated."
                                                                            ),
                                                                        )
                                                                        return response

                                                            # I don't validate el identify of the farmer because the ODK return error if not exist
                                                            _json["clm_deviceimei"] = (
                                                                "API_"
                                                                + str(self.apiKey)
                                                            )
                                                            uniqueId = str(uuid.uuid1())
                                                            path = os.path.join(
                                                                self.request.registry.settings[
                                                                    "user.repository"
                                                                ],
                                                                *[
                                                                    self.user.login,
                                                                    dataworking[
                                                                        "project_cod"
                                                                    ],
                                                                    "data",
                                                                    "ass",
                                                                    dataworking[
                                                                        "ass_cod"
                                                                    ],
                                                                    "json",
                                                                    uniqueId,
                                                                ]
                                                            )

                                                            if not os.path.exists(path):
                                                                os.makedirs(path)

                                                            pathfinal = os.path.join(
                                                                path, uniqueId + ".json"
                                                            )

                                                            f = open(pathfinal, "w")
                                                            f.write(json.dumps(_json))
                                                            f.close()

                                                            storeJSONInMySQL(
                                                                "ASS",
                                                                self.user.login,
                                                                None,
                                                                dataworking[
                                                                    "project_cod"
                                                                ],
                                                                dataworking["ass_cod"],
                                                                pathfinal,
                                                                self.request,
                                                            )

                                                            logFile = pathfinal.replace(
                                                                ".json", ".log"
                                                            )
                                                            if os.path.exists(logFile):
                                                                doc = minidom.parse(
                                                                    logFile
                                                                )
                                                                errors = doc.getElementsByTagName(
                                                                    "error"
                                                                )
                                                                response = Response(
                                                                    status=401,
                                                                    body=self._(
                                                                        "The data could not be saved. ERROR: "
                                                                        + errors[
                                                                            0
                                                                        ].getAttribute(
                                                                            "Error"
                                                                        )
                                                                    ),
                                                                )
                                                                return response

                                                            response = Response(
                                                                status=200,
                                                                body=self._(
                                                                    "Data registered."
                                                                ),
                                                            )
                                                            return response

                                                        else:
                                                            response = Response(
                                                                status=401,
                                                                body=self._(
                                                                    "ERROR: The farmer code must be a number."
                                                                ),
                                                            )
                                                            return response
                                                    else:
                                                        response = Response(
                                                            status=401,
                                                            body=self._(
                                                                "Error in the JSON. Not all parameters have data."
                                                            ),
                                                        )
                                                        return response
                                                else:
                                                    response = Response(
                                                        status=401,
                                                        body=self._(
                                                            "Error in the JSON sent by parameter. Check the obligatory Keys."
                                                        ),
                                                    )
                                                    return response
                                            else:
                                                response = Response(
                                                    status=401,
                                                    body=self._(
                                                        "Error in the JSON sent by parameter. Check the permitted Keys."
                                                    ),
                                                )
                                                return response
                                        except:
                                            response = Response(
                                                status=401,
                                                body=self._(
                                                    "Error in the JSON sent by parameter."
                                                ),
                                            )
                                            return response
                                    else:
                                        response = Response(
                                            status=401,
                                            body=self._(
                                                "The data do not have structure."
                                            ),
                                        )
                                        return response
                                else:
                                    response = Response(
                                        status=401,
                                        body=self._(
                                            "Data collection is closed. After you close data collection, no more data can be entered."
                                        ),
                                    )
                                    return response
                            else:
                                response = Response(
                                    status=401,
                                    body=self._("Data collection has not started."),
                                )
                                return response
                        else:
                            response = Response(
                                status=401,
                                body=self._(
                                    "There is no data collection with that code."
                                ),
                            )
                            return response
                    else:
                        response = Response(
                            status=401,
                            body=self._("There is no project with that code."),
                        )
                        return response
                else:
                    response = Response(
                        status=401, body=self._("Not all parameters have data.")
                    )
                    return response
            else:
                response = Response(status=401, body=self._("Error in the JSON."))
                return response
        else:
            response = Response(status=401, body=self._("Only accepts POST method."))
            return response
