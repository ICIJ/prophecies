import TaskTemplateSetting from '@/models/TaskTemplateSetting'

export default class TaskTemplateSettingForMedia extends TaskTemplateSetting {
  static entity = 'TaskTemplateSettingForMedia'

  static fields() {
    return {
      ...super.fields(),
      maxWidth: this.number(null),
      maxHeight: this.number(null),
      displayOriginalValue: this.boolean(true)
    }
  }
}
