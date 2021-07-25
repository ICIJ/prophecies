import axios from 'axios'
import VuexORM from '@vuex-orm/core'
import VuexORMAxios from '@vuex-orm/plugin-axios'

import Setting from '@/models/Setting'
import User from '@/models/User'
import settings from '@/settings'

// Configure VuexORM to VuexORMAxios and the correct baseUrl
export const baseURL = settings.apiUrl
VuexORM.use(VuexORMAxios, { axios, baseURL })

// Initialize the database
export const database = new VuexORM.Database()
// Models must be registered manually so a store module is created
database.register(Setting)
database.register(User)
