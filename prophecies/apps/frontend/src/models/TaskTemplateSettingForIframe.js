import TaskTemplateSetting from '@/models/TaskTemplateSetting'

export default class TaskTemplateSettingForIframe extends TaskTemplateSetting {
  static entity = 'TaskTemplateSettingForIframe'
  static baseEntity = 'TaskTemplateSetting'

  static fields () {
    return {
      ...super.fields(),
    }
  }
}
