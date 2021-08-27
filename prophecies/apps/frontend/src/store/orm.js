import axios from 'axios'
import VuexORM from '@vuex-orm/core'
import VuexORMAxios from '@vuex-orm/plugin-axios'

import Action from '@/models/Action'
import AlternativeValue from '@/models/AlternativeValue'
import Choice from '@/models/Choice'
import ChoiceGroup from '@/models/ChoiceGroup'
import Project from '@/models/Project'
import Setting from '@/models/Setting'
import Task from '@/models/Task'
import TaskChecker from '@/models/TaskChecker'
import TaskRecord from '@/models/TaskRecord'
import TaskRecordReview from '@/models/TaskRecordReview'
import User from '@/models/User'

import settings from '@/settings'

// Configure VuexORM to use VuexORMAxios and the correct baseUrl
export const baseURL = settings.apiUrl
VuexORM.use(VuexORMAxios, { axios, baseURL })

// Initialize the database
export const database = new VuexORM.Database()
// Models must be registered manually so a store module is created
database.register(Action)
database.register(AlternativeValue)
database.register(Choice)
database.register(ChoiceGroup)
database.register(Project)
database.register(Setting)
database.register(Task)
database.register(TaskChecker)
database.register(TaskRecord)
database.register(TaskRecordReview)
database.register(User)
