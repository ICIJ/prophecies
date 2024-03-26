import TaskTemplateSetting from '@/models/TaskTemplateSetting'

export default class TaskTemplateSettingForText extends TaskTemplateSetting {
  static entity = 'TaskTemplateSettingForText'

  static fields() {
    return {
      ...super.fields()
    }
  }
}
