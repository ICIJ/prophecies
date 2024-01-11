import axios from 'axios'
import VuexORM from '@vuex-orm/core'
import VuexORMAxios from '@vuex-orm/plugin-axios'

import Action from '@/models/Action'
import ActionAggregate from '@/models/ActionAggregate'
import AlternativeValue from '@/models/AlternativeValue'
import Choice from '@/models/Choice'
import ChoiceGroup from '@/models/ChoiceGroup'
import Operation from '@/models/Operation'
import Project from '@/models/Project'
import Setting from '@/models/Setting'
import Task from '@/models/Task'
import TaskChecker from '@/models/TaskChecker'
import TaskRecord from '@/models/TaskRecord'
import TaskRecordMedia from '@/models/TaskRecordMedia'
import TaskRecordReview from '@/models/TaskRecordReview'
import TaskTemplateSetting from '@/models/TaskTemplateSetting'
import TaskTemplateSettingForIframe from '@/models/TaskTemplateSettingForIframe'
import TaskTemplateSettingForMedia from '@/models/TaskTemplateSettingForMedia'
import TaskTemplateSettingForText from '@/models/TaskTemplateSettingForText'
import TaskUserStatistics from '@/models/TaskUserStatistics'
import TaskUserChoiceStatistics from '@/models/TaskUserChoiceStatistics'
import Tip from '@/models/Tip'
import User from '@/models/User'
import UserNotification from '@/models/UserNotification'

import settings from '@/settings'

// Configure VuexORM to use VuexORMAxios and the correct baseUrl
export const baseURL = settings.apiUrl
VuexORM.use(VuexORMAxios, { axios, baseURL })

// Initialize the database
export const database = new VuexORM.Database()
// Models must be registered manually so a store module is created
database.register(Action)
database.register(ActionAggregate)
database.register(AlternativeValue)
database.register(Choice)
database.register(ChoiceGroup)
database.register(UserNotification)
database.register(Operation)
database.register(Project)
database.register(Setting)
database.register(Task)
database.register(TaskChecker)
database.register(TaskRecord)
database.register(TaskRecordMedia)
database.register(TaskRecordReview)
database.register(TaskUserStatistics)
database.register(TaskTemplateSetting)
database.register(TaskTemplateSettingForIframe)
database.register(TaskTemplateSettingForMedia)
database.register(TaskTemplateSettingForText)
database.register(TaskUserChoiceStatistics)
database.register(Tip)
database.register(User)
